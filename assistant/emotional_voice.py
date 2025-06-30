# emotional_voice.py - Jesko-inspired voice engine for JARVIS

import time
import random
import threading

class EmotionalVoiceEngine:
    """
    Koenigsegg Jesko-inspired voice system for JARVIS
    Adapts voice characteristics based on detected emotional state
    Optimized for performance on low-RAM systems
    """
    
    def __init__(self):
        # Jesko-inspired voice profiles - sleek, powerful, responsive
        self.voice_personalities = {
            'excited': {'rate': 1.2, 'pitch': 1.1, 'volume': 1.1},
            'focused': {'rate': 1.0, 'pitch': 1.0, 'volume': 1.0},
            'tired': {'rate': 0.9, 'pitch': 0.9, 'volume': 0.9},
            'frustrated': {'rate': 1.1, 'pitch': 0.95, 'volume': 1.05},
            'formal': {'rate': 0.95, 'pitch': 0.98, 'volume': 1.0},
            'jesko_sport': {'rate': 1.15, 'pitch': 1.05, 'volume': 1.1},  # Performance mode
            'jesko_cruise': {'rate': 0.98, 'pitch': 1.0, 'volume': 1.0}   # Elegant mode
        }
        
        self.current_emotion = 'focused'
        self.tts_engine = None
        self.is_speaking = False
        self.voice_queue = []
    
    def detect_emotion(self, text):
        """
        Detect emotional state from text
        Optimized for speed on low-RAM systems
        """
        text_lower = text.lower()
        
        # Emotion patterns (lightweight implementation)
        emotion_patterns = {
            'excited': ['!', 'wow', 'amazing', 'awesome', 'great', 'love'],
            'frustrated': ['wtf', 'stupid', 'annoying', 'ridiculous', 'hate', '!!!'],
            'tired': ['tired', 'sleepy', 'exhausted', 'late', 'long day'],
            'formal': ['please', 'would you', 'kindly', 'appreciate', 'thank you'],
            'jesko_sport': ['hurry', 'quickly', 'fast', 'speed', 'asap', 'now']
        }
        
        # Count emotion indicators
        emotion_scores = {'focused': 1}  # Default score
        
        for emotion, patterns in emotion_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Add question mark detection
        if '?' in text:
            emotion_scores['focused'] = emotion_scores.get('focused', 0) + 1
        
        # Add exclamation detection
        exclamation_count = text.count('!')
        if exclamation_count > 2:
            emotion_scores['excited'] = emotion_scores.get('excited', 0) + 2
        elif exclamation_count > 0:
            emotion_scores['excited'] = emotion_scores.get('excited', 0) + 1
        
        # Return highest scoring emotion
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def adapt_voice(self, text, personality_mode=None):
        """
        Adapt voice characteristics based on text content and personality mode
        """
        # Detect emotion from text
        detected_emotion = self.detect_emotion(text)
        
        # Adjust based on personality mode
        if personality_mode:
            if personality_mode == 'unleashed':
                detected_emotion = 'jesko_sport'
            elif personality_mode == 'professional':
                detected_emotion = 'formal'
            elif personality_mode == 'sarcastic':
                # Add slight sarcastic variation to whatever emotion we detected
                current_profile = self.voice_personalities.get(detected_emotion, 
                                                              self.voice_personalities['focused'])
                return {
                    'rate': current_profile['rate'] * 0.95,
                    'pitch': current_profile['pitch'] * 1.05,
                    'volume': current_profile['volume']
                }
        
        # Store current emotion
        self.current_emotion = detected_emotion
        
        # Return voice profile for the emotion
        return self.voice_personalities.get(detected_emotion, self.voice_personalities['focused'])
    
    def initialize_tts_engine(self):
        """
        Initialize text-to-speech engine (lazy loading to save memory)
        Uses Edge TTS for free, high-quality voices
        """
        try:
            # Lazy import to save memory when not in use
            import edge_tts
            self.tts_engine = 'edge_tts'
            return True
        except ImportError:
            try:
                # Fallback to pyttsx3 if edge_tts not available
                import pyttsx3
                self.tts_engine = 'pyttsx3'
                return True
            except ImportError:
                print("No TTS engine available. Install edge_tts or pyttsx3.")
                return False
    
    def speak(self, text, personality_mode=None, callback=None):
        """
        Speak text with emotional adaptation
        Non-blocking implementation for responsive UI
        """
        if not self.tts_engine and not self.initialize_tts_engine():
            print("TTS engine not available.")
            if callback:
                callback()
            return
        
        # Get voice parameters based on emotion
        voice_profile = self.adapt_voice(text, personality_mode)
        
        # Add to voice queue
        self.voice_queue.append({
            'text': text,
            'profile': voice_profile,
            'callback': callback
        })
        
        # Start speaking thread if not already speaking
        if not self.is_speaking:
            threading.Thread(target=self._process_voice_queue).start()
    
    def _process_voice_queue(self):
        """Process the voice queue in a separate thread"""
        self.is_speaking = True
        
        while self.voice_queue:
            item = self.voice_queue.pop(0)
            text = item['text']
            profile = item['profile']
            callback = item['callback']
            
            try:
                self._speak_text(text, profile)
            except Exception as e:
                print(f"TTS Error: {e}")
            
            if callback:
                callback()
        
        self.is_speaking = False
    
    def _speak_text(self, text, profile):
        """
        Actual text-to-speech implementation
        Optimized for low resource usage
        """
        if self.tts_engine == 'edge_tts':
            self._speak_with_edge_tts(text, profile)
        elif self.tts_engine == 'pyttsx3':
            self._speak_with_pyttsx3(text, profile)
    
    def _speak_with_edge_tts(self, text, profile):
        """Use Edge TTS for speech (free, high quality)"""
        try:
            import edge_tts
            import asyncio
            
            async def _edge_tts_speak():
                voice = "en-US-GuyNeural"  # Male voice like JARVIS
                
                # Apply voice profile
                rate = str(int((profile['rate'] - 1.0) * 100)) + "%"
                pitch = str(int((profile['pitch'] - 1.0) * 100)) + "Hz"
                volume = str(int(profile['volume'] * 100)) + "%"
                
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save("temp_speech.mp3", 
                                      rate=rate,
                                      volume=volume, 
                                      pitch=pitch)
                
                # Play the audio
                from playsound import playsound
                playsound("temp_speech.mp3")
                
                # Clean up temp file
                import os
                if os.path.exists("temp_speech.mp3"):
                    os.remove("temp_speech.mp3")
            
            # Run async function
            asyncio.run(_edge_tts_speak())
            
        except Exception as e:
            print(f"Edge TTS error: {e}")
    
    def _speak_with_pyttsx3(self, text, profile):
        """Fallback to pyttsx3 when Edge TTS not available"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Apply voice profile
            engine.setProperty('rate', 150 * profile['rate'])
            engine.setProperty('volume', profile['volume'])
            
            # Use the first male voice available
            voices = engine.getProperty('voices')
            for voice in voices:
                if "male" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"pyttsx3 error: {e}")
    
    def stop_speaking(self):
        """Stop all speech and clear queue"""
        self.voice_queue = []
        # Additional engine-specific stop methods would be here
