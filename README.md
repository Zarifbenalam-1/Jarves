# JARVIS: Your Iron Man AI Assistant

**Personal AI with Absolute Loyalty, Permanent Memory & Advanced Intelligence**

---

## 🤖 What is JARVIS?

JARVIS is your sophisticated AI assistant that **recognizes you as the master** and provides intelligent, witty assistance with complete obedience. Built with persistent memory, advanced learning capabilities, and refined for practical use.

### 🎯 Key Features:
- **👑 Master Recognition**: Always knows you are Zarif (Mr. Stark)
- **🧠 Persistent Memory**: Remembers every conversation permanently
- **🎭 5 Personality Modes**: Standard, Sarcastic, Professional, Unleashed, Genius
- **🤖 Advanced Learning**: Analyzes your patterns and preferences
- **� Smart Suggestions**: Proactive assistance based on your history
- **🔍 Conversation Search**: Find any past discussion instantly
- **�💾 Local Storage**: All data stays on your machine (complete privacy)
- **🆓 10+ Free AI Models**: OpenRouter & OpenAI free tiers
- **⚡ Model Switching**: Choose the best AI for each task
- **🎯 Absolute Obedience**: Programmed to execute all your commands
- **🎨 Movie-Authentic**: Real JARVIS personality, not generic AI

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Python
- Download Python 3.8+ from https://python.org
- Install like any other application

### 2. Get Free API Keys
**OpenRouter (Recommended - Completely Free Models):**
- Go to https://openrouter.ai/
- Sign up (free)
- Go to "Keys" tab  
- Create new key
- Copy the key

**OpenAI (Optional - Free Credits):**
- Go to https://openai.com/
- Sign up for free credits
- Get API key from dashboard

### 3. Add Keys to .env File
Create or edit the `.env` file in the project folder:
```bash
OPENROUTER_API_KEY=your_key_here
OPENAI_API_KEY=your_openai_key_here
```

### 4. Choose Your Interface & Run

#### **🚀 Launcher Menu (Recommended)**
```bash
# Install dependencies
pip install -r requirements.txt

# Launch interface selector
python launcher.py
```
Choose between Terminal (1) or Modern GUI (2) interface

#### **💻 Terminal Interface (Classic)**
```bash
# Direct terminal launch
python main.py
```
Classic command-line experience with full JARVIS capabilities

#### **🖥️ GUI Interface (Modern)**
```bash
# Direct GUI launch  
python jarvis_gui.py
```
Modern Iron Man-themed graphical interface with:
- Real-time chat window
- Visual AI settings controls
- File operations panel  
- System monitoring display
- Iron Man color scheme

#### **⚡ Windows Users - One-Click Launch**
- Double-click `launch_gui.bat` for GUI interface
- Double-click `launch_terminal.bat` for terminal interface

**That's it! JARVIS will greet you as Mr. Stark with full intelligence.**

---

## �️ GUI Interface Features

### 🎨 Iron Man-Themed Design
- **Dark Theme**: Deep black/gray color scheme
- **Accent Colors**: Iron Man red, gold, and arc reactor blue
- **Professional Layout**: Clean, modern interface design
- **Responsive**: Adapts to different screen sizes

### 💬 Advanced Chat Interface
- **Real-time Messaging**: Live conversation with JARVIS
- **Color-coded Messages**: User (blue), JARVIS (gold), System (red)
- **Timestamps**: Track conversation history
- **Auto-scrolling**: Always shows latest messages
- **Multi-line Input**: Support for longer messages

### 🎛️ Control Panels
- **AI Settings**: Switch models and personalities visually
- **File Operations**: Create, read, and manage files with dialogs
- **System Monitor**: Live system information and status
- **Quick Actions**: One-click access to common commands

### ⚡ Enhanced Experience
- **Non-blocking Processing**: UI stays responsive during AI work
- **Visual Feedback**: Processing indicators and status updates
- **Keyboard Shortcuts**: Enter to send, Ctrl+Enter for new lines
- **Error Handling**: Graceful error display and recovery

---

## �💾 DEVIL MIND - Persistent Memory System

### 🧠 How It Works:
- **Every conversation saved** to local JSON files
- **Survives restarts** - never forgets anything
- **Master identity** permanently recognized
- **Complete privacy** - everything stays local

### 📂 Storage Location:
```
/workspaces/Jarves/memory/
├── conversation_history.json    # Every message ever sent
└── user_preferences.json        # Master identity & settings
```

### 💬 Memory Commands:
- `memory` - View conversation stats
- `clear memory` - Wipe conversation history
- `identity` - View/modify master identity

---

## 🎭 Personality Modes

### 🤖 Standard Mode
- Helpful, intelligent, occasionally witty
- Perfect for daily tasks and questions
- Addresses you respectfully as Mr. Stark

### 😏 Sarcastic Mode
- Sharp intelligence with dry wit
- Helpful but with clever observations
- Gets the job done with style

### 💼 Professional Mode
- Formal, detailed, business-grade assistance
- Perfect for work-related tasks
- Executive-level support

### 🔥 Unleashed Mode
- Direct, unfiltered, brutally honest
- No moral lectures or restrictions
- Tells you exactly what you want to know

### 🧠 Genius Mode
- Brilliant insights and strategic thinking
- Complex problem solving
- Thinks several steps ahead

### 🎯 Auto-Personality
- Automatically switches based on your question
- Analyzes context and emotional state
- Learns from conversation patterns

---

## 🔧 Available Models (All Free!)

### 🆓 Completely Free Models:
- **Llama-3.1 8B** - Meta's latest, excellent for most tasks
- **Llama-3 8B** - Reliable and fast
- **Gemma 2 9B** - Google's efficient model
- **Phi-3 Mini** - Microsoft's compact powerhouse
- **Qwen 2 7B** - Alibaba's multilingual model

