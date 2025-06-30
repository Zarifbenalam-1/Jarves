# 🔧 JARVIS-X CONFIGURATION GUIDE

**Complete guide to customize JARVIS-X storage, emotional detection, and advanced features**

---

## 📂 **STORAGE CONFIGURATION**

### **Changing Storage Locations**

**File:** `assistant/ai_engine.py` (Lines ~15-20)

```python
class JarvisAI:
    def __init__(self):
        # BOSS: Change these paths to your preferred locations
        self.memory_dir = "memory"                    # ← Change this line
        self.conversation_file = "conversation_history.json"  # ← And this
        self.preferences_file = "user_preferences.json"       # ← And this
```

### **Example Configurations:**

**Option 1: Move to D Drive**
```python
self.memory_dir = r"D:\JARVIS_Data"
self.conversation_file = "conversations.json"
self.preferences_file = "settings.json"
```

**Option 2: Cloud Folder (OneDrive/Google Drive)**
```python
self.memory_dir = r"C:\Users\YourName\OneDrive\JARVIS_Memory"
self.conversation_file = "jarvis_conversations.json"
self.preferences_file = "jarvis_preferences.json"
```

**Option 3: Portable USB Drive**
```python
self.memory_dir = r"E:\JARVIS_Portable"  # USB drive
self.conversation_file = "portable_conversations.json"
self.preferences_file = "portable_settings.json"
```

### **Important Notes:**
- Use raw strings (`r"path"`) for Windows paths
- Create the folder manually if it doesn't exist
- JARVIS will automatically create the JSON files

---

## 🎭 **EMOTIONAL DETECTION SYSTEM**

### **How It Works:**
JARVIS analyzes your text input to detect emotional state and adapts responses accordingly.

### **Emotional States Detected:**
- **😤 Frustrated/Angry**: Detected from "!!!", "wtf", "seriously", "come on"
- **🤔 Curious/Learning**: Detected from "?", "how", "why", "what"
- **💼 Formal/Professional**: Detected from "please", "would you", "could you kindly"
- **😊 Excited/Happy**: Detected from "awesome", "great", "love", "amazing"
- **😔 Tired/Sad**: Detected from "tired", "exhausted", "sad", "depressed"

### **Emotional Voice Adaptation:**
```python
# File: assistant/ai_engine.py (Koenigsegg Jesko Voice System)
class EmotionalVoiceEngine:
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
```

### **Customizing Emotional Triggers:**
**File:** `assistant/ai_engine.py` (Lines ~400-450)

```python
# Add your custom emotional triggers here
CUSTOM_EMOTIONS = {
    'excited': ['awesome', 'fantastic', 'incredible', 'amazing'],
    'frustrated': ['annoying', 'stupid', 'ridiculous', 'hate'],
    'curious': ['interesting', 'wondering', 'curious', 'explain']
}
```

---

## 🏎️ **KOENIGSEGG JESKO GUI THEME**

### **Dark Carbon Fiber Theme**
The GUI is inspired by the elegant and powerful Koenigsegg Jesko hypercar, featuring a deep black carbon fiber look with sharp orange accents.

```python
# File: assistant/gui.py
class JeskoGUI:
    def __init__(self):
        self.theme = {
            'bg_color': '#0A0A0A',           # Jesko carbon black
            'accent_color': '#FF6B35',       # Jesko orange
            'panel_color': '#1A1A1A',        # Dark panels
            'text_color': '#FFFFFF',         # Pure white
            'success_color': '#00FF88',      # Neon green for success
            'warning_color': '#FFD700',      # Gold for warnings
            'font_family': 'Consolas',       # Clean, technical font
            'window_style': 'borderless',    # Sleek like Jesko
        }
```

### **Customizing the Jesko Theme**
You can adjust the color scheme to match different Koenigsegg models:

```python
# Jesko Absolut Theme (Silver/Blue)
self.theme = {
    'bg_color': '#131313',           # Dark gray
    'accent_color': '#00A8E0',       # Electric blue
    'panel_color': '#1F1F1F',        # Medium gray
    'text_color': '#FFFFFF',         # White
}

# Jesko Attack Theme (Red/Black)
self.theme = {
    'bg_color': '#0A0A0A',           # Deep black
    'accent_color': '#FF3333',       # Aggressive red
    'panel_color': '#1A1A1A',        # Dark gray
    'text_color': '#FFFFFF',         # White
}
```

