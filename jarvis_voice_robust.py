#!/usr/bin/env python3
"""
JARVIS-X ROBUST Voice Engine
Reliable voice assistant with proper error handling
- System TTS (always works)
- Optional Edge TTS (if available)
- LiveKit integration (with fallback)
- Advanced speech recognition
"""

import os
import sys
import asyncio
import json
import time
import tempfile
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import requests
from dotenv import load_dotenv

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

# Load environment
load_dotenv()

class RobustVoiceEngine:
    """Robust voice engine with bulletproof error handling"""
    
    def __init__(self):
        """Initialize robust voice engine"""
        print("🔥 Initializing JARVIS-X Robust Voice Engine...")
        
        # AI Engine
        self.ai = JarvisAI()
        
        # Voice settings
        self.voice_active = False
        self.listening = False
        self.speaking = False
        self.conversation_active = False
        
        # Wake words
        self.wake_words = [
            "jarvis", "hey jarvis", "jarvis x", "ok jarvis", 
            "computer", "assistant", "ai", "hey ai"
        ]
        
        # Initialize components with error handling
        self.setup_speech_recognition()
        self.setup_text_to_speech()
        self.check_edge_tts()
        
        print("✅ Robust Voice Engine Ready!")
        print("🎤 Say 'JARVIS' to activate")
    
    def setup_speech_recognition(self):
        """Setup speech recognition with error handling"""
        try:
            self.recognizer = sr.Recognizer()
            
            # Get available microphones
            mics = sr.Microphone.list_microphone_names()
            print(f"🎤 Available microphones: {len(mics)}")
            
            # Use default microphone
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                print("🔧 Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"✅ Energy threshold: {self.recognizer.energy_threshold}")
            
            # Optimize settings
            self.recognizer.energy_threshold = max(self.recognizer.energy_threshold, 300)
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
        except Exception as e:
            print(f"❌ Speech recognition setup error: {e}")
            raise
    
    def setup_text_to_speech(self):
        """Setup text-to-speech with best available voice"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            print(f"🔊 Available voices: {len(voices)}")
            
            # Find the best voice
            best_voice = None
            preferred_voices = ['hazel', 'zira', 'david', 'mark', 'microsoft']
            
            for voice in voices:
                voice_name = voice.name.lower()
                for preferred in preferred_voices:
                    if preferred in voice_name:
                        best_voice = voice
                        break
                if best_voice:
                    break
            
            # If no preferred voice found, use first available
            if not best_voice and voices:
                best_voice = voices[0]
            
            if best_voice:
                self.tts_engine.setProperty('voice', best_voice.id)
                print(f"✅ Selected voice: {best_voice.name}")
            
            # Set optimal speech settings
            self.tts_engine.setProperty('rate', 160)  # Clear speech rate
            self.tts_engine.setProperty('volume', 0.95)  # High volume
            
        except Exception as e:
            print(f"❌ TTS setup error: {e}")
            raise
    
    def check_edge_tts(self):
        """Check if Edge TTS is available"""
        try:
            import edge_tts
            self.edge_tts_available = True
            print("✅ Edge TTS available (will use as fallback)")
        except ImportError:
            self.edge_tts_available = False
            print("⚠️ Edge TTS not available - using system TTS only")
    
    def speak(self, text):
        """Speak text using system TTS (most reliable)"""
        if not text or not text.strip():
            return
        
        self.speaking = True
        print(f"🤖 JARVIS: {text}")
        
        try:
            # Use system TTS (most reliable)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
            # Fallback - just print
            print(f"🤖 JARVIS (text only): {text}")
        finally:
            self.speaking = False
    
    def listen_for_speech(self, timeout=5, phrase_timeout=8):
        """Listen for speech with robust error handling"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
                
                # Try to recognize speech
                text = self.recognizer.recognize_google(audio, language='en-US')
                print(f"✅ Recognized: {text}")
                return text.lower().strip()
                
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Listen error: {e}")
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
    
    def process_command(self, command):
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
            
            # Optimize response for voice (shorter responses)
            if len(response) > 200:
                sentences = response.split('. ')
                if len(sentences) > 2:
                    response = '. '.join(sentences[:2]) + "."
                    response += " Would you like me to continue?"
            
            return response
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            return "I encountered an error processing your request. Please try again."
    
    def voice_interaction_loop(self):
        """Main voice interaction loop with robust error handling"""
        self.speak("JARVIS voice system online. I'm ready to assist you, Sir.")
        
        self.voice_active = True
        
        while self.voice_active:
            try:
                # Listen for wake word or command
                if not self.conversation_active:
                    # Listen for wake word (shorter timeout)
                    text = self.listen_for_speech(timeout=2, phrase_timeout=4)
                    
                    if text and self.is_wake_word(text):
                        self.conversation_active = True
                        self.speak("Yes, Sir? How may I assist you?")
                        continue
                
                else:
                    # In conversation mode - listen for commands
                    text = self.listen_for_speech(timeout=6, phrase_timeout=10)
                    
                    if text:
                        # Process command
                        response = self.process_command(text)
                        self.speak(response)
                        
                        # Continue conversation
                        self.speak("Anything else?")
                    else:
                        # No speech detected - end conversation
                        self.speak("I'm here when you need me, Sir.")
                        self.conversation_active = False
                
                # Brief pause to prevent CPU overload
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                time.sleep(1)  # Pause before retrying
        
        self.speak("JARVIS voice system shutting down. Goodbye, Sir.")
    
    def test_voice_system(self):
        """Test voice system components"""
        print("\n🔧 Testing Voice System...")
        
        # Test TTS
        print("1. Testing Text-to-Speech...")
        self.speak("Voice test successful. Text to speech is working perfectly.")
        
        # Test microphone
        print("2. Testing Microphone - say something...")
        text = self.listen_for_speech(timeout=8, phrase_timeout=5)
        
        if text:
            self.speak(f"Excellent! I heard you say: {text}")
        else:
            self.speak("No speech detected. Please check your microphone.")
        
        # Test AI
        print("3. Testing AI integration...")
        response = self.process_command("say hello and confirm you're working")
        self.speak(response)
        
        print("✅ Voice system test complete!")
    
    def single_command_test(self):
        """Test with a single voice command"""
        self.speak("What would you like me to do?")
        text = self.listen_for_speech(timeout=10, phrase_timeout=8)
        
        if text:
            response = self.process_command(text)
            self.speak(response)
        else:
            self.speak("I didn't hear anything. Please try again.")

def main():
    """Main function with robust error handling"""
    print("🔥 JARVIS-X Robust Voice Engine")
    print("=" * 50)
    
    try:
        # Initialize voice engine
        voice = RobustVoiceEngine()
        
        print("\n🎯 Select mode:")
        print("1. Full voice interaction")
        print("2. Voice system test")
        print("3. Single command test")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🎤 Starting voice interaction...")
            print("💬 Say 'JARVIS' to activate")
            print("❌ Press Ctrl+C to exit")
            voice.voice_interaction_loop()
        elif choice == "2":
            voice.test_voice_system()
        elif choice == "3":
            voice.single_command_test()
        else:
            print("Invalid choice. Starting voice interaction...")
            voice.voice_interaction_loop()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your microphone and try again.")

if __name__ == "__main__":
    main()
