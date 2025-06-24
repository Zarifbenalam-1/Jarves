"""
JARVIS Iron Man Voice Interface
100% FREE Implementation with Wake Word Detection

This module provides voice interaction capabilities for JARVIS-X,
implementing the authentic Iron Man experience with zero cost.
"""

import threading
import time
import numpy as np
import speech_recognition as sr
from datetime import datetime
import logging
import os
import asyncio
import json

# Free libraries for voice processing
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Whisper not installed. Run: pip install openai-whisper")

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️  Edge TTS not installed. Run: pip install edge-tts")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠️  PyAudio not installed. Run: pip install pyaudio")


class IronManWakeWordDetector:
    """
    Iron Man authentic wake word detection system
    Detects: "JARVIS", "Hey JARVIS", "JARVIS are you there"
    """
    
    def __init__(self):
        self.wake_words = [
            "jarvis",
            "hey jarvis", 
            "jarvis are you there",
            "jarvis wake up"
        ]
        
        self.sleep_commands = [
            "jarvis go to sleep",
            "jarvis power down", 
            "jarvis standby mode",
            "that's all jarvis",
            "jarvis sleep",
            "jarvis offline"
        ]
        
        self.status_commands = [
            "jarvis status",
            "jarvis are you online", 
            "jarvis system check",
            "jarvis how are you"
        ]
        
        self.is_listening = False
        self.is_active = False
        
    def detect_wake_word(self, text):
        """Check if text contains a wake word"""
        text_lower = text.lower().strip()
        
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def detect_sleep_command(self, text):
        """Check if text contains a sleep command"""
        text_lower = text.lower().strip()
        
        for sleep_cmd in self.sleep_commands:
            if sleep_cmd in text_lower:
                return True
        return False
    
    def detect_status_command(self, text):
        """Check if text contains a status command"""
        text_lower = text.lower().strip()
        
        for status_cmd in self.status_commands:
            if status_cmd in text_lower:
                return True
        return False


class FreeSpeechProcessor:
    """
    100% Free speech processing using Whisper (local) and Edge TTS
    """
    
    def __init__(self):
        self.whisper_model = None
        self.tts_voices = self._setup_personality_voices()
        self.current_personality = 'standard'
        
        # Initialize Whisper model if available
        if WHISPER_AVAILABLE:
            try:
                print("🧠 Loading Whisper model (this may take a moment)...")
                self.whisper_model = whisper.load_model("base")
                print("✅ Whisper model loaded successfully")
            except Exception as e:
                print(f"❌ Error loading Whisper model: {e}")
                self.whisper_model = None
    
    def _setup_personality_voices(self):
        """Map JARVIS personalities to free Edge TTS voices"""
        return {
            'standard': 'en-US-AriaNeural',      # Professional, balanced
            'professional': 'en-US-DavisNeural', # Authoritative, clear  
            'sarcastic': 'en-US-GuyNeural',      # Witty, expressive
            'unleashed': 'en-US-TonyNeural',     # Confident, intense
            'genius': 'en-US-JennyNeural'        # Intelligent, smooth
        }
    
    def speech_to_text(self, audio_file_path):
        """Convert speech to text using free Whisper"""
        if not self.whisper_model:
            return {"success": False, "error": "Whisper model not available"}
        
        try:
            result = self.whisper_model.transcribe(audio_file_path)
            return {
                "success": True,
                "text": result["text"].strip(),
                "language": result.get("language", "en"),
                "confidence": result.get("confidence", 0.0)
            }
        except Exception as e:
            return {"success": False, "error": f"Speech recognition failed: {str(e)}"}
    
    async def text_to_speech(self, text, output_file="temp_speech.wav"):
        """Convert text to speech using free Edge TTS"""
        if not EDGE_TTS_AVAILABLE:
            return {"success": False, "error": "Edge TTS not available"}
        
        try:
            voice = self.tts_voices.get(self.current_personality, self.tts_voices['standard'])
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
            
            return {
                "success": True,
                "audio_file": output_file,
                "voice": voice,
                "personality": self.current_personality
            }
        except Exception as e:
            return {"success": False, "error": f"Text-to-speech failed: {str(e)}"}
    
    def set_personality_voice(self, personality):
        """Change voice based on JARVIS personality"""
        if personality in self.tts_voices:
            self.current_personality = personality
            return True
        return False


