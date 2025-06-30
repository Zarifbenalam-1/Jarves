"""
JARVIS Enhanced Voice Engine
Advanced LiveKit Voice Integration with Devil Level Features
"""

import asyncio
import os
import sys
import json
import logging
import numpy as np
import threading
import queue
import time
from datetime import datetime
import wave
import io
import tempfile
# import audioop  # Not available in Python 3.13
from typing import Optional, Dict, List, Tuple

# Voice processing imports (LiveKit removed - not available on PyPI)
# from livekit import api, rtc, agents  # Enterprise feature - not available
import speech_recognition as sr
import pyttsx3
# import sounddevice as sd  # Not needed for basic voice
# from google.cloud import speech  # Optional - requires Google Cloud setup
# import edge_tts  # Optional - for premium voices

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

class EmotionAnalyzer:
    """Analyzes emotional tone in speech audio"""
    
    EMOTIONS = ["neutral", "happy", "angry", "sad", "excited", "worried", "urgent"]
    
    def __init__(self):
        self.prev_emotion = "neutral"
        self.emotion_threshold = 0.6
    
    def analyze(self, audio_data: np.ndarray) -> str:
        """
        Analyze audio data for emotional content
        Returns emotion string: neutral, happy, angry, sad, excited, worried, urgent
        """
        # Basic analysis using audio properties
        try:
            # Convert to float array if needed
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Extract audio features
            rms = np.sqrt(np.mean(np.square(audio_data)))
            zero_crossings = np.sum(np.abs(np.diff(np.signbit(audio_data)))) / len(audio_data)
            spectral_centroid = self._get_spectral_centroid(audio_data)
            
            # Simple emotion rules (in production, use a proper ML model)
            emotion = "neutral"
            confidence = 0.5
            
            # Volume-based emotions
            if rms > 0.4:  # Loud
                if zero_crossings > 0.1:  # Many zero crossings = high frequency content
                    emotion = "angry" if spectral_centroid > 2000 else "excited"
                    confidence = min(0.7 + rms * 0.5, 0.95)
                else:
                    emotion = "urgent"
                    confidence = min(0.6 + rms * 0.3, 0.9)
            elif rms > 0.2:  # Medium volume
                if zero_crossings > 0.08:
                    emotion = "happy"
                    confidence = 0.6
                else:
                    emotion = "neutral"
                    confidence = 0.7
            else:  # Quiet
                if zero_crossings < 0.05:
                    emotion = "sad" if spectral_centroid < 1500 else "worried"
                    confidence = 0.6
                else:
                    emotion = "neutral"
                    confidence = 0.8
            
            # Simple smoothing
            if confidence < self.emotion_threshold and self.prev_emotion != "neutral":
                emotion = self.prev_emotion
            
            self.prev_emotion = emotion
            return emotion
            
        except Exception as e:
            print(f"Emotion analysis error: {e}")
            return "neutral"
    
    def _get_spectral_centroid(self, audio_data: np.ndarray, sample_rate: int = 16000) -> float:
        """Calculate spectral centroid of audio (simple version)"""
        try:
            if len(audio_data) < 256:
                return 1000.0  # Default for short segments
                
            # Simple FFT for frequency analysis
            fft_data = np.abs(np.fft.rfft(audio_data[:1024]))
            freqs = np.fft.rfftfreq(1024, 1/sample_rate)
            
            # Avoid divide by zero
            if np.sum(fft_data) == 0:
                return 1000.0
                
            # Calculate centroid
            centroid = np.sum(freqs * fft_data) / np.sum(fft_data)
            return centroid
        except:
            return 1000.0  # Default fallback

