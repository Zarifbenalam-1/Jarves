# Jarves

---

## 🧑‍💻 Setup for Humans (No Tech Skills Needed!)

Welcome! This guide will help you set up Jarvis-X, even if you’ve never coded before. Just follow these steps:

### 1. Install Python
- Download Python from https://python.org (version 3.11 or newer).
- Install it like any other app.

### 2. Get Your Free API Keys
Jarvis-X uses free online tools to be smart. You’ll need to get a few keys (like passwords) from these services. Don’t worry, it’s easy!

- **OPENAI_API_KEY**: For smart chat and answers. Get it free from https://openrouter.ai/
- **DUCKDUCKGO_API_KEY**: For web search. Get it free from https://duckduckgo.com/developers
- **YTMUSIC_API_KEY**: For music features. Get it free from https://ytmusicapi.readthedocs.io/en/latest/

If you need help, just ask me!

### 3. Add Keys to the .env File
- Open the `.env` file in this project.
- Paste your keys like this:
  OPENAI_API_KEY=your_openai_key_here
  DUCKDUCKGO_API_KEY=your_duckduckgo_key_here
  YTMUSIC_API_KEY=your_ytmusic_key_here

### 4. Install Requirements
Open a terminal in this folder and run:
  pip install -r requirements.txt

### 5. Run Jarvis-X
In the terminal, run:
  python main.py

That’s it! If you get stuck, check the FAQ at the bottom of this file or ask for help.

---

## 🔥 Project Overview

**JARVIS-X** is a next-gen personal assistant inspired by Tony Stark’s JARVIS, built for real-world use using only **free tools, APIs, and offline capabilities**. It combines a voice+text interface, smart emotional responses, webcam-based security, PC automation, and adaptive learning to deliver an Iron-Man-level AI experience.

This project is built for:

* 🏁 Hackathons
* 📄 Harvard/Tech resume highlight
* 🧪 Research & dev demos
* 🔐 Local desktop usage (no data leaks)

---

## 🚀 Core Features (Free, Real, and Powerful)

### ✅ Voice + Text Chat Interface

JARVIS-X includes a dual-mode communication interface — a modern, dark-themed GUI where users can either speak commands or type them directly. This chat interface logs all user interactions with timestamps, allowing a clear command history. The assistant will process these inputs through an NLP engine and give verbal and visual feedback.

### ✅ Wake Word Detection

To simulate a hands-free experience, JARVIS-X continuously listens for the phrase "Hey Jarvis" using Porcupine, a privacy-focused and offline wake-word engine. Once triggered, it activates the assistant and awaits your command.

### ✅ Offline + Online Modes

JARVIS-X works in hybrid mode:

* **Offline mode:** Handles basic automation, voice interaction, face recognition, file control, and local responses using lightweight models.
* **Online mode:** Enables richer conversational capabilities, web search, and dynamic data fetching using OpenRouter’s GPT-3.5 and DuckDuckGo API.

This ensures it remains functional even without internet access, while still capable of advanced thinking when online.

### ✅ Emotional TTS + Mood Awareness

The assistant’s voice engine (using Tortoise or Coqui TTS) delivers expressive and emotional speech. It adjusts tone and emotion (sarcastic, cheerful, serious) based on the mood detected from your voice, text, and even facial expressions. The assistant can sound snarky when joking, calming when giving reminders, or intense during alerts.

### ✅ Adaptive Memory & Learning

JARVIS-X constantly monitors your command patterns, preferences, and usage time. Using local databases and vector stores, it begins to understand your habits (like playing music at night or checking weather in the morning). Over time, it starts suggesting actions, improving personalization, and simulating familiarity — like a real digital companion.

---

## 🔐 Security Features

### 🛡️ Secure Perimeter Protocol (Face Lock)

This custom security system uses your webcam to detect and recognize faces using OpenCV and DeepFace. When the system detects an unrecognized face, it auto-locks your workstation. If your face is recognized, JARVIS-X grants access. It supports fallback options like passphrases or voice ID. This does not require Windows Hello or biometric hardware.

### 👥 Access Control

Users are categorized into access levels:

* **Admin Mode:** Full system access and commands.
* **Guest Mode:** Limited features — cannot delete files or access memory logs.

You can restrict command sets based on who’s present.

---

## 🎧 Entertainment + Research

### 🎶 Smart Music DJ

JARVIS-X integrates with YouTube via `ytmusicapi` or `yt-dlp` to search and play music. It tailors song choice to your mood or specific command. You can say:

* “Play something relaxing.”
* “Shuffle my battle playlist.”

It automatically fetches the right content and launches it with voice feedback.

### 🌐 Deep Web Research

You can ask JARVIS-X research questions like “What is quantum computing?” It uses DuckDuckGo to find the most relevant sources, scrapes and summarizes results, and can even open the pages for further reading. Perfect for fast fact-checking or inspiration.

### 🌍 ISS & Weather Tracking

Jarvis can track the International Space Station and deliver its live position on a map. For weather, it pulls data from OpenWeatherMap to give reports, forecasts, and personalized advice like "Take an umbrella today."

---

## 🤖 AI Power Engine

