# memory_optimizer.py - DEVIL MIND Memory Optimization for 4GB RAM

import gc
import time
import os
import json
from collections import deque
import threading

class MemoryOptimizer:
    """
    DEVIL MIND Memory Optimization for 4GB RAM
    Boss's laptop-friendly memory management system
    
    Features:
    - Smart conversation chunking
    - Response caching system
    - Aggressive garbage collection
    - Low RAM mode for i3 processors
    - Memory usage monitoring
    """
    def __init__(self, max_conversation_size=800, cache_size=300, aggressive_mode=False):
        self.max_conversation_size = max_conversation_size
        self.response_cache = {}
        self.cache_size = cache_size
        self.memory_cleanup_interval = 50  # Clean every 50 interactions
        self.interaction_count = 0
        self.conversation_chunks = deque(maxlen=10)  # Keep last 10 chunks
        self.aggressive_mode = aggressive_mode  # Ultra performance mode
        self.last_full_gc_time = time.time()
        self.gc_full_interval = 300  # Full GC every 5 minutes
        self.memory_warning_threshold = 85  # Percentage
        
        # Start memory monitor thread if in aggressive mode
        if aggressive_mode:
            self.monitor_thread = threading.Thread(target=self._memory_monitor, daemon=True)
            self.monitor_thread.start()
        
    def optimize_conversation_history(self, conversation_history):
        """Smart conversation chunking for memory efficiency"""
        if len(conversation_history) <= self.max_conversation_size:
            return conversation_history
            
        # Keep recent conversations and important ones
        recent_conversations = conversation_history[-self.max_conversation_size // 2:]
        
        # Find important conversations (questions, commands, etc.)
        important_conversations = []
        for msg in conversation_history[:-self.max_conversation_size // 2]:
            # Keep messages with questions or commands as they might be referenced later
            if msg.get("role") == "user" and (
                "?" in msg.get("content", "") or 
                any(cmd in msg.get("content", "").lower() for cmd in 
                    ["how", "what", "why", "could", "would", "please", "help"])
            ):
                important_conversations.append(msg)
        
        # Archive older conversations to chunks
        if len(conversation_history) > self.max_conversation_size:
            chunk = conversation_history[:-self.max_conversation_size // 2]
            self.conversation_chunks.append(chunk)
            
        # Combine recent and important conversations
        optimized_history = important_conversations + recent_conversations
        
        # If still too large, trim more aggressively
        if self.aggressive_mode and len(optimized_history) > self.max_conversation_size:
            return optimized_history[-self.max_conversation_size:]
        
        return optimized_history
    
    def cache_response(self, query_hash, response):
        """Cache responses for instant retrieval"""
        if len(self.response_cache) >= self.cache_size:
            # Remove oldest cached response
            oldest_key = min(
                self.response_cache.items(), 
                key=lambda x: x[1]['timestamp']
            )[0]
            del self.response_cache[oldest_key]
            
        self.response_cache[query_hash] = {
            'response': response,
            'timestamp': time.time(),
            'access_count': 1,
            'last_accessed': time.time()
        }
    
    def get_cached_response(self, query_hash):
        """Get cached response if available"""
        if query_hash in self.response_cache:
            cache_entry = self.response_cache[query_hash]
            cache_entry['access_count'] += 1
            cache_entry['last_accessed'] = time.time()
            return cache_entry['response']
        return None
    
    def cleanup_memory(self):
        """Aggressive memory cleanup for low-RAM systems"""
        self.interaction_count += 1
        current_time = time.time()
        
        # Standard cleanup interval
        if self.interaction_count % self.memory_cleanup_interval == 0:
            # Force garbage collection (generation 0 only for speed)
            gc.collect(0)
            
            # Clean old cache entries
            expired_keys = []
            
            for key, cache_entry in self.response_cache.items():
                # Remove entries older than 1 hour with low access count
                if (current_time - cache_entry['timestamp'] > 3600 and 
                    cache_entry['access_count'] < 3):
                    expired_keys.append(key)
            
            # Actually remove the expired keys
            for key in expired_keys:
                del self.response_cache[key]
                
            # Check if full garbage collection is needed
            if current_time - self.last_full_gc_time > self.gc_full_interval:
                # Full system garbage collection (all generations)
                gc.collect(2)
                self.last_full_gc_time = current_time
                
        # Aggressive mode for extremely low memory systems
        if self.aggressive_mode:
            # More aggressive cache pruning
            if len(self.response_cache) > self.cache_size * 0.8:  # 80% full
                # Sort by access count and remove least used 20%
                sorted_cache = sorted(
                    self.response_cache.items(),
                    key=lambda x: x[1]['access_count']
                )
                # Remove bottom 20%
                items_to_remove = int(len(sorted_cache) * 0.2)
                for i in range(items_to_remove):
                    if i < len(sorted_cache):
                        del self.response_cache[sorted_cache[i][0]]
                        
        # Return stats about memory cleanup
        return {
            "cache_size": len(self.response_cache),
            "expired_keys_removed": len(expired_keys) if 'expired_keys' in locals() else 0,
            "aggressive_mode": self.aggressive_mode
        }
    
    def get_memory_stats(self):
        """Get memory usage statistics"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            return {
                "ram_usage_mb": memory_info.rss / 1024 / 1024,
                "cache_size": len(self.response_cache),
                "conversation_chunks": len(self.conversation_chunks)
            }
        except ImportError:
            return {
                "ram_usage": "psutil not installed",
                "cache_size": len(self.response_cache),
                "conversation_chunks": len(self.conversation_chunks)
            }
    
    def _memory_monitor(self):
        """Background thread to monitor memory usage and perform cleanup when needed"""
        try:
            import psutil
            while True:
                # Check every 30 seconds
                time.sleep(30)
                
                # Get current memory usage
                process = psutil.Process(os.getpid())
                memory_percent = process.memory_percent()
                
                # If memory usage is high, perform aggressive cleanup
                if memory_percent > self.memory_warning_threshold:
                    print(f"Memory usage high ({memory_percent:.1f}%) - performing aggressive cleanup")
                    # Full garbage collection
                    gc.collect(2)
                    
                    # Clear as much cache as possible
                    if len(self.response_cache) > self.cache_size * 0.5:
                        # Sort by access time and remove oldest 50%
                        sorted_cache = sorted(
                            self.response_cache.items(),
                            key=lambda x: x[1]['last_accessed']
                        )
                        # Remove oldest 50%
                        items_to_remove = int(len(sorted_cache) * 0.5)
                        for i in range(items_to_remove):
                            if i < len(sorted_cache):
                                del self.response_cache[sorted_cache[i][0]]
        except ImportError:
            # If psutil not available, disable memory monitor
            pass
        except Exception as e:
            print(f"Memory monitor error: {e}")
    
    def smart_model_selector(self, query, available_models, user_preferences=None):
        """
        DEVIL MIND Smart Model Selector - Choose the right model for each query
        
        Balances between speed and intelligence based on:
        1. Query complexity
        2. Available RAM 
        3. Response time needs
        4. User preferences
        """
        # Default models
        fast_models = ["Llama-3.1 8B (OpenRouter)", "GPT-3.5 Turbo (OpenAI)", "Phi-3-mini (OpenRouter)"]
        smart_models = ["Llama-3.1 70B (OpenRouter)", "Claude 3 Haiku (OpenRouter)", "GPT-4o Mini (OpenAI)"]
        
        # User preferred models take priority if specified
        if user_preferences and 'preferred_models' in user_preferences:
            preferred = user_preferences['preferred_models']
            if preferred and preferred[0] in available_models:
                return preferred[0]
        
        # Simple complexity estimation
        query_lower = query.lower()
        
        # Check query length (longer queries may need smarter models)
        query_length = len(query)
        
        # Check for complexity indicators
        complexity_indicators = [
            "explain", "analyze", "compare", "difference between", 
            "how does", "why does", "implications", "consequences"
        ]
        
        complexity_score = sum(2 for indicator in complexity_indicators 
                              if indicator in query_lower)
        
        # Adjust for query length
        if query_length > 200:
            complexity_score += 3
        elif query_length > 100:
            complexity_score += 2
        elif query_length > 50:
            complexity_score += 1
            
        # Check for code-related queries (need smarter models)
        code_indicators = [
            "code", "function", "class", "implement", "algorithm",
            "programming", "syntax", "bug", "error", "debug"
        ]
        
        code_score = sum(2 for indicator in code_indicators 
                        if indicator in query_lower)
        complexity_score += code_score
        
        # Check system resources - use fast model if memory is constrained
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            if memory_percent > 80:  # High memory usage
                # Force fast model
                for model in fast_models:
                    if model in available_models:
                        return model
        except ImportError:
            pass
            
        # Make decision - higher complexity score means smarter model
        if complexity_score > 5:
            # Use smart model
            for model in smart_models:
                if model in available_models:
                    return model
        else:
            # Use fast model
            for model in fast_models:
                if model in available_models:
                    return model
                    
        # Fallback to any available model
        return list(available_models)[0] if available_models else None
