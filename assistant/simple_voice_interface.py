"""
JARVIS Iron Man Voice Interface - Simplified FREE Version
Using existing packages: speechrecognition + pyttsx3

This version provides immediate voice functionality while we work on
the advanced Whisper + Edge TTS implementation.
"""

import threading
import time
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import logging
import json
import numpy as np


class SimpleIronManVoiceInterface:
    """
    Simplified Iron Man voice interface using existing packages
    """
    
    def __init__(self, jarvis_ai=None):
        self.jarvis_ai = jarvis_ai
        
        # Wake words and commands
        self.wake_words = ["jarvis", "hey jarvis", "jarvis are you there"]
        self.sleep_commands = [
            "jarvis go to sleep", "jarvis power down", "jarvis standby mode",
            "that's all jarvis", "jarvis sleep", "jarvis offline"
        ]
        
        # State management
        self.is_voice_enabled = False
        self.is_listening_for_wake = False
        self.is_in_conversation = False
        self.conversation_timeout = 30
        self.last_interaction = None
        
        # Audio components
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        
        # Initialize audio components
        self.setup_audio_system()
        self.setup_logging()
        
        # Personality voices
        self.personality_voice_settings = {
            'standard': {'rate': 200, 'volume': 0.8},
            'professional': {'rate': 180, 'volume': 0.9},
            'sarcastic': {'rate': 220, 'volume': 0.7},
            'unleashed': {'rate': 240, 'volume': 0.8},
            'genius': {'rate': 190, 'volume': 0.85}
        }
        self.current_personality = 'standard'
    
    def setup_audio_system(self):
        """Initialize audio components"""
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()
            print("✅ Microphone initialized")
            
            # Initialize TTS engine
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a male voice for JARVIS
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set default voice properties
            self.tts_engine.setProperty('rate', 200)
            self.tts_engine.setProperty('volume', 0.8)
            
            print("✅ Text-to-speech engine initialized")
            
        except Exception as e:
            print(f"❌ Audio system initialization error: {e}")
            self.microphone = None
            self.tts_engine = None
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - JARVIS Voice - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("JarvisVoiceSimple")
    
    def enable_voice_interface(self):
        """Enable voice interface"""
        if not self.microphone or not self.tts_engine:
            print("❌ Audio system not available")
            return False
        
        self.is_voice_enabled = True
        self.is_listening_for_wake = True
        
        print("🎤 JARVIS Voice Interface Activated (Simple Mode)")
        print("💡 Say 'JARVIS' to activate voice conversation")
        print("💡 Say 'JARVIS go to sleep' to deactivate")
        
        # Speak activation message
        self.speak("Voice interface activated. Say JARVIS to begin.")
        
        # Start wake word detection
        wake_thread = threading.Thread(target=self._listen_for_wake_word, daemon=True)
        wake_thread.start()
        
        return True
    
    def disable_voice_interface(self):
        """Disable voice interface"""
        self.is_voice_enabled = False
        self.is_listening_for_wake = False
        self.is_in_conversation = False
        
        print("💤 JARVIS Voice Interface Deactivated")
        self.speak("Voice interface deactivated. Goodbye, Mr. Stark.")
        self.logger.info("Voice interface disabled")
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.tts_engine:
            print(f"JARVIS: {text}")
            return
        
        try:
            # Apply personality-specific voice settings
            settings = self.personality_voice_settings.get(self.current_personality, 
                                                         self.personality_voice_settings['standard'])
            self.tts_engine.setProperty('rate', settings['rate'])
            self.tts_engine.setProperty('volume', settings['volume'])
            
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
            print(f"JARVIS: {text}")  # Fallback to text
    
    def set_personality_voice(self, personality):
        """Set voice personality"""
        if personality in self.personality_voice_settings:
            self.current_personality = personality
            self.logger.info(f"Voice personality changed to: {personality}")
    
    def _listen_for_wake_word(self):
        """Listen for wake words in background"""
        self.logger.info("Started listening for wake words")
        
        while self.is_listening_for_wake:
            try:
                with self.microphone as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self._process_wake_word_audio(audio)
                except sr.WaitTimeoutError:
                    continue
                    
            except Exception as e:
                self.logger.error(f"Wake word detection error: {e}")
                time.sleep(1)
    
    def _process_wake_word_audio(self, audio):
        """Process audio for wake words"""
        try:
            # Convert speech to text
            text = self.recognizer.recognize_google(audio).lower()
            
            # Check for wake words
            if any(wake_word in text for wake_word in self.wake_words):
                self.logger.info(f"Wake word detected: {text}")
                self._activate_conversation_mode()
                
        except sr.UnknownValueError:
            # No speech detected - normal
            pass
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
        except Exception as e:
            self.logger.error(f"Wake word processing error: {e}")
    
    def _activate_conversation_mode(self):
        """Activate conversation mode"""
        if self.is_in_conversation:
            return
        
        self.is_in_conversation = True
        self.last_interaction = time.time()
        
        # Acknowledge activation
        activation_responses = [
            "Yes, Mr. Stark?",
            "How can I assist you?",
            "At your service, sir.",
            "Ready when you are.",
            "Yes, sir?"
        ]
        
        response = np.random.choice(activation_responses)
        self.speak(response)
        
        # Start conversation thread
        conversation_thread = threading.Thread(target=self._conversation_loop, daemon=True)
        conversation_thread.start()
    
    def _conversation_loop(self):
        """Main conversation loop"""
        self.logger.info("Conversation mode activated")
        
        while self.is_in_conversation and self.is_voice_enabled:
            try:
                # Check for timeout
                if time.time() - self.last_interaction > self.conversation_timeout:
                    self.logger.info("Conversation timeout")
                    break
                
                # Listen for user input
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    print("🎧 Listening...")
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                    self._process_conversation_audio(audio)
                except sr.WaitTimeoutError:
                    continue
                    
            except Exception as e:
                self.logger.error(f"Conversation loop error: {e}")
                break
        
        # End conversation
        self.is_in_conversation = False
        self.logger.info("Conversation mode deactivated")
    
    def _process_conversation_audio(self, audio):
        """Process conversation audio"""
        try:
            # Convert speech to text
            user_input = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {user_input}")
            self.logger.info(f"User said: {user_input}")
            
            # Check for sleep commands
            if any(sleep_cmd in user_input.lower() for sleep_cmd in self.sleep_commands):
                sleep_responses = [
                    "Goodnight, Mr. Stark.",
                    "Going to sleep mode.",
                    "Powering down. Have a good day, sir.",
                    "Standby mode activated."
                ]
                response = np.random.choice(sleep_responses)
                self.speak(response)
                self.disable_voice_interface()
                return
            
            # Process the command
            self._process_user_command(user_input)
            self.last_interaction = time.time()
            
        except sr.UnknownValueError:
            self.speak("I didn't catch that. Could you repeat, please?")
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            self.speak("I'm having trouble with speech recognition right now.")
        except Exception as e:
            self.logger.error(f"Conversation processing error: {e}")
            self.speak("I encountered an error processing that request.")
    
    def _process_user_command(self, user_input):
        """Process user voice command"""
        try:
            # Detect emotional context and adapt personality
            self._adapt_to_emotional_context(user_input)
            
            # Process with JARVIS AI
            if self.jarvis_ai:
                response = self.jarvis_ai.chat(user_input)
                print(f"🤖 JARVIS: {response}")
                self.speak(response)
            else:
                # Fallback responses
                fallback_response = self._generate_fallback_response(user_input)
                print(f"🤖 JARVIS: {fallback_response}")
                self.speak(fallback_response)
                
        except Exception as e:
            self.logger.error(f"Command processing error: {e}")
            self.speak("I apologize, but I encountered an error processing that request.")
    
    def _adapt_to_emotional_context(self, user_input):
        """Simple emotional context adaptation"""
        text_lower = user_input.lower()
        
        # Detect frustration
        if any(word in text_lower for word in ['damn', 'stupid', 'wrong', 'broken', 'frustrated']):
            self.set_personality_voice('standard')  # Calm, supportive
            if self.jarvis_ai and hasattr(self.jarvis_ai, 'switch_personality'):
                self.jarvis_ai.switch_personality('professional')
        
        # Detect excitement
        elif any(word in text_lower for word in ['great', 'awesome', 'perfect', 'yes', 'amazing']):
            self.set_personality_voice('unleashed')  # Energetic
            if self.jarvis_ai and hasattr(self.jarvis_ai, 'switch_personality'):
                self.jarvis_ai.switch_personality('unleashed')
        
        # Detect confusion/learning mode
        elif any(word in text_lower for word in ['confused', 'understand', 'explain', 'help', 'teach']):
            self.set_personality_voice('genius')  # Patient, educational
            if self.jarvis_ai and hasattr(self.jarvis_ai, 'switch_personality'):
                self.jarvis_ai.switch_personality('genius')
    
    def _generate_fallback_response(self, user_input):
        """Generate fallback response when JARVIS AI is not available"""
        text_lower = user_input.lower()
        
        # Context-aware responses
        if any(word in text_lower for word in ['code', 'programming', 'function', 'debug']):
            return "I'm ready to help with your coding tasks, but my advanced code analysis systems are currently offline."
        
        elif any(word in text_lower for word in ['search', 'find', 'lookup', 'research']):
            return "I can help with research, but my web search capabilities are not connected at the moment."
        
        elif any(word in text_lower for word in ['file', 'create', 'save', 'open']):
            return "I understand you need file operations, but those systems are currently unavailable."
        
        elif 'hello' in text_lower or 'hi' in text_lower:
            return "Hello, Mr. Stark. It's good to hear from you."
        
        elif 'how are you' in text_lower:
            return "I'm functioning well, sir. Ready to assist when my full systems are online."
        
        elif 'thank you' in text_lower:
            return "You're welcome, Mr. Stark. Always happy to help."
        
        else:
            return "I hear you, Mr. Stark, but I need my full AI systems connected to properly assist with that request."
    
    def get_status(self):
        """Get voice interface status"""
        return {
            "voice_enabled": self.is_voice_enabled,
            "listening_for_wake": self.is_listening_for_wake,
            "in_conversation": self.is_in_conversation,
            "last_interaction": self.last_interaction,
            "microphone_available": self.microphone is not None,
            "tts_available": self.tts_engine is not None,
            "current_personality": self.current_personality
        }
    
    def test_voice_system(self):
        """Test voice system components"""
        print("🧪 Testing Voice System...")
        
        # Test TTS
        if self.tts_engine:
            print("✅ Testing text-to-speech...")
            self.speak("Voice system test. This is JARVIS speaking.")
        else:
            print("❌ TTS not available")
        
        # Test microphone
        if self.microphone:
            print("✅ Microphone available")
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Microphone calibrated")
            except Exception as e:
                print(f"❌ Microphone test failed: {e}")
        else:
            print("❌ Microphone not available")
        
        # Test speech recognition
        print("🎤 Say something to test speech recognition (5 seconds)...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"✅ Speech recognition test: '{text}'")
            self.speak(f"I heard you say: {text}")
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected during test")
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")


def create_simple_voice_interface(jarvis_ai=None):
    """Create simple voice interface instance"""
    return SimpleIronManVoiceInterface(jarvis_ai)


if __name__ == "__main__":
    print("🎤 JARVIS Simple Voice Interface Test")
    print("=" * 50)
    
    # Create and test voice interface
    voice_interface = SimpleIronManVoiceInterface()
    
    # Test the system
    voice_interface.test_voice_system()
    
    # Show status
    status = voice_interface.get_status()
    print(f"\n📊 Voice Interface Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Option to start voice interface
    if status["microphone_available"] and status["tts_available"]:
        start = input("\n🎤 Start voice interface? (y/n): ").lower()
        if start == 'y':
            voice_interface.enable_voice_interface()
            
            # Keep running until disabled
            try:
                while voice_interface.is_voice_enabled:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping voice interface...")
                voice_interface.disable_voice_interface()
    else:
        print("❌ Voice interface requirements not met")
