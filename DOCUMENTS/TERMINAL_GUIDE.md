# How to Use Jarvis-X Terminal Interface

This guide explains how to use the terminal-based version of Jarvis-X, including AI model selection and chat features.

## 🚀 Starting Jarvis-X

1. Open a terminal in the main Jarvis-X directory
2. Run the command:
   ```bash
   python3 main.py
   ```
3. Jarvis-X will start with a welcome screen showing the current AI model

## 💬 Basic Chat Commands

Once Jarvis-X is running, you can:

- **Chat normally**: Just type your message and press Enter
- **Switch AI models**: Type `models` to see and select different AI brains
- **Change personality**: Type `personality` to switch AI behavior modes
- **Toggle auto-personality**: Type `auto` to enable/disable automatic mode switching
- **Check memory**: Type `memory` to see conversation history
- **Clear memory**: Type `clear memory` to start a fresh conversation
- **Clear screen**: Type `clear` to clean up the interface
- **Exit program**: Type `exit` or `quit`, or press Ctrl+C

## 🧠 AI Model Selection

### How to Switch Models:
1. Type `models` in the chat
2. You'll see a list like this:
   ```
   🧠 Available AI Models:
     1. GPT-3.5 Turbo (OpenRouter) ✅
     2. Mixtral 8x7B (OpenRouter)
     3. Llama-3 (OpenRouter)
     4. Gemini (OpenRouter)
   ```
3. Type the number (1-4) of the model you want
4. Jarvis-X will switch immediately - no restart needed!

### Model Differences:
- **GPT-3.5 Turbo**: Best for general chat, creative writing
- **Mixtral 8x7B**: Great for reasoning, technical questions
- **Llama-3**: Good balance of creativity and logic
- **Gemini**: Strong at analysis and research tasks

## 🎯 Tips for Best Results

### Chat Tips:
- Be specific with your questions
- Ask follow-up questions for clarification
- Use "explain like I'm 5" for simple explanations

### Model Selection Tips:
- Try different models for different tasks
- GPT-3.5 is fastest for quick questions
- Mixtral is better for complex problem-solving
- Switch models anytime during conversation

## 🔧 Troubleshooting

### If Jarvis-X won't start:
- Check that your API keys are in the `.env` file
- Run `pip install -r requirements.txt` to install dependencies

### If AI responses are slow:
- Try switching to GPT-3.5 Turbo (fastest model)
- Check your internet connection
 [Auto-switched to Unleashed mode]
🤖 Jarvis-X: Error: Failed to connect to AI service - 403 Client Error: Forbidden for url: https://openrouter.ai/api/v1/chat/completions [Auto-switched to Unleashed mode]
🤖 Jarvis-X: Error: Failed to connect to AI service - 403 Client Error: Forbidden for url: https://openrouter.ai/api/v1/chat/completions
- Check the DOCUMENTS/API_KEYS.md file for help getting keys

---

**Pro Tip**: The current model is always shown at the top of the screen, so you know which AI brain you're talking to!
