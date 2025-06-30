#!/usr/bin/env python3
"""
JARVIS-X PREMIUM Voice Engine
High-Quality Voice Assistant with Natural Speech
- Azure Cognitive Services (premium TTS)
- Google Cloud Speech (premium STT)  
- Edge TTS (natural voices)
- Advanced voice processing
"""

import os
import sys
import time
import asyncio
import threading
import json
import tempfile
import wave
import io
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import numpy as np
from dotenv import load_dotenv

# Advanced TTS imports
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts not available - using basic TTS")

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_TTS_AVAILABLE = True
except ImportError:
    AZURE_TTS_AVAILABLE = False
    print("⚠️ Azure Speech SDK not available - using alternative TTS")

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

# Load environment
load_dotenv()

class PremiumVoiceEngine:
    """Premium voice engine with natural, human-like speech"""
    
    def __init__(self):
        """Initialize premium voice engine"""
        print("🔥 Initializing JARVIS-X Premium Voice Engine...")
        
        # AI Engine
        self.ai = JarvisAI()
        
        # Voice settings
        self.voice_active = False
        self.listening = False
        self.speaking = False
        self.conversation_active = False
        
        # Wake words (more natural variations)
        self.wake_words = [
            "jarvis", "hey jarvis", "jarvis x", "ok jarvis", 
            "computer", "assistant", "ai", "hey ai"
        ]
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.setup_microphone()
        
        # TTS setup (multiple engines for quality)
        self.tts_engines = {}
        self.setup_premium_tts()
        
        # Voice processing settings
        self.recognition_timeout = 3
        self.phrase_timeout = 8
        self.energy_threshold = 300
        
        print("✅ Premium Voice Engine Ready!")
        print("🎤 Available wake words:", ", ".join(self.wake_words))
    
    def setup_microphone(self):
        """Setup microphone with optimal settings"""
        try:
            # Find the best microphone
            mics = sr.Microphone.list_microphone_names()
            print(f"🎤 Available microphones: {len(mics)}")
            
            # Use default microphone with optimal settings
            self.microphone = sr.Microphone(sample_rate=16000, chunk_size=1024)
            
            # Calibrate for ambient noise
            with self.microphone as source:
                print("🔧 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                self.energy_threshold = self.recognizer.energy_threshold
                print(f"✅ Energy threshold set to: {self.energy_threshold}")
                
        except Exception as e:
            print(f"❌ Microphone setup error: {e}")
            self.microphone = sr.Microphone()  # Fallback to default
    
    def setup_premium_tts(self):
        """Setup multiple TTS engines for best quality"""
        
        # 1. Edge TTS (Microsoft - Most Natural)
        if EDGE_TTS_AVAILABLE:
            self.tts_engines['edge'] = {
                'type': 'edge',
                'voices': {
                    'male': 'en-US-DavisNeural',      # Professional male
                    'male_casual': 'en-US-JasonNeural', # Casual male  
                    'british': 'en-GB-RyanNeural',    # British accent
                    'deep': 'en-US-GuyNeural',        # Deep voice
                }
            }
            print("✅ Edge TTS (Microsoft) - Premium voices available")
        
        # 2. Azure Cognitive Services (Enterprise grade)
        if AZURE_TTS_AVAILABLE:
            azure_key = os.getenv('AZURE_SPEECH_KEY')
            azure_region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
            
            if azure_key:
                self.tts_engines['azure'] = {
                    'type': 'azure',
                    'key': azure_key,
                    'region': azure_region,
                    'voices': {
                        'neural': 'en-US-JennyNeural',
                        'male': 'en-US-GuyNeural', 
                        'british': 'en-GB-RyanNeural'
                    }
                }
                print("✅ Azure TTS - Enterprise voices available")
        
        # 3. System TTS (Fallback)
        self.tts_engines['system'] = {
            'type': 'system',
            'engine': pyttsx3.init()
        }
        
        # Configure system TTS with best settings
        sys_engine = self.tts_engines['system']['engine']
        voices = sys_engine.getProperty('voices')
        
        # Find best voice (prefer male, high quality)
        best_voice = None
        for voice in voices:
            if 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                best_voice = voice
                break
            elif voice.gender and 'male' in str(voice.gender).lower():
                best_voice = voice
        
        if best_voice:
            sys_engine.setProperty('voice', best_voice.id)
        
        # Optimize speech settings
        sys_engine.setProperty('rate', 165)  # Slightly slower for clarity
        sys_engine.setProperty('volume', 0.95)
        
        print("✅ System TTS configured")
        print(f"🔊 Primary TTS: {'Edge TTS' if EDGE_TTS_AVAILABLE else 'System TTS'}")
    
    async def speak_edge_tts(self, text, voice='en-US-DavisNeural'):
        """Use Edge TTS for natural speech"""
        try:
            # Create TTS request
            communicate = edge_tts.Communicate(text, voice)
            
            # Generate audio to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            await communicate.save(tmp_path)
            
            # Play the audio file
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # Cleanup
            pygame.mixer.quit()
            os.unlink(tmp_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return False
    
    def speak_system_tts(self, text):
        """Use system TTS as fallback"""
        try:
            engine = self.tts_engines['system']['engine']
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ System TTS error: {e}")
            return False
    
    async def speak(self, text, voice_type='male'):
        """Speak text using the best available TTS"""
        if not text.strip():
            return
        
        self.speaking = True
        print(f"🤖 JARVIS: {text}")
        
        try:
            # Try Edge TTS first (best quality)
            if EDGE_TTS_AVAILABLE and 'edge' in self.tts_engines:
                voice_map = self.tts_engines['edge']['voices']
                voice = voice_map.get(voice_type, voice_map['male'])
                
                if await self.speak_edge_tts(text, voice):
                    self.speaking = False
                    return
            
            # Fallback to system TTS
            if self.speak_system_tts(text):
                self.speaking = False
                return
            
            # Last resort - just print
            print(f"🤖 JARVIS (text only): {text}")
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            print(f"🤖 JARVIS (text only): {text}")
        finally:
            self.speaking = False
    
    def listen_for_speech(self, timeout=5, phrase_timeout=8):
        """Advanced speech recognition with multiple engines"""
        try:
            with self.microphone as source:
                # Dynamic noise adjustment
                if not hasattr(self, '_noise_adjusted'):
                    print("🔧 Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    self._noise_adjusted = True
                
                # Listen with optimized settings
                print("🎤 Listening...")
                self.recognizer.energy_threshold = max(self.energy_threshold, 200)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_damping = 0.15
                self.recognizer.dynamic_energy_ratio = 1.5
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
                
                # Try multiple recognition engines
                return self.recognize_speech_multiple_engines(audio)
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return None
    
    def recognize_speech_multiple_engines(self, audio):
        """Try multiple speech recognition engines for best accuracy"""
        engines = [
            ('google', lambda: self.recognizer.recognize_google(audio)),
            ('google_cloud', lambda: self.recognizer.recognize_google_cloud(audio) if hasattr(self.recognizer, 'recognize_google_cloud') else None),
            ('sphinx', lambda: self.recognizer.recognize_sphinx(audio)),
        ]
        
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
                return "How can I help you?"
            
            # Check for system commands first
            if any(cmd in command for cmd in ["stop listening", "pause", "quiet", "shut up"]):
                self.conversation_active = False
                return "Voice interaction paused. Say my name to reactivate."
            
            if any(cmd in command for cmd in ["goodbye", "exit", "shut down", "turn off"]):
                self.voice_active = False
                return "JARVIS voice system shutting down. Goodbye, Sir."
            
            # Process with AI
            print(f"🧠 Processing: {command}")
            response = self.ai.chat(command)
            
            # Make response more conversational
            if len(response) > 200:
                # Shorten long responses for voice
                sentences = response.split('. ')
                if len(sentences) > 2:
                    response = '. '.join(sentences[:2]) + "."
                    response += " Would you like me to elaborate?"
            
            return response
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            return "I encountered an error processing your request. Please try again."
    
    async def voice_interaction_loop(self):
        """Main voice interaction loop"""
        await self.speak("JARVIS Premium voice system online. I'm ready to assist you, Sir.", 'male')
        
        self.voice_active = True
        
        while self.voice_active:
            try:
                # Listen for wake word or command
                if not self.conversation_active:
                    # Listen for wake word (shorter timeout)
                    text = self.listen_for_speech(timeout=2, phrase_timeout=4)
                    
                    if text and self.is_wake_word(text):
                        self.conversation_active = True
                        await self.speak("Yes, Sir?", 'male')
                        continue
                
                else:
                    # In conversation mode - listen for commands
                    text = self.listen_for_speech(timeout=5, phrase_timeout=10)
                    
                    if text:
                        # Process command
                        response = await self.process_command(text)
                        await self.speak(response, 'male')
                        
                        # Continue conversation
                        await self.speak("Anything else?", 'male')
                    else:
                        # No speech detected - end conversation after timeout
                        await self.speak("I'm here when you need me.", 'male')
                        self.conversation_active = False
                
                # Brief pause to prevent CPU hammering
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                await asyncio.sleep(1)
        
        await self.speak("JARVIS voice system shutting down. Goodbye, Sir.", 'male')
    
    async def test_voice_system(self):
        """Test all voice components"""
        print("\n🔧 Testing Premium Voice System...")
        
        # Test TTS
        await self.speak("Premium voice test initiated. Testing text to speech quality.", 'male')
        await asyncio.sleep(1)
        
        # Test different voices if available
        if EDGE_TTS_AVAILABLE:
            await self.speak("This is the professional voice mode.", 'male')
            await self.speak("And this is the casual voice mode.", 'male_casual')
            await self.speak("British accent is also available.", 'british')
        
        # Test microphone
        await self.speak("Now testing microphone. Please say something.", 'male')
        text = self.listen_for_speech(timeout=8, phrase_timeout=10)
        
        if text:
            await self.speak(f"Perfect! I heard you say: {text}", 'male')
        else:
            await self.speak("No speech detected. Please check your microphone.", 'male')
        
        await self.speak("Voice system test complete!", 'male')

async def main():
    """Main function"""
    print("🔥 JARVIS-X Premium Voice Engine")
    print("=" * 50)
    
    # Install required packages if missing
    try:
        import pygame
    except ImportError:
        print("📦 Installing pygame for audio playback...")
        os.system("pip install pygame")
        import pygame
    
    try:
        import edge_tts
    except ImportError:
        print("📦 Installing edge-tts for premium voices...")
        os.system("pip install edge-tts")
    
    # Initialize voice engine
    voice = PremiumVoiceEngine()
    
    print("\n🎯 Select mode:")
    print("1. Full voice interaction")
    print("2. Voice system test")
    print("3. Single command test")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await voice.voice_interaction_loop()
        elif choice == "2":
            await voice.test_voice_system()
        elif choice == "3":
            await voice.speak("What would you like me to do?", 'male')
            text = voice.listen_for_speech(timeout=10, phrase_timeout=8)
            if text:
                response = await voice.process_command(text)
                await voice.speak(response, 'male')
            else:
                await voice.speak("I didn't hear anything.", 'male')
        else:
            await voice.voice_interaction_loop()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