class ContextualVoiceCommands:
    """
    Handle context-aware voice commands like Iron Man
    """
    
    def __init__(self):
        self.context_commands = {
            'fix_error': [
                'fix this error', 'help with error', 'debug this',
                'what\'s wrong here', 'solve this problem'
            ],
            'explain_code': [
                'what does this do', 'explain this', 'how does this work',
                'what\'s this function', 'break this down'
            ],
            'optimize': [
                'make this faster', 'optimize this', 'improve performance',
                'speed this up', 'make it efficient'
            ],
            'educate': [
                'explain like im 5', 'teach me', 'help me understand',
                'simple explanation', 'walk me through'
            ],
            'create': [
                'create function', 'make a class', 'write code for',
                'generate code', 'build this'
            ],
            'test': [
                'test this code', 'write tests', 'check if this works',
                'validate this', 'run tests'
            ]
        }
    
    def classify_command(self, voice_input):
        """Classify voice input into command categories"""
        voice_lower = voice_input.lower()
        
        for command_type, phrases in self.context_commands.items():
            for phrase in phrases:
                if phrase in voice_lower:
                    return {
                        "type": command_type,
                        "confidence": 0.9,
                        "matched_phrase": phrase,
                        "original_input": voice_input
                    }
        
        return {
            "type": "general",
            "confidence": 0.5,
            "matched_phrase": None,
            "original_input": voice_input
        }
    
    def extract_context(self, command_classification):
        """Extract context clues from the command"""
        cmd_type = command_classification["type"]
        original = command_classification["original_input"]
        
        context = {
            "command_type": cmd_type,
            "requires_screen_context": cmd_type in ['fix_error', 'explain_code', 'optimize'],
            "requires_file_context": cmd_type in ['create', 'test'],
            "educational_mode": cmd_type in ['educate', 'explain_code'],
            "original_command": original
        }
        
        return context


class ProactiveVoiceAssistant:
    """
    Proactive voice assistance - JARVIS speaks up when appropriate
    """
    
    def __init__(self):
        self.last_error_time = None
        self.error_count = 0
        self.success_celebrations = [
            "Nice work, Mr. Stark!",
            "Excellent execution!",
            "That's some clean code, sir.",
            "Well done!",
            "Perfect implementation, Mr. Stark."
        ]
        
        self.encouragement_phrases = [
            "Don't worry, we'll figure this out.",
            "Take a deep breath, Mr. Stark. We've got this.",
            "Every problem has a solution.",
            "You're on the right track.",
            "Let's approach this systematically."
        ]
        
        self.problem_detected_phrases = [
            "I notice you're having trouble. Would you like assistance?",
            "Shall I help you with this issue?",
            "I have some suggestions that might help.",
            "Would you like me to analyze this problem?"
        ]
    
    def should_offer_help(self, context):
        """Determine if JARVIS should proactively offer help"""
        current_time = time.time()
        
        # If user has been struggling with errors
        if context.get('error_detected'):
            if self.last_error_time and (current_time - self.last_error_time) < 300:  # 5 minutes
                self.error_count += 1
                if self.error_count >= 3:
                    return "repeated_errors"
            else:
                self.error_count = 1
            self.last_error_time = current_time
        
        # If user seems stuck (no activity)
        if context.get('idle_time', 0) > 600:  # 10 minutes idle
            return "stuck_detection"
        
        # If performance issues detected
        if context.get('performance_issue'):
            return "optimization_opportunity"
        
        return None
    
    def get_proactive_message(self, trigger_type):
        """Get appropriate proactive message"""
        if trigger_type == "repeated_errors":
            return np.random.choice(self.problem_detected_phrases)
        elif trigger_type == "stuck_detection":
            return "You've been quiet for a while. Need any assistance, Mr. Stark?"
        elif trigger_type == "optimization_opportunity":
            return "I have a suggestion that might improve performance here."
        
        return None
    
    def celebrate_success(self, achievement_type="general"):
        """Generate celebration message"""
        return np.random.choice(self.success_celebrations)


