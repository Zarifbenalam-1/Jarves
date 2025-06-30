#!/usr/bin/env python3
"""
JARVIS-X LiveKit Voice Engine
Premium Voice Assistant using LiveKit API
- Real-time voice communication
- High-quality audio processing
- Multi-user support
- Professional voice synthesis
"""

import os
import sys
import asyncio
import json
import logging
import wave
import io
import tempfile
import time
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import requests
import numpy as np
from dotenv import load_dotenv

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiveKitVoiceEngine:
    """LiveKit-powered voice engine for premium voice experience"""
    
    def __init__(self):
        """Initialize LiveKit voice engine"""
        print("🔥 Initializing JARVIS-X LiveKit Voice Engine...")
        
        # Load LiveKit credentials
        self.livekit_url = os.getenv("LIVEKIT_URL", "wss://jarvis-bg7u43x4.livekit.cloud")
        self.api_key = os.getenv("LIVEKIT_API_KEY", "APIBsSZnWSF7q7K")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET", "lJU8krmu6jJ9TtHeg1wE1von277ex2V7qCZBj6U5fTIB")
        
        # Validate credentials
        if not all([self.livekit_url, self.api_key, self.api_secret]):
            raise ValueError("❌ LiveKit credentials missing in .env file")
        
        print(f"✅ LiveKit URL: {self.livekit_url}")
        print(f"✅ API Key: {self.api_key[:10]}...")
        
        # AI Engine
        self.ai = JarvisAI()
        
        # Voice settings
        self.voice_active = False
        self.listening = False
        self.speaking = False
        self.conversation_active = False
        self.room_name = "jarvis-voice-room"
        
        # Wake words
        self.wake_words = [
            "jarvis", "hey jarvis", "jarvis x", "ok jarvis", 
            "computer", "assistant", "ai", "hey ai"
        ]
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.setup_microphone()
        
        # TTS setup with multiple engines
        self.tts_engines = {}
        self.setup_tts_engines()
        self.setup_premium_voice_settings()
        
        # Enhanced audio quality
        self.enhance_audio_quality()
        
        # LiveKit connection
        self.room = None
        self.participants = {}
        
        print("✅ LiveKit Voice Engine Ready!")
        
    def setup_microphone(self):
        """Setup microphone with optimal settings"""
        try:
            # Get available microphones
            mics = sr.Microphone.list_microphone_names()
            print(f"🎤 Available microphones: {len(mics)}")
            
            # Use default microphone with high-quality settings
            self.microphone = sr.Microphone(sample_rate=48000, chunk_size=4096)
            
            # Calibrate for ambient noise
            with self.microphone as source:
                print("🔧 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print(f"✅ Energy threshold: {self.recognizer.energy_threshold}")
                
        except Exception as e:
            print(f"❌ Microphone setup error: {e}")
            self.microphone = sr.Microphone()  # Fallback
    
    def setup_tts_engines(self):
        """Setup multiple TTS engines for best quality"""
        
        # 1. System TTS (Fallback)
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Find best voice
            best_voice = None
            for voice in voices:
                if any(name in voice.name.lower() for name in ['david', 'mark', 'zira', 'hazel']):
                    best_voice = voice
                    break
                elif voice.gender and 'male' in str(voice.gender).lower():
                    best_voice = voice
            
            if best_voice:
                engine.setProperty('voice', best_voice.id)
                print(f"✅ Selected voice: {best_voice.name}")
            
            # Optimize for clarity and naturalness
            engine.setProperty('rate', 160)  # Slightly slower for clarity
            engine.setProperty('volume', 0.95)
            
            self.tts_engines['system'] = engine
            
        except Exception as e:
            print(f"❌ System TTS error: {e}")
        
        # 2. Try to use Edge TTS if available
        try:
            import edge_tts
            self.tts_engines['edge'] = {
                'available': True,
                'voices': {
                    'male_professional': 'en-US-DavisNeural',
                    'male_casual': 'en-US-JasonNeural',
                    'male_deep': 'en-US-GuyNeural',
                    'british_male': 'en-GB-RyanNeural',
                    'female_professional': 'en-US-JennyNeural'
                }
            }
            print("✅ Edge TTS (Microsoft) available - Premium voices enabled")
        except ImportError:
            print("⚠️ Edge TTS not available - using system TTS")
            self.tts_engines['edge'] = {'available': False}
        
        print(f"🔊 TTS Engines configured: {list(self.tts_engines.keys())}")
    
    def generate_livekit_token(self, identity="jarvis-ai", room_name=None):
        """Generate LiveKit access token"""
        if not room_name:
            room_name = self.room_name
            
        # Create token payload
        payload = {
            "iss": self.api_key,
            "sub": identity,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,  # 1 hour expiry
            "video": {
                "room": room_name,
                "roomJoin": True,
                "canPublish": True,
                "canSubscribe": True,
                "canPublishData": True
            }
        }
        
        # For simplicity, we'll use a basic token - in production use proper JWT
        import base64
        import hmac
        import hashlib
        
        # Create signature
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        signature = hmac.new(
            self.api_secret.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        token = f"{header_b64}.{payload_b64}.{signature_b64}"
        return token
    
    async def connect_to_livekit(self):
        """Connect to LiveKit room using REST API"""
        try:
            print(f"🔗 Connecting to LiveKit room: {self.room_name}")
            
            # Generate access token
            token = self.generate_livekit_token()
            
            # Create room using REST API
            room_url = f"{self.livekit_url.replace('wss://', 'https://').replace('ws://', 'http://')}/twirp/livekit.RoomService/CreateRoom"
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'name': self.room_name,
                'max_participants': 10,
                'empty_timeout': 300,  # 5 minutes
                'metadata': json.dumps({
                    'type': 'jarvis-voice-room',
                    'created_by': 'jarvis-ai',
                    'features': ['voice', 'ai_assistant']
                })
            }
            
            # Use requests for HTTP API calls
            response = requests.post(room_url, headers=headers, json=data)
            
            if response.status_code in [200, 409]:  # 200 = created, 409 = already exists
                print("✅ LiveKit room ready!")
                self.room = {'name': self.room_name, 'token': token}
                return True
            else:
                print(f"❌ Room creation failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LiveKit connection error: {e}")
            return False
    
    async def speak_edge_tts(self, text, voice='en-US-DavisNeural'):
        """Use Edge TTS for natural speech"""
        try:
            if not self.tts_engines.get('edge', {}).get('available'):
                return False
                
            import edge_tts
            
            # Validate text
            if not text or len(text.strip()) == 0:
                return False
            
            # Clean text for TTS
            text = text.strip()
            if len(text) > 500:  # Limit text length
                text = text[:500] + "..."
            
            # Create TTS request with error handling
            communicate = edge_tts.Communicate(text, voice)
            
            # Generate audio to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            # Save with error handling
            try:
                await communicate.save(tmp_path)
            except Exception as save_error:
                print(f"❌ Edge TTS save error: {save_error}")
                os.unlink(tmp_path)
                return False
            
            # Check if file was created and has content
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                print("❌ Edge TTS generated empty audio file")
                return False
            
            # Play the audio file
            try:
                import pygame
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                
                pygame.mixer.quit()
                
            except ImportError:
                print("⚠️ pygame not available - using system audio")
                return False
            except Exception as play_error:
                print(f"❌ Audio playback error: {play_error}")
                return False
            
            # Cleanup
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return False
    
    def speak_system_tts(self, text):
        """Use system TTS"""
        try:
            if 'system' not in self.tts_engines:
                return False
                
            engine = self.tts_engines['system']
            engine.say(text)
            engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"❌ System TTS error: {e}")
            return False
    
    async def speak(self, text, voice_type='male_professional'):
        """Speak text using the best available TTS"""
        if not text.strip():
            return
        
        self.speaking = True
        print(f"🤖 JARVIS: {text}")
        
        try:
            # Try Edge TTS first (premium quality)
            if self.tts_engines.get('edge', {}).get('available'):
                voices = self.tts_engines['edge']['voices']
                voice = voices.get(voice_type, voices['male_professional'])
                
                if await self.speak_edge_tts(text, voice):
                    return
                else:
                    print("⚠️ Edge TTS failed, falling back to system TTS")
            
            # Fallback to system TTS
            if self.speak_system_tts(text):
                return
            
            # Last resort - text only
            print(f"🤖 JARVIS (text only): {text}")
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            print(f"🤖 JARVIS (text only): {text}")
        finally:
            self.speaking = False
    
    def listen_for_speech(self, timeout=5, phrase_timeout=8):
        """High-quality speech recognition"""
        try:
            with self.microphone as source:
                # Dynamic noise adjustment
                if not hasattr(self, '_noise_calibrated'):
                    print("🔧 Performing noise calibration...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    self._noise_calibrated = True
                
                # Optimize recognition settings
                print("🎤 Listening...")
                self.recognizer.energy_threshold = max(self.recognizer.energy_threshold, 300)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_damping = 0.15
                self.recognizer.dynamic_energy_ratio = 1.5
                self.recognizer.pause_threshold = 0.8  # Slightly longer pause threshold
                
                # Listen with high quality settings
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
                
                # Try multiple recognition engines for best accuracy
                return self.recognize_speech_advanced(audio)
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return None
    
    def recognize_speech_advanced(self, audio):
        """Advanced speech recognition with multiple engines"""
        engines = [
            ('google', lambda: self.recognizer.recognize_google(audio, language='en-US')),
            ('sphinx', lambda: self.recognizer.recognize_sphinx(audio)),
        ]
        
        # Try Google Cloud if available
        google_cloud_key = os.getenv('GOOGLE_CLOUD_API_KEY')
        if google_cloud_key:
            engines.insert(1, ('google_cloud', lambda: self.recognizer.recognize_google_cloud(audio, credentials_json=google_cloud_key)))
        
        for engine_name, recognize_func in engines:
            try:
                result = recognize_func()
                if result:
                    print(f"✅ [{engine_name}] Recognized: {result}")
                    return result.lower().strip()
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"⚠️ {engine_name} unavailable: {e}")
                continue
            except Exception as e:
                print(f"⚠️ {engine_name} error: {e}")
                continue
        
        print("❓ Could not understand speech")
        return None
    
    def is_wake_word(self, text):
        """Check if text contains wake word"""
        if not text:
            return False
        
        text = text.lower().strip()
        return any(wake_word in text for wake_word in self.wake_words)
    
    def remove_wake_word(self, text):
        """Remove wake word from command"""
        if not text:
            return ""
        
        text = text.lower().strip()
        for wake_word in self.wake_words:
            if text.startswith(wake_word):
                text = text[len(wake_word):].strip()
                break
            elif wake_word in text:
                text = text.replace(wake_word, "").strip()
        
        return text
    
    async def process_command(self, command):
        """Process voice command with AI"""
        try:
            # Clean command
            command = self.remove_wake_word(command)
            if not command:
                return "How can I help you, Sir?"
            
            # Check for system commands
            if any(cmd in command for cmd in ["stop listening", "pause", "quiet"]):
                self.conversation_active = False
                return "Voice interaction paused. Say my name to reactivate."
            
            if any(cmd in command for cmd in ["goodbye", "exit", "shut down", "turn off"]):
                self.voice_active = False
                return "JARVIS voice system shutting down. Goodbye, Sir."
            
            # Process with AI
            print(f"🧠 Processing: {command}")
            response = self.ai.chat(command)
            
            # Optimize response for voice
            if len(response) > 250:
                sentences = response.split('. ')
                if len(sentences) > 3:
                    response = '. '.join(sentences[:3]) + "."
                    response += " Would you like me to continue?"
            
            return response
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            return "I encountered an error processing your request. Please try again."
    
    async def voice_interaction_loop(self):
        """Main voice interaction loop"""
        # Connect to LiveKit
        if not await self.connect_to_livekit():
            print("❌ Failed to connect to LiveKit - running in local mode")
        
        await self.speak("JARVIS LiveKit voice system online. I'm ready to assist you, Sir.", 'male_professional')
        
        self.voice_active = True
        
        while self.voice_active:
            try:
                # Listen for wake word or command
                if not self.conversation_active:
                    # Listen for wake word (shorter timeout)
                    text = self.listen_for_speech(timeout=3, phrase_timeout=5)
                    
                    if text and self.is_wake_word(text):
                        self.conversation_active = True
                        await self.speak("Yes, Sir? How may I assist you?", 'male_professional')
                        continue
                
                else:
                    # In conversation mode - listen for commands
                    text = self.listen_for_speech(timeout=8, phrase_timeout=12)
                    
                    if text:
                        # Process command
                        response = await self.process_command(text)
                        await self.speak(response, 'male_professional')
                        
                        # Continue conversation
                        await self.speak("Is there anything else I can help you with?", 'male_professional')
                    else:
                        # No speech detected - end conversation
                        await self.speak("I'm here whenever you need me, Sir.", 'male_professional')
                        self.conversation_active = False
                
                # Brief pause
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                await asyncio.sleep(1)
        
        await self.speak("JARVIS LiveKit voice system shutting down. Goodbye, Sir.", 'male_professional')
    
    async def test_voice_system(self):
        """Test all voice components"""
        print("\n🔧 Testing LiveKit Voice System...")
        
        # Test LiveKit connection
        if await self.connect_to_livekit():
            print("✅ LiveKit connection successful")
        else:
            print("⚠️ LiveKit connection failed - using local mode")
        
        # Test TTS
        await self.speak("LiveKit voice test initiated. Testing professional voice quality.", 'male_professional')
        await asyncio.sleep(1)
        
        # Test different voices if available
        if self.tts_engines.get('edge', {}).get('available'):
            await self.speak("This is the professional voice.", 'male_professional')
            await asyncio.sleep(0.5)
            await self.speak("This is the casual voice.", 'male_casual')
            await asyncio.sleep(0.5)
            await self.speak("And this is the deep voice.", 'male_deep')
        
        # Test microphone
        await self.speak("Now testing microphone. Please say something.", 'male_professional')
        text = self.listen_for_speech(timeout=10, phrase_timeout=8)
        
        if text:
            await self.speak(f"Excellent! I heard you say: {text}", 'male_professional')
        else:
            await self.speak("No speech detected. Please check your microphone.", 'male_professional')
        
        await self.speak("LiveKit voice system test complete!", 'male_professional')
    
    def enhance_audio_quality(self):
        """Configure advanced audio settings for premium quality"""
        try:
            # Enhanced recognition settings
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.pause_threshold = 0.8
            self.recognizer.operation_timeout = None
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            print("✅ Advanced audio quality settings applied")
            
        except Exception as e:
            print(f"⚠️ Audio enhancement warning: {e}")
    
    def setup_premium_voice_settings(self):
        """Setup premium voice synthesis settings"""
        if 'system' in self.tts_engines:
            engine = self.tts_engines['system']
            
            # Advanced voice settings for clarity and naturalness
            try:
                # Slower rate for clarity
                engine.setProperty('rate', 155)
                
                # Optimal volume
                engine.setProperty('volume', 0.95)
                
                # Try to set voice quality if supported
                voices = engine.getProperty('voices')
                
                # Prioritize high-quality voices
                premium_voices = ['david', 'mark', 'zira', 'hazel', 'microsoft']
                best_voice = None
                
                for voice in voices:
                    voice_name = voice.name.lower()
                    for premium in premium_voices:
                        if premium in voice_name:
                            best_voice = voice
                            break
                    if best_voice:
                        break
                
                if best_voice:
                    engine.setProperty('voice', best_voice.id)
                    print(f"🎭 Premium voice selected: {best_voice.name}")
                
            except Exception as e:
                print(f"⚠️ Voice setup warning: {e}")

    # ...existing code...
    
async def main():
    """Main function"""
    print("🔥 JARVIS-X LiveKit Voice Engine")
    print("=" * 50)
    
    # Install required packages if missing
    try:
        import pygame
    except ImportError:
        print("📦 Installing pygame...")
        os.system(f"{sys.executable} -m pip install pygame")
    
    try:
        import edge_tts
    except ImportError:
        print("📦 Installing edge-tts...")
        os.system(f"{sys.executable} -m pip install edge-tts")
    
    try:
        # Initialize voice engine
        voice = LiveKitVoiceEngine()
        
        print("\n🎯 Select mode:")
        print("1. Full voice interaction (with LiveKit)")
        print("2. Voice system test")
        print("3. Single command test")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await voice.voice_interaction_loop()
        elif choice == "2":
            await voice.test_voice_system()
        elif choice == "3":
            await voice.speak("What would you like me to do?", 'male_professional')
            text = voice.listen_for_speech(timeout=10, phrase_timeout=8)
            if text:
                response = await voice.process_command(text)
                await voice.speak(response, 'male_professional')
            else:
                await voice.speak("I didn't hear anything.", 'male_professional')
        else:
            await voice.voice_interaction_loop()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
