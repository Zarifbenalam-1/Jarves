# integration.py - Integration module for JARVIS components
# Connects the standalone optimization modules to the main AI engine

import os
import time
import importlib
import hashlib
import threading
from datetime import datetime

class JarvisIntegrator:
    """
    Integration manager for connecting JARVIS components
    
    This class serves as the bridge between:
    1. The main AI engine
    2. Memory Optimizer for performance
    3. Emotional Voice system
    4. Jesko GUI interface
    
    Designed for clean, modular integration that keeps components separate
    but allows them to work together seamlessly.
    """
    
    def __init__(self, main_engine=None):
        """Initialize the integrator with references to components"""
        self.main_engine = main_engine
        self.memory_optimizer = None
        self.emotional_voice = None
        self.jesko_gui = None
        
        # Integration status
        self.components_status = {
            "memory_optimizer": False,
            "emotional_voice": False,
            "jesko_gui": False
        }
        
        # Configuration
        self.config = {
            "aggressive_mode": False,  # Performance mode for 4GB RAM
            "use_voice": False,        # Voice interface enabled
            "use_gui": False,          # GUI interface enabled
            "auto_personality": False, # Auto personality switching
            "debug_mode": False        # Debugging output
        }
    
    def initialize_components(self):
        """Initialize all available components"""
        # Initialize Memory Optimizer
        self._init_memory_optimizer()
        
        # Initialize Voice (if enabled)
        if self.config["use_voice"]:
            self._init_emotional_voice()
        
        # Initialize GUI (if enabled)
        if self.config["use_gui"]:
            self._init_jesko_gui()
        
        return self.get_status()
    
    def _init_memory_optimizer(self):
        """Initialize the Memory Optimizer component"""
        try:
            # Dynamic import to avoid circular imports
            from assistant.memory_optimizer import MemoryOptimizer
            
            # Create Memory Optimizer with appropriate settings
            self.memory_optimizer = MemoryOptimizer(
                aggressive_mode=self.config["aggressive_mode"]
            )
            
            self.components_status["memory_optimizer"] = True
            
            if self.config["debug_mode"]:
                print("✅ Memory Optimizer initialized")
                
            return True
        except ImportError:
            print("❌ Memory Optimizer module not found")
            return False
        except Exception as e:
            print(f"❌ Error initializing Memory Optimizer: {str(e)}")
            return False
    
    def _init_emotional_voice(self):
        """Initialize the Emotional Voice component"""
        try:
            # Dynamic import to avoid circular imports
            from assistant.emotional_voice import EmotionalVoiceEngine
            
            # Create Emotional Voice Engine
            self.emotional_voice = EmotionalVoiceEngine()
            
            self.components_status["emotional_voice"] = True
            
            if self.config["debug_mode"]:
                print("✅ Emotional Voice initialized")
                
            return True
        except ImportError:
            print("❌ Emotional Voice module not found")
            return False
        except Exception as e:
            print(f"❌ Error initializing Emotional Voice: {str(e)}")
            return False
    
    def _init_jesko_gui(self):
        """Initialize the Jesko GUI component"""
        try:
            # Dynamic import to avoid circular imports
            from assistant.jesko_gui import JeskoGUI
            
            # Create Jesko GUI
            self.jesko_gui = JeskoGUI()
            self.jesko_gui.initialize(aggressive_mode=self.config["aggressive_mode"])
            
            self.components_status["jesko_gui"] = True
            
            if self.config["debug_mode"]:
                print("✅ Jesko GUI initialized")
                
            return True
        except ImportError:
            print("❌ Jesko GUI module not found")
            return False
        except Exception as e:
            print(f"❌ Error initializing Jesko GUI: {str(e)}")
            return False
    
    def get_status(self):
        """Get integration status of all components"""
        return {
            "components": self.components_status,
            "config": self.config,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def set_config(self, **kwargs):
        """Update configuration settings"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        # Re-initialize components if needed
        if "aggressive_mode" in kwargs:
            self._init_memory_optimizer()
        
        if "use_voice" in kwargs and kwargs["use_voice"] != self.config["use_voice"]:
            if kwargs["use_voice"]:
                self._init_emotional_voice()
                
        if "use_gui" in kwargs and kwargs["use_gui"] != self.config["use_gui"]:
            if kwargs["use_gui"]:
                self._init_jesko_gui()
    
    # =========== MEMORY OPTIMIZATION INTEGRATION ===========
    
    def optimize_conversation(self, conversation_history):
        """Optimize conversation history using Memory Optimizer"""
        if not self.memory_optimizer:
            return conversation_history
            
        return self.memory_optimizer.optimize_conversation_history(conversation_history)
    
    def cache_response(self, query, response):
        """Cache a response for faster retrieval"""
        if not self.memory_optimizer:
            return
            
        # Create a hash of the query for caching
        query_hash = hashlib.md5(query.encode()).hexdigest()
        self.memory_optimizer.cache_response(query_hash, response)
    
    def get_cached_response(self, query):
        """Get a cached response if available"""
        if not self.memory_optimizer:
            return None
            
        # Create a hash of the query for cache lookup
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return self.memory_optimizer.get_cached_response(query_hash)
    
    def cleanup_memory(self):
        """Trigger memory cleanup"""
        if not self.memory_optimizer:
            return
            
        return self.memory_optimizer.cleanup_memory()
    
    def select_optimal_model(self, query, available_models, user_preferences=None):
        """Select the optimal model for a query based on complexity and RAM"""
        if not self.memory_optimizer:
            return available_models[0] if available_models else None
            
        return self.memory_optimizer.smart_model_selector(query, available_models, user_preferences)
    
    # =========== EMOTIONAL VOICE INTEGRATION ===========
    
    def speak_with_emotion(self, text, personality_mode=None, callback=None):
        """Speak text with appropriate emotional adaptation"""
        if not self.emotional_voice:
            return False
            
        self.emotional_voice.speak(text, personality_mode, callback)
        return True
    
    def detect_emotion_from_text(self, text):
        """Detect emotion from text"""
        if not self.emotional_voice:
            return "neutral"
            
        return self.emotional_voice.detect_emotion(text)
    
    def stop_speaking(self):
        """Stop current speech"""
        if not self.emotional_voice:
            return False
            
        self.emotional_voice.stop_speaking()
        return True
    
    # =========== JESKO GUI INTEGRATION ===========
    
    def create_gui(self):
        """Create and initialize the GUI"""
        if not self.jesko_gui:
            self._init_jesko_gui()
            
        if not self.jesko_gui:
            return None
            
        window = self.jesko_gui.create_main_window()
        self.jesko_gui.create_chat_interface()
        return window
    
    def display_message(self, message, is_user=True):
        """Display a message in the GUI"""
        if not self.jesko_gui:
            return False
            
        self.jesko_gui.add_message(message, is_user)
        return True
    
    def run_gui(self):
        """Run the GUI main loop"""
        if not self.jesko_gui:
            return False
            
        # Run in a separate thread to not block the main thread
        gui_thread = threading.Thread(target=self.jesko_gui.run)
        gui_thread.daemon = True
        gui_thread.start()
        return True
    
    def set_gui_theme(self, variant):
        """Set the GUI theme variant"""
        if not self.jesko_gui:
            return False
            
        self.jesko_gui.set_theme_variant(variant)
        return True


# Example usage
if __name__ == "__main__":
    integrator = JarvisIntegrator()
    integrator.set_config(aggressive_mode=True, use_gui=True, debug_mode=True)
    integrator.initialize_components()
    
    # Test the integration
    if integrator.components_status["memory_optimizer"]:
        print("Memory Optimizer: Available")
        
    if integrator.components_status["jesko_gui"]:
        print("Jesko GUI: Available")
        window = integrator.create_gui()
        integrator.display_message("Testing JARVIS Integration", is_user=True)
        integrator.display_message("All systems operational, Sir.", is_user=False)