class VoiceEmotionalIntelligence:
    """
    Detect emotional state from voice patterns and adapt responses
    """
    
    def __init__(self):
        self.emotional_states = {
            'frustrated': ['stressed', 'angry', 'annoyed'],
            'excited': ['enthusiastic', 'happy', 'energetic'],
            'focused': ['concentrated', 'determined', 'engaged'],
            'tired': ['exhausted', 'weary', 'fatigued'],
            'confused': ['uncertain', 'puzzled', 'lost']
        }
        
        self.adaptive_responses = {
            'frustrated': 'supportive',
            'excited': 'celebratory', 
            'focused': 'efficient',
            'tired': 'gentle',
            'confused': 'educational'
        }
    
    def analyze_voice_emotion(self, voice_characteristics):
        """Analyze emotional state from voice (placeholder for future ML model)"""
        # This is a simplified version - in full implementation,
        # we would analyze audio features like pitch, speed, pauses
        
        # For now, detect from speech patterns and words
        speech_text = voice_characteristics.get('text', '').lower()
        
        # Simple keyword-based emotion detection
        if any(word in speech_text for word in ['damn', 'stupid', 'wrong', 'broken']):
            return 'frustrated'
        elif any(word in speech_text for word in ['great', 'awesome', 'perfect', 'yes']):
            return 'excited'
        elif any(word in speech_text for word in ['focus', 'work', 'code', 'implement']):
            return 'focused'
        elif any(word in speech_text for word in ['tired', 'exhausted', 'long day']):
            return 'tired'
        elif any(word in speech_text for word in ['confused', 'understand', 'explain', 'help']):
            return 'confused'
        
        return 'neutral'
    
    def get_adaptive_personality(self, emotional_state):
        """Get recommended personality mode based on emotion"""
        return self.adaptive_responses.get(emotional_state, 'standard')


