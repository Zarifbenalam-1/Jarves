"""
JARVIS LiveKit Voice Engine
Real-time voice interaction with JARVIS AI
"""

import asyncio
import os
import sys
import json
import logging
import numpy as np
import threading
import queue
from datetime import datetime

# LiveKit imports
from livekit import api, rtc, agents
import speech_recognition as sr
import pyttsx3
import edge_tts
import io
import wave

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

class JarvisVoiceEngine:
    def __init__(self):
        # Load credentials from environment
        self.livekit_url = "wss://jarvis-bg7u43x4.livekit.cloud"
        self.api_key = "APIBsSZnWSF7q7K"
        self.api_secret = "lJU8krmu6jJ9TtHeg1wE1von277ex2V7qCZBj6U5fTIB"
        
        # Initialize AI engine
        self.ai = JarvisAI()
        
        # Voice processing components
        self.room = None
        self.audio_source = None
        self.local_audio_track = None
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # TTS Engine
        self.tts_engine = pyttsx3.init()
        self.setup_tts_voices()
        
        # Voice processing state
        self.is_listening = False
        self.is_speaking = False
        self.conversation_active = False
        
        # Audio processing queues
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.command_queue = queue.Queue()
        
        # Wake word detection
        self.wake_words = ["jarvis", "hey jarvis", "jarvis activate"]
        self.wake_word_detected = False
        
        # Conversation context
        self.conversation_buffer = []
        self.last_interaction = None
        
        print("🤖 JARVIS Voice Engine initialized")
        
    def setup_tts_voices(self):
        """Setup TTS voices for different personalities"""
        voices = self.tts_engine.getProperty('voices')
        
        # Voice mapping for personalities
        self.personality_voices = {
            'standard': {
                'voice_id': 0,
                'rate': 180,
                'volume': 0.9
            },
            'professional': {
                'voice_id': 0,
                'rate': 160,
                'volume': 0.95
            },
            'sarcastic': {
                'voice_id': 1 if len(voices) > 1 else 0,
                'rate': 200,
                'volume': 0.85
            },
            'unleashed': {
                'voice_id': 1 if len(voices) > 1 else 0,
                'rate': 220,
                'volume': 1.0
            },
            'genius': {
                'voice_id': 0,
                'rate': 140,
                'volume': 0.9
            }
        }
    
    async def connect_to_livekit(self, room_name="jarvis-voice-room"):
        """Connect to LiveKit room"""
        try:
            print(f"🔗 Connecting to LiveKit room: {room_name}")
            
            # Create access token
            token = api.AccessToken(self.api_key, self.api_secret)
            token.with_identity("jarvis-ai")
            token.with_name("JARVIS AI Assistant")
            token.with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True
            ))
            
            # Initialize room
            self.room = rtc.Room()
            self.setup_room_events()
            
            # Connect to room
            await self.room.connect(self.livekit_url, token.to_jwt())
            
            # Setup audio publishing
            await self.setup_audio_publishing()
            
            print("✅ Connected to LiveKit successfully!")
            return True
            
        except Exception as e:
            print(f"❌ LiveKit connection failed: {e}")
            return False
    
    def setup_room_events(self):
        """Setup LiveKit room event handlers"""
        @self.room.on("participant_connected")
        def on_participant_connected(participant: rtc.RemoteParticipant):
            print(f"👋 User connected: {participant.identity}")
            # Welcome message
            asyncio.create_task(self.speak_response("Welcome, Sir. JARVIS voice interface is now active."))
        
        @self.room.on("participant_disconnected") 
        def on_participant_disconnected(participant: rtc.RemoteParticipant):
            print(f"👋 User disconnected: {participant.identity}")
        
        @self.room.on("track_received")
        def on_track_received(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.RemoteParticipant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                print(f"🎤 Receiving audio from {participant.identity}")
                asyncio.create_task(self.process_incoming_audio(track))
        
        @self.room.on("data_received")
        def on_data_received(data: bytes, participant: rtc.RemoteParticipant):
            try:
                message = json.loads(data.decode())
                self.handle_data_message(message, participant)
            except Exception as e:
                print(f"❌ Data message error: {e}")
    
    async def setup_audio_publishing(self):
        """Setup audio track for JARVIS responses"""
        try:
            # Create audio source (24kHz, mono)
            self.audio_source = rtc.AudioSource(24000, 1)
            
            # Create local audio track
            self.local_audio_track = rtc.LocalAudioTrack.create_audio_track(
                "jarvis-voice", self.audio_source
            )
            
            # Publish the track
            await self.room.local_participant.publish_track(self.local_audio_track)
            
            print("🔊 Audio publishing setup complete")
            
        except Exception as e:
            print(f"❌ Audio setup error: {e}")
    
    async def process_incoming_audio(self, track: rtc.AudioTrack):
        """Process incoming audio for speech recognition"""
        try:
            audio_stream = rtc.AudioStream(track)
            
            async for frame in audio_stream:
                if self.is_listening:
                    # Convert audio frame to recognizable format
                    audio_data = np.frombuffer(frame.data, dtype=np.int16)
                    
                    # Voice activity detection
                    if self.detect_voice_activity(audio_data):
                        # Process speech
                        await self.process_speech_frame(audio_data)
                        
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
    
    def detect_voice_activity(self, audio_data):
        """Simple voice activity detection"""
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
        normalized_rms = rms / 32768.0
        
        # Voice activity threshold
        return normalized_rms > 0.01
    
    async def process_speech_frame(self, audio_data):
        """Process speech from audio frame"""
        try:
            # Add to buffer for recognition
            self.audio_queue.put(audio_data)
            
            # Process if buffer is full enough
            if self.audio_queue.qsize() > 10:  # Roughly 0.5 seconds at 24kHz
                await self.recognize_speech_from_buffer()
                
        except Exception as e:
            print(f"❌ Speech processing error: {e}")
    
    async def recognize_speech_from_buffer(self):
        """Recognize speech from audio buffer"""
        try:
            # Collect audio data from queue
            audio_frames = []
            while not self.audio_queue.empty():
                audio_frames.append(self.audio_queue.get())
            
            if not audio_frames:
                return
            
            # Combine frames
            combined_audio = np.concatenate(audio_frames)
            
            # Convert to audio format for recognition
            audio_bytes = combined_audio.tobytes()
            
            # Create AudioData object for speech recognition
            audio_data = sr.AudioData(audio_bytes, 24000, 2)
            
            # Recognize speech
            try:
                text = self.recognizer.recognize_google(audio_data, language='en-US')
                if text.strip():
                    print(f"🎤 Recognized: {text}")
                    await self.process_voice_command(text)
                    
            except sr.UnknownValueError:
                # No speech recognized
                pass
            except sr.RequestError as e:
                print(f"🔴 Speech recognition error: {e}")
                
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
    
    async def process_voice_command(self, text):
        """Process recognized voice command"""
        try:
            text_lower = text.lower()
            
            # Check for wake word
            wake_word_found = any(wake_word in text_lower for wake_word in self.wake_words)
            
            if wake_word_found or self.conversation_active:
                # Remove wake word from command
                command = text
                for wake_word in self.wake_words:
                    command = command.replace(wake_word, "").strip()
                
                if command or self.conversation_active:
                    # Activate conversation mode
                    self.conversation_active = True
                    self.last_interaction = datetime.now()
                    
                    # Process command
                    await self.handle_ai_command(command if command else text)
                    
                    # Send acknowledgment
                    await self.send_data_message({
                        "type": "command_received",
                        "command": command,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Check for voice control commands
            if "voice off" in text_lower:
                await self.stop_listening()
            elif "voice on" in text_lower:
                await self.start_listening()
            elif "end conversation" in text_lower:
                self.conversation_active = False
                await self.speak_response("Conversation ended, Sir.")
                
        except Exception as e:
            print(f"❌ Command processing error: {e}")
    
    async def handle_ai_command(self, command):
        """Handle AI command and generate response"""
        try:
            print(f"🧠 Processing AI command: {command}")
            
            # Send status update
            await self.send_data_message({
                "type": "processing",
                "status": "Thinking..."
            })
            
            # Get AI response in background thread
            def get_ai_response():
                try:
                    response = self.ai.chat(command)
                    self.response_queue.put(("success", response))
                except Exception as e:
                    self.response_queue.put(("error", str(e)))
            
            # Run in thread to avoid blocking
            thread = threading.Thread(target=get_ai_response, daemon=True)
            thread.start()
            
            # Wait for response with timeout
            start_time = datetime.now()
            while thread.is_alive():
                if (datetime.now() - start_time).seconds > 10:  # 10 second timeout
                    self.response_queue.put(("error", "Response timeout"))
                    break
                await asyncio.sleep(0.1)
            
            # Get response from queue
            if not self.response_queue.empty():
                status, response = self.response_queue.get()
                
                if status == "success":
                    # Speak the response
                    await self.speak_response(response)
                    
                    # Add to conversation buffer
                    self.conversation_buffer.append({
                        "user": command,
                        "jarvis": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Send response data
                    await self.send_data_message({
                        "type": "ai_response",
                        "response": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                else:
                    error_msg = f"I'm sorry, Sir. I encountered an error: {response}"
                    await self.speak_response(error_msg)
                    
        except Exception as e:
            error_msg = f"I apologize, Sir. There was a system error: {str(e)}"
            await self.speak_response(error_msg)
    
    async def speak_response(self, text):
        """Convert text to speech and stream via LiveKit"""
        try:
            if self.is_speaking:
                return  # Prevent overlapping speech
            
            self.is_speaking = True
            print(f"🔊 JARVIS speaking: {text[:50]}...")
            
            # Get current personality for voice settings
            personality = self.ai.get_current_personality()
            voice_settings = self.personality_voices.get(personality, self.personality_voices['standard'])
            
            # Configure TTS engine
            self.tts_engine.setProperty('voice', self.tts_engine.getProperty('voices')[voice_settings['voice_id']].id)
            self.tts_engine.setProperty('rate', voice_settings['rate'])
            self.tts_engine.setProperty('volume', voice_settings['volume'])
            
            # Generate speech using edge-tts for better quality
            try:
                await self.speak_with_edge_tts(text, personality)
            except:
                # Fallback to pyttsx3
                self.speak_with_pyttsx3(text)
            
            self.is_speaking = False
            
        except Exception as e:
            print(f"❌ Speech synthesis error: {e}")
            self.is_speaking = False
    
    async def speak_with_edge_tts(self, text, personality):
        """Use edge-tts for high-quality speech"""
        try:
            # Voice mapping for edge-tts
            edge_voices = {
                'standard': 'en-US-AriaNeural',
                'professional': 'en-US-SaraNeural',
                'sarcastic': 'en-US-GuyNeural',
                'unleashed': 'en-US-JennyNeural',
                'genius': 'en-US-BrianNeural'
            }
            
            voice = edge_voices.get(personality, edge_voices['standard'])
            
            # Generate speech
            communicate = edge_tts.Communicate(text, voice)
            
            # Stream audio data
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            # Convert to proper format and stream via LiveKit
            if audio_data and self.audio_source:
                await self.stream_audio_to_livekit(audio_data)
                
        except Exception as e:
            print(f"❌ Edge-TTS error: {e}")
            raise e
    
    def speak_with_pyttsx3(self, text):
        """Fallback TTS using pyttsx3"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ pyttsx3 error: {e}")
    
    async def stream_audio_to_livekit(self, audio_data):
        """Stream audio data via LiveKit"""
        try:
            # This is a simplified version - you'd need proper audio format conversion
            # Convert audio to proper sample rate and format for LiveKit
            
            # For now, we'll use a placeholder
            print(f"🌊 Streaming {len(audio_data)} bytes to LiveKit")
            
            # In a real implementation, you'd:
            # 1. Convert audio to PCM format
            # 2. Resample to 24kHz if needed
            # 3. Send frames to audio_source
            
        except Exception as e:
            print(f"❌ Audio streaming error: {e}")
    
    async def send_data_message(self, message):
        """Send data message to participants"""
        try:
            if self.room:
                data = json.dumps(message).encode()
                await self.room.local_participant.publish_data(data)
        except Exception as e:
            print(f"❌ Data message error: {e}")
    
    def handle_data_message(self, message, participant):
        """Handle incoming data messages"""
        try:
            msg_type = message.get("type")
            
            if msg_type == "user_status":
                print(f"📊 User status: {message}")
            elif msg_type == "command_request":
                command = message.get("command")
                if command:
                    asyncio.create_task(self.process_voice_command(command))
                    
        except Exception as e:
            print(f"❌ Data message handling error: {e}")
    
    async def start_listening(self):
        """Start voice recognition"""
        try:
            self.is_listening = True
            print("🎤 Voice recognition started - Say 'JARVIS' to activate")
            
            # Calibrate microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            await self.send_data_message({
                "type": "voice_status",
                "listening": True,
                "wake_words": self.wake_words
            })
            
        except Exception as e:
            print(f"❌ Failed to start listening: {e}")
    
    async def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        self.conversation_active = False
        print("🔇 Voice recognition stopped")
        
        await self.send_data_message({
            "type": "voice_status", 
            "listening": False
        })
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            self.is_listening = False
            self.is_speaking = False
            
            if self.room:
                await self.room.disconnect()
            
            print("🧹 JARVIS Voice Engine cleaned up")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")

# Main voice interface runner
async def main():
    """Main voice interface"""
    print("🔥 Starting JARVIS Voice Interface...")
    
    try:
        # Initialize voice engine
        voice_engine = JarvisVoiceEngine()
        
        # Connect to LiveKit
        connected = await voice_engine.connect_to_livekit()
        
        if not connected:
            print("❌ Failed to connect to LiveKit")
            return
        
        # Start listening
        await voice_engine.start_listening()
        
        print("✅ JARVIS Voice Interface active!")
        print("💬 Commands:")
        print("   - Say 'JARVIS' or 'Hey JARVIS' followed by your command")
        print("   - Say 'voice off' to stop listening")
        print("   - Say 'end conversation' to exit conversation mode")
        print("   - Press Ctrl+C to exit")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
                
                # Check for conversation timeout
                if (voice_engine.conversation_active and 
                    voice_engine.last_interaction and
                    (datetime.now() - voice_engine.last_interaction).seconds > 30):
                    
                    voice_engine.conversation_active = False
                    await voice_engine.speak_response("Conversation timeout. Say JARVIS to reactivate.")
                
        except KeyboardInterrupt:
            print("\n👋 Shutting down JARVIS Voice Interface...")
            
    except Exception as e:
        print(f"❌ Voice interface error: {e}")
        
    finally:
        if 'voice_engine' in locals():
            await voice_engine.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