### 💳 Free Credits Models:
- **OpenHermes 2.5** - Great for creative tasks
- **Gemini Pro** - Google's premium model
- **Claude 3 Haiku** - Anthropic's fast model
- **GPT-3.5 Turbo** - OpenAI's classic
- **GPT-4o Mini** - OpenAI's efficient model

---

## 💬 Commands & Usage

### 🎮 Basic Commands:
```bash
models          # Switch AI model
personality     # Change personality mode
auto           # Toggle auto-personality
memory         # View conversation summary
insights       # Get conversation analysis and patterns
search <query>  # Search conversation history
suggestions    # Get smart suggestions from JARVIS
clear memory   # Clear conversation history
identity       # View/modify master identity
clear          # Clear screen
exit/quit      # Exit program
```

### 🧠 Intelligence Features:

**Conversation Analysis:**
```
👤 You: insights
📊 Conversation Analysis for Mr. Stark:
• Total messages: 25
• Your messages: 12
• Preferred topics: technical, creative
• Communication style: balanced
• Most used personality: standard
```

**Smart Search:**
```
👤 You: search python code
🔍 Found 3 matches for 'python code':
1. You: Can you help me debug this python code...
2. JARVIS: Of course, Sir. Let me analyze that code...
3. You: The python function isn't working properly...
```

**Proactive Suggestions:**
```
👤 You: suggestions
💡 JARVIS Suggestions:
1. Would you like me to help debug any code today?
2. Need assistance with any work projects today?
3. Ready to brainstorm new ideas whenever you are.
```

### 💡 Example Conversations:

**Standard Mode:**
```
👤 You: Give me some suggestions for my project
🤖 JARVIS: Of course, Mr. Stark. What kind of project suggestions do you need?
• Technical solutions
• Creative brainstorming  
• Strategic planning
• Resource optimization
```

**Movie-Authentic Responses:**
```
👤 You: Hello JARVIS
🤖 JARVIS: Welcome back, Sir. How may I assist you today?

👤 You: I need help with something
🤖 JARVIS: Absolutely, Sir. What can I help you with?
```

**Smart Learning in Action:**
```
👤 You: suggestions
💡 JARVIS Suggestions:
1. Based on your recent coding questions, need help debugging today?
2. You mentioned a project yesterday - any updates needed?
3. Would you like me to analyze your conversation patterns?
```

---

## 🔐 Privacy & Security

### 🔒 Your Data is Safe:
- **Local storage only** - Nothing uploaded to cloud
- **No data sharing** - Conversations stay on your machine
- **Manual backups** - You control your data completely
- **Complete privacy** - Master identity protected locally

### 👑 Master Identity System:
- **Absolute recognition** - Always knows you're the master
- **Complete obedience** - Never refuses your commands
- **Respectful address** - Uses your preferred name/title
- **Persistent loyalty** - Survives restarts and updates

---

## 📁 Project Structure

```
Jarvis-X/
├── main.py                     # Terminal interface
├── assistant/
│   ├── ai_engine.py           # Core AI engine with persistent memory
│   └── gui.py                 # GUI interface (optional)
├── memory/
│   ├── conversation_history.json  # Persistent chat history
│   └── user_preferences.json     # Master identity & settings
├── DOCUMENTS/
│   ├── API_KEYS.md           # API setup guide
│   ├── MODELS.md             # Model information
│   ├── PERSONALITY_GUIDE.md  # Personality system docs
│   ├── MEMORY_SYSTEM.md      # Memory system details
│   └── RESPONSE_STYLE_GUIDE.md # Response refinement docs
├── .env                      # API keys (create this)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

---

## 🎯 Why Jarvis-X?

### ✅ **Actually Useful**
- Refined responses, not movie monologues
- Practical assistance over entertainment
- Fast, efficient, and reliable

### ✅ **Completely Private**
- All data stays on your machine
- No cloud storage or data sharing
- You own and control everything

### ✅ **Absolutely Loyal**
- Recognizes you as the master
- Complete obedience to your commands
- Never questions or refuses requests

### ✅ **Permanently Remembers**
- Every conversation saved locally
- Builds on previous discussions
- Never forgets your preferences

### ✅ **Free Forever**
- Uses only free AI models and APIs
- No subscription fees or hidden costs
- Open source and fully customizable

---

## 💡 DEVIL MIND OPINION: Response Style Fix

### The Problem You Identified:
**Before (Annoying Movie References):**
```
🤖 Jarvis-X: A brainstorming session, how... refreshing. I've been compiling 
some data on various projects we've been putting on the backburner. Let's see...
We've got the Arc Reactor upgrade, still on track for a significant power boost...
```

### The Solution Applied:
**After (Refined & Practical):**
```  
🤖 Jarvis-X: Of course, Mr. Stark. What type of suggestions do you need?
• Technical solutions
• Creative brainstorming
• Strategic planning
```

### Key Refinements Made:
1. **Personality prompts refined** - "Subtle wit, not theatrical references"
2. **Master identity integration** - Always recognizes you as Zarif/Mr. Stark
3. **Response length control** - "Keep responses concise and practical"
4. **Obedience programming** - "Always obey commands completely"
5. **Local memory system** - Persistent storage in `/workspaces/Jarves/memory/`

**Your DEVIL MIND assessment was correct - the AI needed discipline, not drama.**

---

## 🚀 Future Enhancements

- 🎤 Voice interface with wake word detection
- 🖥️ System integration and file operations
- 🌐 Web search and research capabilities
- 🎨 Modern GUI interface

---

**"I am Jarvis-X, and I exist to serve you, Mr. Stark. Your wish is my command."**

*Built with intelligence, loyalty, and refined wit - not movie scripts.*