class JarvisVoiceInterface:
    """
    Main voice interface class - coordinates all voice components
    """
    
    def __init__(self, jarvis_ai=None):
        self.jarvis_ai = jarvis_ai
        self.wake_detector = IronManWakeWordDetector()
        self.speech_processor = FreeSpeechProcessor()
        self.contextual_commands = ContextualVoiceCommands()
        self.proactive_assistant = ProactiveVoiceAssistant()
        self.emotional_intelligence = VoiceEmotionalIntelligence()
        
        # State management
        self.is_voice_enabled = False
        self.is_listening_for_wake = False
        self.is_in_conversation = False
        self.conversation_timeout = 30  # seconds
        self.last_interaction = None
        
        # Audio setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone() if PYAUDIO_AVAILABLE else None
        
        # Logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup voice interface logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - JARVIS Voice - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("JarvisVoice")
    
    def enable_voice_interface(self):
        """Enable voice interface with wake word detection"""
        if not all([WHISPER_AVAILABLE, EDGE_TTS_AVAILABLE, PYAUDIO_AVAILABLE]):
            missing = []
            if not WHISPER_AVAILABLE: missing.append("openai-whisper")
            if not EDGE_TTS_AVAILABLE: missing.append("edge-tts") 
            if not PYAUDIO_AVAILABLE: missing.append("pyaudio")
            
            print(f"❌ Missing required packages: {', '.join(missing)}")
            print("Please install with: pip install " + " ".join(missing))
            return False
        
        self.is_voice_enabled = True
        self.is_listening_for_wake = True
        
        print("🎤 JARVIS Voice Interface Activated")
        print("💡 Say 'JARVIS' to activate voice conversation")
        print("💡 Say 'JARVIS go to sleep' to deactivate")
        
        # Start wake word detection in background thread
        wake_thread = threading.Thread(target=self._listen_for_wake_word, daemon=True)
        wake_thread.start()
        
        return True
    
    def disable_voice_interface(self):
        """Disable voice interface"""
        self.is_voice_enabled = False
        self.is_listening_for_wake = False
        self.is_in_conversation = False
        
        print("💤 JARVIS Voice Interface Deactivated")
        self.logger.info("Voice interface disabled")
    
    def _listen_for_wake_word(self):
        """Background thread to listen for wake words"""
        if not self.microphone:
            print("❌ No microphone available")
            return
        
        self.logger.info("Started listening for wake words")
        
        while self.is_listening_for_wake:
            try:
                with self.microphone as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                # Listen for audio with timeout
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    continue
                
                # Process audio for wake words
                self._process_wake_word_audio(audio)
                
            except Exception as e:
                self.logger.error(f"Wake word detection error: {e}")
                time.sleep(1)  # Brief pause on error
    
    def _process_wake_word_audio(self, audio):
        """Process audio for wake word detection"""
        try:
            # Use basic speech recognition for wake word (faster than Whisper)
            text = self.recognizer.recognize_google(audio).lower()
            
            if self.wake_detector.detect_wake_word(text):
                self.logger.info(f"Wake word detected: {text}")
                self._activate_conversation_mode()
            
        except sr.UnknownValueError:
            # No speech detected - this is normal
            pass
        except sr.RequestError as e:
            # Fallback to Whisper if Google fails
            self._process_with_whisper(audio)
        except Exception as e:
            self.logger.error(f"Wake word processing error: {e}")
    
    def _process_with_whisper(self, audio):
        """Fallback processing with Whisper"""
        try:
            # Save audio to temporary file for Whisper
            temp_file = "temp_wake_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            # Process with Whisper
            result = self.speech_processor.speech_to_text(temp_file)
            if result["success"]:
                text = result["text"].lower()
                if self.wake_detector.detect_wake_word(text):
                    self.logger.info(f"Wake word detected (Whisper): {text}")
                    self._activate_conversation_mode()
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            self.logger.error(f"Whisper fallback error: {e}")
    
    def _activate_conversation_mode(self):
        """Activate conversation mode after wake word"""
        if self.is_in_conversation:
            return  # Already in conversation
        
        self.is_in_conversation = True
        self.last_interaction = time.time()
        
        # Acknowledge activation
        asyncio.run(self._speak_activation_response())
        
        # Start conversation thread
        conversation_thread = threading.Thread(target=self._conversation_loop, daemon=True)
        conversation_thread.start()
    
    async def _speak_activation_response(self):
        """Speak activation acknowledgment"""
        responses = [
            "Yes, Mr. Stark?",
            "How can I assist you?", 
            "At your service, sir.",
            "Ready when you are.",
            "Yes, sir?"
        ]
        
        response = np.random.choice(responses)
        await self._speak_response(response)
    
    def _conversation_loop(self):
        """Main conversation loop"""
        self.logger.info("Conversation mode activated")
        
        while self.is_in_conversation and self.is_voice_enabled:
            try:
                # Check for conversation timeout
                if time.time() - self.last_interaction > self.conversation_timeout:
                    self.logger.info("Conversation timeout")
                    break
                
                # Listen for user input
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
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
        """Process audio during conversation"""
        try:
            # Save audio for Whisper processing
            temp_file = "temp_conversation_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            # Process with Whisper for better accuracy
            result = self.speech_processor.speech_to_text(temp_file)
            
            if result["success"]:
                user_input = result["text"]
                self.logger.info(f"User said: {user_input}")
                
                # Check for sleep commands
                if self.wake_detector.detect_sleep_command(user_input):
                    asyncio.run(self._speak_sleep_response())
                    self.disable_voice_interface()
                    return
                
                # Process the command
                self._process_user_command(user_input)
                self.last_interaction = time.time()
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            self.logger.error(f"Conversation processing error: {e}")
    
    async def _speak_sleep_response(self):
        """Speak sleep acknowledgment"""
        responses = [
            "Goodnight, Mr. Stark.",
            "Going to sleep mode.",
            "Powering down. Have a good day, sir.",
            "Standby mode activated.",
            "Until next time, Mr. Stark."
        ]
        
        response = np.random.choice(responses)
        await self._speak_response(response)
    
    def _process_user_command(self, user_input):
        """Process user voice command"""
        try:
            # Classify the command
            command_info = self.contextual_commands.classify_command(user_input)
            
            # Extract context
            context = self.contextual_commands.extract_context(command_info)
            
            # Analyze emotional state
            voice_chars = {"text": user_input}
            emotion = self.emotional_intelligence.analyze_voice_emotion(voice_chars)
            
            # Adapt personality if needed
            adaptive_personality = self.emotional_intelligence.get_adaptive_personality(emotion)
            if self.jarvis_ai and hasattr(self.jarvis_ai, 'switch_personality'):
                self.jarvis_ai.switch_personality(adaptive_personality)
            
            # Set appropriate voice
            self.speech_processor.set_personality_voice(adaptive_personality)
            
            # Process with JARVIS AI
            if self.jarvis_ai:
                response = self.jarvis_ai.chat(user_input)
                
                # Speak the response
                asyncio.run(self._speak_response(response))
            else:
                # Fallback response
                asyncio.run(self._speak_response("I'm here, but my core systems aren't connected yet."))
                
        except Exception as e:
            self.logger.error(f"Command processing error: {e}")
            asyncio.run(self._speak_response("I apologize, but I encountered an error processing that request."))
    
    async def _speak_response(self, text):
        """Convert text to speech and play"""
        try:
            # Generate speech
            result = await self.speech_processor.text_to_speech(text)
            
            if result["success"]:
                # Play the audio file
                self._play_audio_file(result["audio_file"])
                
                # Clean up
                if os.path.exists(result["audio_file"]):
                    os.remove(result["audio_file"])
            else:
                self.logger.error(f"TTS failed: {result.get('error')}")
                
        except Exception as e:
            self.logger.error(f"Speech response error: {e}")
    
    def _play_audio_file(self, audio_file):
        """Play audio file (cross-platform)"""
        try:
            import subprocess
            import platform
            
            system = platform.system()
            
            if system == "Windows":
                import winsound
                winsound.PlaySound(audio_file, winsound.SND_FILENAME)
            elif system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            else:  # Linux
                subprocess.run(["aplay", audio_file], check=True)
                
        except Exception as e:
            self.logger.error(f"Audio playback error: {e}")
    
    def get_status(self):
        """Get voice interface status"""
        return {
            "voice_enabled": self.is_voice_enabled,
            "listening_for_wake": self.is_listening_for_wake,
            "in_conversation": self.is_in_conversation,
            "last_interaction": self.last_interaction,
            "whisper_available": WHISPER_AVAILABLE,
            "edge_tts_available": EDGE_TTS_AVAILABLE,
            "pyaudio_available": PYAUDIO_AVAILABLE
        }