### 🧠 GPT Brain (Hybrid)

The engine uses OpenRouter's GPT-3.5 for online tasks and a local LLM (like Phi or TinyLlama via Ollama) for offline reasoning. It classifies your command: Is it a task? A question? A joke? A file instruction? Then routes it to the right logic handler. All responses are natural and context-aware.

### 🧠 Conscious Mode (Habit Learning)

Beyond basic memory, JARVIS-X keeps a timeline of your actions, forming behavioral patterns. It knows when you usually code, listen to music, or work on documents. This makes it proactive:

* “You usually review your notes now. Should I open them?”
* “Want me to play your evening playlist?”

### ⏰ Morning/Night Routines

These customizable routines let you trigger a sequence of actions with one phrase:

* **Morning:** Greet you, show weather, open productivity apps.
* **Night:** Say goodnight, pause music, close files, and lock screen.

---

## 🖥️ PC Superpowers (Iron Man Mode)

### 💻 PC Automation

Using PyAutoGUI and system libraries, JARVIS-X can:

* Open/close apps (e.g., Chrome, VS Code)
* Type messages, move the mouse, click buttons
* Execute commands like “Open YouTube and search lo-fi music”

This replicates the feel of a digital assistant who can use the PC like you do.

### 🗃️ File Assistant

Jarvis understands file operations:

* “Create a folder called ProjectX.”
* “Delete old\_logs directory.”
* “List contents of Downloads folder.”

It provides audio/visual confirmations and follows voice-triggered file control.

---

## 👁️ Surveillance & Vision

### 🎥 Webcam Face Recognition

Using DeepFace and OpenCV, Jarvis can analyze webcam feeds in real-time to detect:

* Your identity (unlock or restrict access)
* Your mood (happy, stressed, neutral)
* Number of people present

It becomes your desktop’s visual awareness system.

### 🕵️ Object Detection Mode

Using YOLOv8, Jarvis can recognize and name objects seen through your webcam:

* Laptops, bottles, phones, faces, hands

When you ask, “Jarvis, what do you see?”, it responds based on real-time analysis.

---

## 🎮 Power User & Developer Tools

### 🧑‍💻 IDE Assistant

JARVIS-X can assist with coding. It can:

* Read a Python file and explain it
* Spot syntax errors
* Suggest improvements
* Even generate basic functions using GPT

It helps you debug like a real assistant watching your IDE.

### 🧾 PDF Summarizer

Drop any PDF into a linked folder and say “Summarize this.” Jarvis scans it using PyMuPDF, then generates a human-style summary using GPT or local models. Perfect for studying, reports, or research.

### 🧠 Self-Reflective Journal

Jarvis logs its daily activities:

* What it did for you
* What questions you asked
* Your mood

It then writes a short diary-style log of your day — like a digital assistant learning to reflect.

---

## 🐣 Easter Eggs & Personality

JARVIS-X includes playful, surprising, and nerdy responses:

* “Jarvis, drop the beat” → Hidden music starts
* “Randomly ” → Replies with MCU quotes witch is relevent. and findes the quotes in the internet database.

* “Who am I?” → Personalized motivational or sarcastic replies
* “Play something cool” → May music on youtube.
* After 3 AM → Says, “You should be sleeping.”

These add human-like behavior and humor, making your assistant feel alive.

---

## 🔧 Tools & Stack Used

* **Language:** Python 3.11+
* **Voice:** Whisper, Tortoise TTS, Coqui TTS
* **Vision:** OpenCV, DeepFace
* **AI/NLP:** GPT-3.5 via OpenRouter, Ollama (local LLMs)
* **GUI:** PyQt6 or Electron.js
* **Automation:** PyAutoGUI
* **Web:** DuckDuckGo API, ytmusicapi, OpenWeatherMap API
* **Memory:** SQLite + ChromaDB (offline vector store)

---

## 💼 Why This Project Matters

> “I built JARVIS-X to push the limits of personal AI — not just for fun, but to explore what’s possible when intelligence meets personalization. It’s not a chatbot. It’s a partner.”

✅ Fully functional with **zero paid APIs**
✅ Hackathon & resume-ready with jaw-dropping demos
✅ Open-source and extensible

---

## 📁 Coming Soon

### 🖥️ GUI Overlay HUD

A floating visual overlay that stays on top of your desktop, showing live data like CPU usage, battery, running tasks, and assistant status. Transparent and interactive, just like Iron Man's helmet interface. And option to close it.

### 🗣️ Emotion Cloning via Your Own Voice

Train your own voice into the system using free tools (Tortoise or Coqui). Jarvis then replies in your voice — with different moods (calm, funny, dramatic). Makes the assistant feel more like you or more like your mirror.

### 🧠 Neural Agent for Long-Term Reasoning

Jarvis will track long-term interactions, memory, and user habits. It will connect facts over time, ask smarter questions, and recall history across weeks — forming an evolving intelligence model.

---

## 👑 Final Note

This is not just a project. It’s your **personal legacy interface**. Run it. Hack it. Improve it. Or let it evolve.

> *“I am... Jarvis-X. And I’m always listening.”*
