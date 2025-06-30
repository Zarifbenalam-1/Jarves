# ai_engine_integration.py
# Helper module to integrate Performance Beast Mode and other components into the main AI engine
# This patch can be applied to ai_engine.py without rewriting the entire file

import os
import re
import hashlib
from datetime import datetime

def integrate_performance_beast(ai_instance, use_aggressive_mode=False):
    """
    Integrate Performance Beast Mode components into an existing JarvisAI instance
    
    Args:
        ai_instance: The JarvisAI instance to enhance
        use_aggressive_mode: Enable extreme optimization for very low RAM systems
        
    Returns:
        Enhanced JarvisAI instance with Beast Mode capabilities
    """
    try:
        from assistant.integration import JarvisIntegrator
        
        # Create integrator with appropriate configuration
        integrator = JarvisIntegrator(main_engine=ai_instance)
        integrator.set_config(
            aggressive_mode=use_aggressive_mode,
            debug_mode=True
        )
        
        # Initialize the optimizer
        integrator.initialize_components()
        
        # Inject integrator into the AI engine
        ai_instance._integrator = integrator
        
        # Enhance methods with Beast Mode capabilities
        _enhance_chat_method(ai_instance)
        _enhance_memory_system(ai_instance)
        _enhance_model_selection(ai_instance)
        
        # Add Beast Mode capabilities
        ai_instance.beast_mode_enabled = True
        ai_instance.get_memory_stats = integrator.memory_optimizer.get_memory_stats
        
        print("🔥 PERFORMANCE BEAST MODE ACTIVATED 🔥")
        return ai_instance
        
    except ImportError as e:
        print(f"Failed to integrate Performance Beast Mode: {e}")
        return ai_instance
    except Exception as e:
        print(f"Error during Performance Beast integration: {e}")
        return ai_instance

def _enhance_chat_method(ai_instance):
    """Enhance the chat method with response caching and optimization"""
    original_chat = ai_instance.chat
    
    def enhanced_chat(message, system_prompt=None):
        # Get cached response if available
        cached_response = ai_instance._integrator.get_cached_response(message)
        if cached_response:
            # Add to conversation history but skip API call
            ai_instance.conversation_history.append({"role": "user", "content": message})
            ai_instance.conversation_history.append({"role": "assistant", "content": cached_response})
            ai_instance._save_conversation_history()
            return cached_response
        
        # No cache hit, use original method
        response = original_chat(message, system_prompt)
        
        # Cache the response for future use
        if not response.startswith("Error:"):
            ai_instance._integrator.cache_response(message, response)
        
        # Run memory cleanup periodically
        ai_instance._integrator.cleanup_memory()
        
        return response
    
    # Replace the method
    ai_instance.chat = enhanced_chat

def _enhance_memory_system(ai_instance):
    """Enhance the memory system with optimization"""
    original_save_history = ai_instance._save_conversation_history
    
    def optimized_save_history():
        # Optimize conversation before saving
        if hasattr(ai_instance, '_integrator') and ai_instance._integrator.memory_optimizer:
            ai_instance.conversation_history = ai_instance._integrator.optimize_conversation(
                ai_instance.conversation_history
            )
        
        # Call original method
        original_save_history()
    
    # Replace the method
    ai_instance._save_conversation_history = optimized_save_history

def _enhance_model_selection(ai_instance):
    """Enhance model selection with smart switching"""
    
    def smart_model_switch(message, user_preferences=None):
        """Automatically select the best model based on query complexity"""
        if not hasattr(ai_instance, '_integrator'):
            return ai_instance.current_model
            
        available_models = list(ai_instance.available_models.keys())
        optimal_model = ai_instance._integrator.select_optimal_model(
            message, 
            available_models, 
            user_preferences
        )
        
        # Only switch if different from current
        if optimal_model and optimal_model != ai_instance.current_model:
            old_model = ai_instance.current_model
            ai_instance.current_model = optimal_model
            return optimal_model
            
        return ai_instance.current_model
    
    # Add new method
    ai_instance.smart_model_switch = smart_model_switch

def integrate_voice_system(ai_instance):
    """
    Integrate the Emotional Voice system into the AI engine
    
    Args:
        ai_instance: The JarvisAI instance to enhance
        
    Returns:
        Enhanced JarvisAI instance with voice capabilities
    """
    try:
        # Make sure integrator is initialized
        if not hasattr(ai_instance, '_integrator'):
            from assistant.integration import JarvisIntegrator
            ai_instance._integrator = JarvisIntegrator(main_engine=ai_instance)
        
        # Enable and initialize voice
        ai_instance._integrator.set_config(use_voice=True)
        ai_instance._integrator.initialize_components()
        
        # Add voice methods to the AI engine
        ai_instance.speak = lambda text, personality=None: ai_instance._integrator.speak_with_emotion(
            text, 
            ai_instance.personality_mode if personality is None else personality
        )
        
        ai_instance.stop_speaking = ai_instance._integrator.stop_speaking
        ai_instance.detect_emotion = ai_instance._integrator.detect_emotion_from_text
        
        print("🎤 EMOTIONAL VOICE SYSTEM ACTIVATED 🎤")
        return ai_instance
        
    except Exception as e:
        print(f"Error during Voice System integration: {e}")
        return ai_instance

def integrate_jesko_gui(ai_instance):
    """
    Integrate the Koenigsegg Jesko GUI into the AI engine
    
    Args:
        ai_instance: The JarvisAI instance to enhance
        
    Returns:
        Enhanced JarvisAI instance with GUI capabilities
    """
    try:
        # Make sure integrator is initialized
        if not hasattr(ai_instance, '_integrator'):
            from assistant.integration import JarvisIntegrator
            ai_instance._integrator = JarvisIntegrator(main_engine=ai_instance)
        
        # Enable and initialize GUI
        ai_instance._integrator.set_config(use_gui=True)
        ai_instance._integrator.initialize_components()
        
        # Create GUI
        window = ai_instance._integrator.create_gui()
        
        # Add GUI methods to the AI engine
        ai_instance.display_message = ai_instance._integrator.display_message
        ai_instance.set_gui_theme = ai_instance._integrator.set_gui_theme
        ai_instance.run_gui = ai_instance._integrator.run_gui
        
        # Enhance chat method to display messages in GUI
        _enhance_chat_with_gui(ai_instance)
        
        print("🏎️ KOENIGSEGG JESKO GUI ACTIVATED 🏎️")
        return ai_instance
        
    except Exception as e:
        print(f"Error during Jesko GUI integration: {e}")
        return ai_instance

def _enhance_chat_with_gui(ai_instance):
    """Add GUI updates to chat method"""
    if not hasattr(ai_instance, 'display_message'):
        return
    
    original_chat = ai_instance.chat
    
    def chat_with_gui(message, system_prompt=None):
        # Display user message in GUI
        ai_instance.display_message(message, is_user=True)
        
        # Get response
        response = original_chat(message, system_prompt)
        
        # Display AI response in GUI
        ai_instance.display_message(response, is_user=False)
        
        return response
    
    # Replace the method
    ai_instance.chat = chat_with_gui