---

## 🚀 **PERFORMANCE OPTIMIZATION SETTINGS**

### **Memory Limits (4GB RAM Optimization)**
**File:** `assistant/ai_engine.py` (Lines ~50-60)

```python
class MemoryOptimizer:
    def __init__(self, max_conversation_size=800, cache_size=300, aggressive_mode=False):
        # PERFORMANCE BEAST MODE: Optimized for 4GB RAM laptops
        self.max_conversation_size = max_conversation_size  # Lower for less RAM usage
        self.cache_size = cache_size                        # Smaller cache for memory saving
        self.memory_cleanup_interval = 50                   # More frequent cleanup
        self.aggressive_mode = aggressive_mode              # Ultra performance mode
        self.conversation_chunks = deque(maxlen=10)         # Keep only 10 chunks
        self.interaction_count = 0                          # Track interactions for cleanup
```

### **Performance Beast Mode Options**

For extremely low RAM systems (2-4GB), use these settings:

```python
# Ultra-Lightweight Mode (i3 7th gen friendly)
memory_optimizer = MemoryOptimizer(
    max_conversation_size=400,    # Half the default
    cache_size=100,               # Minimal cache
    aggressive_mode=True          # Maximum optimization
)
```
        self.max_model_cache = 2          # Max cached model responses
```

### **Model Performance Settings**
```python
# Fast models for quick responses
SPEED_MODELS = ['llama-3.1-8b', 'phi-3-mini']
# Smart models for complex tasks  
INTELLIGENCE_MODELS = ['llama-3.1-70b', 'claude-3-haiku']
```

---

## 🎨 **GUI THEME CONFIGURATION**

### **Koenigsegg Jesko Theme Colors**
**File:** `assistant/gui.py` (Future Implementation)

```python
JESKO_THEME = {
    'primary_color': '#0A0A0A',        # Deep black carbon fiber
    'accent_color': '#FF6B35',         # Jesko orange highlights
    'secondary': '#1A1A1A',           # Dark gray panels
    'text_color': '#FFFFFF',          # Pure white text
    'success_color': '#00FF88',       # Neon green for success
    'warning_color': '#FFD700',       # Gold for warnings
    'error_color': '#FF4444',         # Red for errors
    'font_family': 'Consolas',        # Technical font
    'font_size': 12,                  # Base font size
}
```

### **Custom Theme Creation:**
```python
# Create your own theme
CUSTOM_THEME = {
    'primary_color': '#YourColor',     # Main background
    'accent_color': '#YourAccent',     # Buttons and highlights
    'text_color': '#YourText',         # Text color
    'font_family': 'YourFont',         # Font family
}
```

---

## 🔄 **FUTURE CONFIGURATION OPTIONS**

### **Voice Settings (Coming Soon)**
```python
VOICE_CONFIG = {
    'voice_speed': 1.0,               # Speech rate (0.5-2.0)
    'voice_pitch': 1.0,               # Voice pitch (0.5-2.0)
    'voice_volume': 1.0,              # Volume level (0.0-1.0)
    'emotional_adaptation': True,      # Enable emotional voice
    'personality_voices': True,        # Different voices per personality
}
```

### **Advanced Learning Settings**
```python
LEARNING_CONFIG = {
    'pattern_recognition': True,       # Learn user patterns
    'preference_adaptation': True,     # Adapt to preferences
    'context_memory': True,           # Remember conversation context
    'predictive_suggestions': True,    # Predict user needs
}
```

---

## 📝 **QUICK REFERENCE**

### **Most Common Changes:**
1. **Change Storage Location**: Line ~17 in `ai_engine.py`
2. **Modify Emotional Triggers**: Line ~400 in `ai_engine.py`
3. **Adjust Memory Limits**: Line ~50 in `ai_engine.py`
4. **Customize Theme Colors**: `gui.py` (when implemented)

### **After Making Changes:**
1. Save the file
2. Restart JARVIS
3. Test the new configuration
4. Check for any errors in the console

---

**Boss, this guide will be updated as we add more features! 🚀**