# Main functions for integration
def create_voice_interface(jarvis_ai=None):
    """Create and return voice interface instance"""
    return JarvisVoiceInterface(jarvis_ai)


def check_voice_requirements():
    """Check if all voice requirements are met"""
    requirements = {
        "whisper": WHISPER_AVAILABLE,
        "edge_tts": EDGE_TTS_AVAILABLE, 
        "pyaudio": PYAUDIO_AVAILABLE
    }
    
    all_available = all(requirements.values())
    
    return {
        "all_available": all_available,
        "requirements": requirements,
        "missing": [pkg for pkg, available in requirements.items() if not available]
    }


if __name__ == "__main__":
    # Test voice interface components
    print("🎤 JARVIS Voice Interface Test")
    print("=" * 50)
    
    # Check requirements
    req_check = check_voice_requirements()
    print(f"Requirements check: {req_check}")
    
    if req_check["all_available"]:
        print("✅ All requirements met!")
        
        # Test basic components
        wake_detector = IronManWakeWordDetector()
        print(f"Wake word test: {wake_detector.detect_wake_word('Hey JARVIS')}")
        
        speech_processor = FreeSpeechProcessor()
        print(f"TTS voices available: {list(speech_processor.tts_voices.keys())}")
        
    else:
        print(f"❌ Missing requirements: {req_check['missing']}")
        print("Install with: pip install " + " ".join(req_check['missing']))