class VoiceActivityDetector:
    """Detects when someone is speaking"""
    
    def __init__(self):
        self.energy_threshold = 300  # Adjustable energy threshold
        self.silence_threshold = 0.3  # Seconds of silence to mark end of speech
        self.speaking_threshold = 0.1  # Seconds of speech to mark start of speech
        self.is_speaking = False
        self.silence_start_time = None
        self.speech_start_time = None
    
    def detect(self, audio_data: np.ndarray) -> bool:
        """
        Detect if the audio contains speech
        Returns True if speech is detected
        """
        try:
            # Convert to int16 if it's float
            if audio_data.dtype == np.float32:
                audio_data = (audio_data * 32768).astype(np.int16)
            
            # Calculate audio energy using numpy instead of audioop
            energy = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
            energy = int(energy * 32768)  # Scale to match audioop.rms range
            
            current_time = time.time()
            
            if energy > self.energy_threshold:
                # Energy above threshold - potential speech
                if not self.is_speaking:
                    if self.speech_start_time is None:
                        self.speech_start_time = current_time
                    elif current_time - self.speech_start_time > self.speaking_threshold:
                        self.is_speaking = True
                        self.silence_start_time = None
                else:
                    self.silence_start_time = None
            else:
                # Energy below threshold - potential silence
                if self.is_speaking:
                    if self.silence_start_time is None:
                        self.silence_start_time = current_time
                    elif current_time - self.silence_start_time > self.silence_threshold:
                        self.is_speaking = False
                        self.speech_start_time = None
                else:
                    self.speech_start_time = None
            
            return self.is_speaking
            
        except Exception as e:
            print(f"VAD error: {e}")
            return False
    
    def adjust_for_ambient_noise(self, ambient_energy):
        """Adjust threshold based on ambient noise level"""
        self.energy_threshold = max(300, ambient_energy * 1.2)

class WakeWordDetector:
    """Detects wake words like 'Hey JARVIS'"""
    
    def __init__(self):
        self.wake_words = [
            "jarvis", "hey jarvis", "okay jarvis", 
            "yo jarvis", "jarvis are you there", "computer"
        ]
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.voice_activity_detector = VoiceActivityDetector()
    
    async def detect(self, audio_data: np.ndarray, format_params=None) -> Tuple[bool, str]:
        """
        Check if audio contains a wake word
        Returns: (detected, detected_phrase)
        """
        try:
            # Skip processing if no speech detected
            if not self.voice_activity_detector.detect(audio_data):
                return False, ""
                
            # Convert numpy array to AudioData
            audio_data_bytes = audio_data.tobytes()
            
            # Default format is 16kHz mono 16-bit
            if format_params is None:
                format_params = {
                    'rate': 16000,
                    'width': 2,  # 16-bit
                    'channels': 1  # mono
                }
            
            # Create an in-memory WAV file
            wav_bytes = io.BytesIO()
            with wave.open(wav_bytes, 'wb') as wav:
                wav.setframerate(format_params['rate'])
                wav.setsampwidth(format_params['width'])
                wav.setnchannels(format_params['channels'])
                wav.writeframes(audio_data_bytes)
            
            # Convert to AudioData
            wav_bytes.seek(0)
            with sr.AudioFile(wav_bytes) as source:
                audio = self.recognizer.record(source)
            
            # Try to recognize using Google (you can switch to other models)
            try:
                text = self.recognizer.recognize_google(audio).lower()
                
                # Check for wake words
                for wake_word in self.wake_words:
                    if wake_word in text:
                        return True, text
                        
                return False, text
            except sr.UnknownValueError:
                return False, ""
            except sr.RequestError:
                # If online service fails, try local fallback
                print("Wake word service error, using fallback")
                # Simple energy-based detection as fallback
                audio_np = np.frombuffer(audio_data_bytes, dtype=np.int16)
                energy = np.sqrt(np.mean(np.square(audio_np.astype(np.float32))))
                energy = int(energy * 32768)  # Scale to match audioop.rms range
                if energy > 1000:  # High energy might be a command
                    return True, "energy_trigger"
                return False, ""
                
        except Exception as e:
            print(f"Wake word detection error: {e}")
            return False, ""

