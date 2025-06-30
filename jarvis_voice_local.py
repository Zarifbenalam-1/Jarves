"""
JARVIS LOCAL VOICE ENGINE
Direct voice interaction without LiveKit dependency
Perfect for local Iron Man experience
"""

import asyncio
import os
import sys
import time
from datetime import datetime
import threading
import queue

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Core imports that should always work
try:
    import speech_recognition as sr
    import pyttsx3
    import numpy as np
    HAS_VOICE = True
except ImportError as e:
    print(f"❌ Voice dependencies missing: {e}")
    HAS_VOICE = False

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from assistant.ai_engine import JarvisAI

class JarvisLocalVoiceEngine:
    """Local JARVIS Voice Engine - Works without internet dependencies"""
    
    def __init__(self):
        print("🔥 Initializing JARVIS Local Voice Engine...")
        
        # Initialize AI engine
        self.ai = JarvisAI()
        
        # Voice components
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        
        # Voice state
        self.is_listening = False
        self.is_speaking = False
        self.conversation_active = False
        self.wake_words = ["jarvis", "hey jarvis", "okay jarvis", "computer"]
        
        # Conversation context
        self.conversation_buffer = []
        self.last_interaction = None
        
        # Initialize components
        self.setup_microphone()
        self.setup_tts()
        
        print("✅ JARVIS Local Voice Engine initialized")
        
    def setup_microphone(self):
        """Setup microphone for speech recognition"""
        try:
            # List available microphones
            mic_list = sr.Microphone.list_microphone_names()
            print(f"🎤 Found {len(mic_list)} microphones")
            
            if mic_list:
                print(f"🎙️ Using: {mic_list[0]}")
                self.microphone = sr.Microphone()
                
                # Calibrate for ambient noise
                with self.microphone as source:
                    print("🔧 Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print(f"✅ Energy threshold: {self.recognizer.energy_threshold}")
                    
                return True
            else:
                print("❌ No microphones found")
                return False
                
        except Exception as e:
            print(f"❌ Microphone setup error: {e}")
            return False
    
    def setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            print(f"🗣️ Found {len(voices)} TTS voices")
            
            # Configure voice settings
            if voices:
                # Prefer male voice for JARVIS
                male_voice = None
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        male_voice = voice
                        break
                
                if male_voice:
                    self.tts_engine.setProperty('voice', male_voice.id)
                    print(f"🎵 Using voice: {male_voice.name}")
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
                    print(f"🎵 Using voice: {voices[0].name}")
            
            # Set speech parameters
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            
            return True
            
        except Exception as e:
            print(f"❌ TTS setup error: {e}")
            return False
    
    def speak(self, text, interrupt_check=True):
        """Speak text using TTS"""
        try:
            if not self.tts_engine or not text:
                return
                
            print(f"🗣️ JARVIS: {text}")
            
            self.is_speaking = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_speaking = False
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            self.is_speaking = False
    
    def listen_for_wake_word(self, timeout=10):
        """Listen for wake word like 'Hey JARVIS'"""
        try:
            if not self.microphone:
                print("❌ No microphone available")
                return False
                
            print("👂 Listening for wake word... Say 'Hey JARVIS'")
            
            with self.microphone as source:
                # Listen for audio
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                    
                    # Try to recognize speech
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US').lower()
                        print(f"🎤 Heard: '{text}'")
                        
                        # Check for wake words
                        for wake_word in self.wake_words:
                            if wake_word in text:
                                print(f"🔥 Wake word '{wake_word}' detected!")
                                return True
                                
                        return False
                        
                    except sr.UnknownValueError:
                        print("❓ Could not understand audio")
                        return False
                    except sr.RequestError as e:
                        print(f"🔌 Recognition service error: {e}")
                        return False
                        
                except sr.WaitTimeoutError:
                    print("⏰ Wake word timeout")
                    return False
                    
        except Exception as e:
            print(f"❌ Wake word error: {e}")
            return False
    
    def listen_for_command(self, timeout=10):
        """Listen for a command after wake word"""
        try:
            if not self.microphone:
                print("❌ No microphone available")
                return None
                
            print("🎤 Listening for command...")
            
            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                    
                    # Try to recognize command
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        print(f"📝 Command: '{text}'")
                        return text
                        
                    except sr.UnknownValueError:
                        print("❓ Could not understand command")
                        return None
                    except sr.RequestError as e:
                        print(f"🔌 Recognition service error: {e}")
                        return None
                        
                except sr.WaitTimeoutError:
                    print("⏰ Command timeout")
                    return None
                    
        except Exception as e:
            print(f"❌ Command listening error: {e}")
            return None
    
    def process_command(self, command):
        """Process voice command with AI"""
        try:
            # Handle special commands
            if command.lower() in ["stop", "exit", "goodbye", "shut down"]:
                self.speak("Goodbye, Sir. JARVIS signing off.")
                return False
                
            if command.lower() in ["stop listening", "voice off"]:
                self.speak("Voice interface deactivated.")
                return False
            
            # Process with AI
            print(f"🧠 Processing with AI...")
            response = self.ai.chat(command)
            
            # Store in conversation buffer
            self.conversation_buffer.append(f"User: {command}")
            self.conversation_buffer.append(f"JARVIS: {response}")
            
            # Keep buffer reasonable size
            while len(self.conversation_buffer) > 10:
                self.conversation_buffer.pop(0)
            
            # Speak response
            self.speak(response)
            
            return True
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            self.speak("I apologize, Sir. I encountered an error processing your request.")
            return True
    
    def run_voice_loop(self):
        """Main voice interaction loop"""
        print("\n🔥 JARVIS Voice Interface Active!")
        print("=" * 50)
        print("💬 Say 'Hey JARVIS' or 'JARVIS' to activate")
        print("💬 Say 'stop' or 'exit' to quit")
        print("💬 Press Ctrl+C to force exit")
        
        # Initial greeting
        self.speak("JARVIS voice interface online. Ready for your commands, Sir.")
        
        try:
            while True:
                # Listen for wake word
                wake_detected = self.listen_for_wake_word(timeout=30)
                
                if wake_detected:
                    # Acknowledge wake word
                    self.speak("Yes, Sir?")
                    
                    # Listen for command
                    command = self.listen_for_command(timeout=15)
                    
                    if command:
                        # Process command
                        continue_listening = self.process_command(command)
                        
                        if not continue_listening:
                            break
                    else:
                        self.speak("I didn't catch that, Sir. Please try again.")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupt received")
            self.speak("Voice interface shutting down. Goodbye, Sir.")
        except Exception as e:
            print(f"❌ Voice loop error: {e}")
            self.speak("Voice system error. Shutting down.")
    
    def test_voice_components(self):
        """Test all voice components"""
        print("\n🧪 Testing JARVIS Voice Components...")
        
        # Test AI
        print("\n🧠 Testing AI Engine...")
        try:
            response = self.ai.chat("Hello JARVIS, are you ready?")
            print(f"✅ AI Response: {response}")
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return False
        
        # Test TTS
        print("\n🗣️ Testing Text-to-Speech...")
        try:
            self.speak("Voice test successful. JARVIS speaking clearly.")
            print("✅ TTS Working")
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return False
        
        # Test microphone
        print("\n🎤 Testing Microphone...")
        if self.microphone:
            print("✅ Microphone Ready")
        else:
            print("❌ Microphone Not Available")
            return False
        
        # Test speech recognition
        print("\n🎤 Testing Speech Recognition (say something)...")
        try:
            test_command = self.listen_for_command(timeout=5)
            if test_command:
                print(f"✅ Speech Recognition: Heard '{test_command}'")
            else:
                print("⚠️ Speech Recognition: No input detected")
        except Exception as e:
            print(f"❌ Speech Recognition Error: {e}")
        
        print("\n✅ Voice component testing complete!")
        return True

def main():
    """Main function"""
    print("🔥🔥🔥 JARVIS LOCAL VOICE SYSTEM 🔥🔥🔥")
    
    if not HAS_VOICE:
        print("❌ Voice dependencies not available")
        print("Please install: pip install speechrecognition pyttsx3 pyaudio")
        return
    
    # Initialize voice engine
    voice_engine = JarvisLocalVoiceEngine()
    
    # Test components first
    print("\n🔧 Running system checks...")
    if not voice_engine.test_voice_components():
        print("❌ Voice system not ready")
        return
    
    # Ask user what to do
    print("\n🎮 Choose an option:")
    print("1. Start voice interaction loop")
    print("2. Test individual components")
    print("3. Quick voice test")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            voice_engine.run_voice_loop()
        elif choice == "2":
            voice_engine.test_voice_components()
        elif choice == "3":
            print("\n🎤 Quick Test - Say something:")
            command = voice_engine.listen_for_command(timeout=10)
            if command:
                voice_engine.process_command(command)
            else:
                print("❓ No input detected")
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
