#!/usr/bin/env python3
"""
JARVIS-X CLEAN Voice Engine
Simplified voice engine without LiveKit dependencies
All import issues resolved
"""

import os
import sys
import asyncio
import time
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

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assistant.ai_engine import JarvisAI

# Load environment
load_dotenv()

class CleanVoiceEngine:
    """Clean voice engine with no import issues"""
    
    def __init__(self):
        """Initialize clean voice engine"""
        print("🔥 Initializing JARVIS-X Clean Voice Engine...")
        
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
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.setup_microphone()
        
        # TTS setup
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        print("✅ Clean Voice Engine Ready!")
        print("🎤 Available wake words:", ", ".join(self.wake_words))
    
    def setup_microphone(self):
        """Setup microphone with optimal settings"""
        try:
            # Use default microphone with optimal settings
            self.microphone = sr.Microphone(sample_rate=16000, chunk_size=1024)
            
            # Calibrate for ambient noise
            with self.microphone as source:
                print("🔧 Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"✅ Energy threshold: {self.recognizer.energy_threshold}")
                
        except Exception as e:
            print(f"❌ Microphone setup error: {e}")
            self.microphone = sr.Microphone()  # Fallback to default
    
    def setup_tts(self):
        """Setup text-to-speech with optimal settings"""
        try:
            voices = self.tts_engine.getProperty('voices')
            
            # Find best voice (prefer male, high quality)
            best_voice = None
            for voice in voices:
                if 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                    best_voice = voice
                    break
                elif voice.gender and 'male' in str(voice.gender).lower():
                    best_voice = voice
            
            if best_voice:
                self.tts_engine.setProperty('voice', best_voice.id)
                print(f"✅ Voice set to: {best_voice.name}")
            
            # Optimize speech settings
            self.tts_engine.setProperty('rate', 170)  # Speed
            self.tts_engine.setProperty('volume', 0.95)  # Volume
            
        except Exception as e:
            print(f"❌ TTS setup error: {e}")
    
    def speak(self, text):
        """Speak text using TTS"""
        if not text.strip():
            return
        
        self.speaking = True
        print(f"🤖 JARVIS: {text}")
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Speech error: {e}")
        finally:
            self.speaking = False
    
    def listen_for_speech(self, timeout=5, phrase_timeout=8):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                
                # Optimize recognition settings
                self.recognizer.energy_threshold = max(self.recognizer.energy_threshold, 200)
                self.recognizer.dynamic_energy_threshold = True
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
                
                # Try to recognize speech
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Recognized: {text}")
                return text.lower().strip()
                
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Recognition error: {e}")
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
                return "How can I help you?"
            
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
            
            # Shorten long responses for voice
            if len(response) > 200:
                sentences = response.split('. ')
                if len(sentences) > 2:
                    response = '. '.join(sentences[:2]) + "."
                    response += " Would you like me to elaborate?"
            
            return response
            
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            return "I encountered an error. Please try again."
    
    def voice_interaction_loop(self):
        """Main voice interaction loop"""
        self.speak("JARVIS voice system online. I'm ready to assist you, Sir.")
        
        self.voice_active = True
        
        while self.voice_active:
            try:
                # Listen for wake word or command
                if not self.conversation_active:
                    # Listen for wake word
                    text = self.listen_for_speech(timeout=2, phrase_timeout=4)
                    
                    if text and self.is_wake_word(text):
                        self.conversation_active = True
                        self.speak("Yes, Sir?")
                        continue
                
                else:
                    # In conversation mode - listen for commands
                    text = self.listen_for_speech(timeout=5, phrase_timeout=10)
                    
                    if text:
                        # Process command
                        response = self.process_command(text)
                        self.speak(response)
                        
                        # Continue conversation
                        self.speak("Anything else?")
                    else:
                        # No speech detected - end conversation
                        self.speak("I'm here when you need me.")
                        self.conversation_active = False
                
                # Brief pause
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                time.sleep(1)
        
        self.speak("JARVIS voice system shutting down. Goodbye, Sir.")
    
    def test_voice_system(self):
        """Test voice system components"""
        print("\n🔧 Testing Voice System...")
        
        # Test TTS
        print("1. Testing Text-to-Speech...")
        self.speak("Voice test successful. Text to speech is working.")
        
        # Test microphone
        print("2. Testing Microphone - say something...")
        text = self.listen_for_speech(timeout=8, phrase_timeout=5)
        
        if text:
            self.speak(f"Perfect! I heard you say: {text}")
        else:
            self.speak("No speech detected. Please check your microphone.")
        
        # Test AI
        print("3. Testing AI integration...")
        response = self.process_command("say hello and confirm you're working")
        self.speak(response)
        
        print("✅ Voice system test complete!")

def main():
    """Main function"""
    print("🔥 JARVIS-X Clean Voice Engine")
    print("=" * 50)
    
    # Initialize voice engine
    voice = CleanVoiceEngine()
    
    print("\n🎯 Select mode:")
    print("1. Full voice interaction")
    print("2. Voice system test")
    print("3. Single command test")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            voice.voice_interaction_loop()
        elif choice == "2":
            voice.test_voice_system()
        elif choice == "3":
            voice.speak("What would you like me to do?")
            text = voice.listen_for_speech(timeout=10, phrase_timeout=8)
            if text:
                response = voice.process_command(text)
                voice.speak(response)
            else:
                voice.speak("I didn't hear anything.")
        else:
            voice.voice_interaction_loop()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