class EnhancedVoiceEngine:
    """Enhanced JARVIS Voice Engine with LiveKit integration"""
    
    def __init__(self):
        # Load credentials from environment
        self.load_credentials()
        
        # Initialize AI engine
        self.ai = JarvisAI()
        
        # Voice processing components
        self.room = None
        self.audio_source = None
        self.local_audio_track = None
        self.web_audio_track = None
        
        # Audio input/output
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.sample_rate = 16000
        self.audio_buffer = []
        self.buffer_size = 10  # Buffer up to 10 seconds
        
        # TTS Engine - Primary and fallback
        self.tts_engine = pyttsx3.init()
        self.setup_tts_voices()
        
        # Enhanced voice features
        self.emotion_analyzer = EmotionAnalyzer()
        self.voice_activity_detector = VoiceActivityDetector()
        self.wake_word_detector = WakeWordDetector()
        self.voice_fingerprints = {}
        
        # Audio processing queues
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.interrupt_queue = queue.Queue()
        
        # Voice processing state
        self.is_listening = False
        self.is_speaking = False
        self.conversation_active = False
        self.continuous_mode = False
        self.interrupt_enabled = True
        self.proactive_mode = True
        self.user_emotion = "neutral"
        self.wake_words = ["jarvis", "hey jarvis", "okay jarvis", "computer"]
        
        # Conversation context
        self.conversation_buffer = []
        self.last_interaction = None
        self.conversation_timeout = 60  # seconds
        self.current_user_id = "primary_user"
        
        print("🤖 Enhanced JARVIS Voice Engine initialized")
        
    def load_credentials(self):
        """Load credentials from environment variables"""
        # Load from .env if available
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        # Get LiveKit credentials
        self.livekit_url = os.getenv("LIVEKIT_URL", "wss://jarvis-bg7u43x4.livekit.cloud")
        self.api_key = os.getenv("LIVEKIT_API_KEY", "APIBsSZnWSF7q7K")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET", "lJU8krmu6jJ9TtHeg1wE1von277ex2V7qCZBj6U5fTIB")
        
    def setup_tts_voices(self):
        """Setup TTS voices for different personalities"""
        voices = self.tts_engine.getProperty('voices')
        
        # Find the best male and female voices
        male_voice = 0
        female_voice = 0
        
        for i, voice in enumerate(voices):
            if voice.gender == 'male':
                male_voice = i
                break
                
        for i, voice in enumerate(voices):
            if voice.gender == 'female':
                female_voice = i
                break
        
        # Voice mapping for personalities
        self.personality_voices = {
            'standard': {
                'voice_id': male_voice,
                'rate': 170,
                'volume': 0.9
            },
            'professional': {
                'voice_id': male_voice,
                'rate': 155,
                'volume': 0.95
            },
            'sarcastic': {
                'voice_id': female_voice if female_voice != male_voice else male_voice,
                'rate': 190,
                'volume': 0.85
            },
            'unleashed': {
                'voice_id': male_voice,
                'rate': 210,
                'volume': 1.0
            },
            'genius': {
                'voice_id': male_voice,
                'rate': 140,
                'volume': 0.9
            },
            'urgent': {
                'voice_id': male_voice,
                'rate': 200,
                'volume': 1.0
            }
        }
    
    async def connect_to_livekit(self, room_name="jarvis-voice-room"):
        """Connect to LiveKit room - DISABLED (LiveKit not available)"""
        print("❌ LiveKit not available - using local voice mode only")
        print("💡 For premium multi-user features, use jarvis_voice_premium.py")
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
                asyncio.create_task(self.process_incoming_audio(track, participant))
        
        @self.room.on("data_received")
        def on_data_received(data: bytes, participant: rtc.RemoteParticipant):
            try:
                message = json.loads(data.decode())
                asyncio.create_task(self.handle_data_message(message, participant))
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
    
    async def process_incoming_audio(self, track: rtc.AudioTrack, participant: rtc.RemoteParticipant):
        """Process incoming audio for speech recognition"""
        try:
            audio_stream = rtc.AudioStream(track)
            
            async for frame in audio_stream:
                if self.is_listening:
                    # Convert audio frame to numpy array
                    audio_data = np.frombuffer(frame.data, dtype=np.int16)
                    
                    # Store user ID from participant
                    user_id = participant.identity
                    
                    # Add to fingerprint database if new user
                    if user_id not in self.voice_fingerprints:
                        self.voice_fingerprints[user_id] = self.extract_voice_fingerprint(audio_data)
                    
                    # Store current user
                    self.current_user_id = user_id
                    
                    # Add audio frame to buffer
                    self.audio_buffer.append((audio_data, time.time()))
                    
                    # Remove old frames to keep buffer size reasonable
                    while len(self.audio_buffer) > self.buffer_size:
                        self.audio_buffer.pop(0)
                    
                    # Voice activity detection
                    if self.voice_activity_detector.detect(audio_data):
                        # Detect emotion
                        emotion = self.emotion_analyzer.analyze(audio_data)
                        if emotion != self.user_emotion:
                            self.user_emotion = emotion
                            print(f"🔍 Detected emotion: {emotion}")
                            
                            # Send emotion status
                            await self.send_data_message({
                                "type": "emotion_update",
                                "user": user_id,
                                "emotion": emotion
                            })
                        
                        # Check for interrupt if JARVIS is speaking
                        if self.is_speaking and self.interrupt_enabled:
                            await self.check_for_interruption(audio_data)
                        
                        # Process speech
                        await self.process_speech(audio_data, user_id)
                        
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
    
    def extract_voice_fingerprint(self, audio_data):
        """Extract basic voice fingerprint for user identification"""
        try:
            # Basic fingerprint: spectral characteristics
            # In a real system, use a proper voice fingerprinting model
            if len(audio_data) > 1024:
                fft_data = np.abs(np.fft.rfft(audio_data[:1024]))
                return fft_data / np.sum(fft_data) if np.sum(fft_data) > 0 else fft_data
            return np.zeros(513)  # Half of 1024 + 1
        except Exception as e:
            print(f"Fingerprint error: {e}")
            return np.zeros(513)
    
    async def check_for_interruption(self, audio_data):
        """Check if user is trying to interrupt"""
        # Simple approach: loud audio during speech might be interruption
        # Calculate energy using numpy instead of audioop
        energy = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
        energy = int(energy * 32768)  # Scale to match audioop.rms range
        
        # If energy is very high, it might be an interruption
        if energy > 1500:  # Threshold for interruption
            self.interrupt_queue.put("interrupt")
            print("⚡ Potential interruption detected")
    
    async def process_speech(self, audio_data, user_id):
        """Process speech data for wake words and commands"""
        try:
            # Check for wake word if not in conversation mode
            if not self.conversation_active:
                wake_detected, phrase = await self.wake_word_detector.detect(audio_data)
                
                if wake_detected:
                    print(f"🔥 Wake word detected: '{phrase}'")
                    self.conversation_active = True
                    self.last_interaction = datetime.now()
                    
                    # Acknowledge wake word
                    await self.speak_response("Yes, Sir?", voice_type="standard")
                    
                    # Notify via data channel
                    await self.send_data_message({
                        "type": "wake_word_detected",
                        "user": user_id,
                        "phrase": phrase
                    })
                    
                    return
            
            # If in conversation mode, try to recognize command
            elif self.conversation_active:
                # Update last interaction time
                self.last_interaction = datetime.now()
                
                # Convert audio to proper format for recognition
                command = await self.recognize_speech(audio_data)
                
                # If command recognized, process it
                if command:
                    print(f"🎯 Command detected: '{command}'")
                    self.command_queue.put((command, user_id))
                    
                    # Notify via data channel
                    await self.send_data_message({
                        "type": "command_detected",
                        "user": user_id,
                        "command": command
                    })
                    
                    # Process the command
                    await self.process_voice_command(command)
        
        except Exception as e:
            print(f"❌ Speech processing error: {e}")
    
    async def recognize_speech(self, audio_data):
        """Recognize speech from audio data"""
        try:
            # Convert numpy array to AudioData
            audio_bytes = io.BytesIO()
            with wave.open(audio_bytes, 'wb') as wav:
                wav.setframerate(self.sample_rate)
                wav.setsampwidth(2)  # 16-bit
                wav.setnchannels(1)  # mono
                wav.writeframes(audio_data.tobytes())
            
            # Convert to AudioData
            audio_bytes.seek(0)
            with sr.AudioFile(audio_bytes) as source:
                audio = self.recognizer.record(source)
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                # Fallback to other recognition service
                print("Google Speech API unavailable, using fallback")
                return None
                
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    async def process_voice_command(self, command):
        """Process a voice command through AI engine"""
        try:
            # Skip if the command is to end conversation or turn off
            if command.lower() in ["end conversation", "stop conversation", "exit conversation"]:
                await self.speak_response("Ending conversation mode. Say JARVIS to activate me again.")
                self.conversation_active = False
                return
                
            if command.lower() in ["voice off", "turn off", "shutdown", "shut down"]:
                await self.speak_response("Deactivating voice interface. Goodbye, Sir.")
                self.is_listening = False
                return
            
            # Process command with AI
            print(f"🧠 Processing command with AI: {command}")
            
            # Get appropriate personality based on user emotion
            personality = self.get_personality_for_emotion(self.user_emotion)
            
            # Add context about current conversation
            context = ""
            if len(self.conversation_buffer) > 0:
                context = "Previous conversation: " + " ".join(self.conversation_buffer[-3:])
            
            # Get AI response
            ai_response = self.ai.chat(command, context=context)
            
            # Store in conversation buffer
            self.conversation_buffer.append(command)
            self.conversation_buffer.append(ai_response)
            
            # Keep buffer reasonable size
            while len(self.conversation_buffer) > 20:
                self.conversation_buffer.pop(0)
            
            # Speak the response
            await self.speak_response(ai_response, voice_type=personality)
            
            # Update last interaction time
            self.last_interaction = datetime.now()
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            await self.speak_response("I'm sorry, I encountered an error processing your request.")
    
    def get_personality_for_emotion(self, emotion):
        """Choose appropriate personality based on user's emotional state"""
        if emotion == "urgent":
            return "urgent"
        elif emotion == "angry":
            return "professional"
        elif emotion == "sad" or emotion == "worried":
            return "genius"
        elif emotion == "happy" or emotion == "excited":
            return "unleashed"
        else:
            return "standard"
    
    async def speak_text(self, text, voice_type="standard"):
        """Convert text to speech and output"""
        try:
            # Skip if text is empty
            if not text:
                return
                
            # Set speaking state
            self.is_speaking = True
            
            # Prepare voice settings
            voice_settings = self.personality_voices.get(voice_type, self.personality_voices["standard"])
            
            # Set voice properties
            self.tts_engine.setProperty('voice', self.tts_engine.getProperty('voices')[voice_settings['voice_id']].id)
            self.tts_engine.setProperty('rate', voice_settings['rate'])
            self.tts_engine.setProperty('volume', voice_settings['volume'])
            
            # Temperary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name
                
            # Generate speech to file
            self.tts_engine.save_to_file(text, temp_filename)
            self.tts_engine.runAndWait()
            
            # Stream file to audio output
            with wave.open(temp_filename, 'rb') as wav_file:
                framerate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                # Read audio data
                audio_data = wav_file.readframes(wav_file.getnframes())
            
            # Clean up temporary file
            try:
                os.unlink(temp_filename)
            except:
                pass
                
            # Stream audio data
            if self.audio_source:
                # Convert to LiveKit format and publish
                frames_size = int(framerate * 0.02)  # 20ms frames
                
                # Check for interruption while speaking
                for i in range(0, len(audio_data), frames_size * channels * sample_width):
                    # Check interrupt queue
                    try:
                        if not self.interrupt_queue.empty():
                            interrupt = self.interrupt_queue.get_nowait()
                            if interrupt == "interrupt":
                                print("🛑 Speech interrupted by user")
                                break
                    except:
                        pass
                        
                    # Get frame chunk
                    chunk = audio_data[i:i + frames_size * channels * sample_width]
                    if not chunk:
                        break
                    
                    # Convert to proper format if needed
                    if sample_width == 2:  # 16-bit audio
                        audio_frame = np.frombuffer(chunk, dtype=np.int16)
                    else:
                        # Convert to 16-bit using simple conversion
                        if sample_width == 4:  # 32-bit
                            audio_frame = np.frombuffer(chunk, dtype=np.int32)
                            audio_frame = (audio_frame / 65536).astype(np.int16)
                        elif sample_width == 1:  # 8-bit
                            audio_frame = np.frombuffer(chunk, dtype=np.uint8)
                            audio_frame = ((audio_frame.astype(np.int16) - 128) * 256).astype(np.int16)
                        else:
                            audio_frame = np.frombuffer(chunk, dtype=np.int16)  # Default to 16-bit
                    
                    # Push to audio source
                    self.audio_source.push_audio(audio_frame)
                    
                    # Small delay to simulate real-time speech
                    await asyncio.sleep(0.01)
            else:
                # Fallback to local playback (sounddevice)
                if sample_width == 2:  # 16-bit audio
                    audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
                else:
                    # Convert to 16-bit using simple conversion
                    if sample_width == 4:  # 32-bit
                        audio_data_np = np.frombuffer(audio_data, dtype=np.int32)
                        audio_data_np = (audio_data_np / 65536).astype(np.int16)
                    elif sample_width == 1:  # 8-bit
                        audio_data_np = np.frombuffer(audio_data, dtype=np.uint8)
                        audio_data_np = ((audio_data_np.astype(np.int16) - 128) * 256).astype(np.int16)
                    else:
                        audio_data_np = np.frombuffer(audio_data, dtype=np.int16)  # Default to 16-bit
                
                # Play audio
                sd.play(audio_data_np, framerate)
                sd.wait()
            
            # Reset speaking state
            self.is_speaking = False
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
            self.is_speaking = False
    
    async def speak_response(self, response, voice_type="standard"):
        """Process and speak AI response"""
        try:
            # Notify about speaking
            await self.send_data_message({
                "type": "jarvis_speaking",
                "text": response
            })
            
            # Speak the response
            await self.speak_text(response, voice_type)
            
            # Notify about finished speaking
            await self.send_data_message({
                "type": "jarvis_finished_speaking"
            })
            
        except Exception as e:
            print(f"❌ Response speaking error: {e}")
    
    async def send_data_message(self, message):
        """Send data message to LiveKit room"""
        try:
            if self.room:
                data = json.dumps(message).encode()
                await self.room.local_participant.publish_data(data)
        except Exception as e:
            print(f"❌ Data message error: {e}")
    
    async def handle_data_message(self, message, participant):
        """Handle incoming data messages"""
        try:
            msg_type = message.get("type")
            
            if msg_type == "user_status":
                print(f"📊 User status: {message}")
            elif msg_type == "command_request":
                command = message.get("command")
                if command:
                    await self.process_voice_command(command)
            elif msg_type == "emotion_update":
                print(f"😊 Emotion update: {message}")
            elif msg_type == "interrupt_request":
                self.interrupt_queue.put("interrupt")
                
        except Exception as e:
            print(f"❌ Data message handling error: {e}")
    
    async def listen_for_wake_word(self, timeout=None):
        """Listen for wake word activation"""
        try:
            print("👂 Listening for wake word...")
            
            # Set up timeout
            start_time = time.time()
            
            # Use microphone for local testing
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                while True:
                    # Check timeout
                    if timeout and (time.time() - start_time) > timeout:
                        return False
                    
                    try:
                        print("🔊 Say 'Hey JARVIS'...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                        
                        # Try to recognize wake word
                        try:
                            text = self.recognizer.recognize_google(audio).lower()
                            print(f"🎤 Heard: '{text}'")
                            
                            # Check for wake words
                            for wake_word in self.wake_words:
                                if wake_word in text:
                                    print(f"🔥 Wake word detected!")
                                    return True
                                    
                        except sr.UnknownValueError:
                            # No speech detected
                            pass
                        except sr.RequestError:
                            print("🔌 API unavailable, using local detection")
                            # Fall back to energy detection
                            audio_raw = audio.get_raw_data()
                            audio_np = np.frombuffer(audio_raw, dtype=np.int16)
                            energy = np.sqrt(np.mean(np.square(audio_np.astype(np.float32))))
                            energy = int(energy * 32768)  # Scale to match audioop.rms range
                            if energy > 1000:  # High energy might be a command
                                return True
                            
                    except sr.WaitTimeoutError:
                        # Timeout waiting for speech
                        pass
                        
                    # Brief pause to prevent CPU hammering
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ Wake word listening error: {e}")
            return False
    
    async def listen_for_command(self, timeout=5):
        """Listen for a command after wake word"""
        try:
            print("🎤 Listening for command...")
            
            # Use microphone for local testing
            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                    
                    # Try to recognize command
                    try:
                        text = self.recognizer.recognize_google(audio)
                        return text
                    except sr.UnknownValueError:
                        print("❓ Could not understand command")
                        return None
                    except sr.RequestError:
                        print("🔌 API unavailable")
                        return None
                        
                except sr.WaitTimeoutError:
                    print("⏰ Command timeout")
                    return None
                    
        except Exception as e:
            print(f"❌ Command listening error: {e}")
            return None
    
    async def start_listening(self):
        """Start voice recognition"""
        try:
            self.is_listening = True
            print("🎤 Voice recognition started - Say 'JARVIS' to activate")
            
            # Calibrate microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Get ambient noise level and adjust VAD
                energy = self.recognizer.energy_threshold
                self.voice_activity_detector.adjust_for_ambient_noise(energy)
            
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
    
    async def enable_continuous_mode(self, timeout=60):
        """Enable continuous conversation without wake word"""
        self.continuous_mode = True
        self.conversation_timeout = timeout
        print(f"🔄 Continuous conversation mode enabled (timeout: {timeout}s)")
        
    async def disable_continuous_mode(self):
        """Disable continuous conversation mode"""
        self.continuous_mode = False
        print("🛑 Continuous conversation mode disabled")
    
    async def enable_proactive_mode(self):
        """Enable proactive interruptions"""
        self.proactive_mode = True
        print("💡 Proactive assistance mode enabled")
        
    async def disable_proactive_mode(self):
        """Disable proactive interruptions"""
        self.proactive_mode = False
        print("🛑 Proactive assistance mode disabled")
    
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
    print("🔥 Starting Enhanced JARVIS Voice Interface...")
    
    try:
        # Initialize voice engine
        voice_engine = EnhancedVoiceEngine()
        
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
                    (datetime.now() - voice_engine.last_interaction).seconds > voice_engine.conversation_timeout):
                    
                    voice_engine.conversation_active = False
                    await voice_engine.speak_response("Conversation timeout. Say JARVIS to reactivate.")
                
        except KeyboardInterrupt:
            print("\n👋 Shutting down JARVIS Voice Interface...")
            
    except Exception as e:
        print(f"❌ Voice interface error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if 'voice_engine' in locals():
            await voice_engine.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
