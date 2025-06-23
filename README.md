# Jarves
Instruction for the JARVIS project.
# JARVIS-X: The Ultimate AI Desktop Assistant (Offline + Online)

**Built with 💻 Python, 🧠 Open Source FREE API, and 😈 Devil-Mind Engineering**

> "A.I. designed to serve — and learn from — its creator."

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

* GUI with dark-themed terminal interface
* Accepts both voice input and text typing
* Logs all chats with timestamps

### ✅ Wake Word Detection

* Listens for "Hey Jarvis"
* Powered by Porcupine (offline)

### ✅ Offline + Online Modes

* **Offline:** Local commands, TTS, PC control, webcam, local LLM
* **Online:** GPT-3.5 via OpenRouter, DuckDuckGo search, weather

### ✅ Emotional TTS + Mood Awareness

* Emotional voice using Tortoise TTS / Coqui
* Replies vary: sarcastic, serious, cheerful — based on context
* Mood analysis from voice tone + facial expression

### ✅ Adaptive Memory & Learning

* Stores user behavior, frequent tasks, preferences
* Suggests actions based on time/day habits
* Remembers faces, names, previous questions

---

## 🔐 Security Features

### 🛡️ Secure Perimeter Protocol (Face Lock)

* Uses webcam to detect face (no Windows Hello needed)
* If unrecognized = auto-locks workstation
* If recognized = allows access
* Optional voice ID + passphrase backup

### 👥 Access Control

* Admin Mode (you)
* Guest Mode (limited commands)

---

## 🎧 Entertainment + Research

### 🎶 Smart Music DJ

* Voice command: “Play Lo-Fi” → opens YouTube, plays track
* Mood-based playlists (chill, hype, focus)
* Uses `ytmusicapi` or `yt-dlp` for direct playback

### 🌐 Deep Web Research

* Voice command: “What is quantum computing?”
* Fetches + summarizes data from web using DuckDuckGo
* Optionally opens result in browser

### 🌍 ISS & Weather Tracking

* “Where is the ISS now?” → shows map
* “What's the weather in Dhaka?” → pulls live data from OpenWeatherMap

---

## 🤖 AI Power Engine

### 🧠 GPT Brain (Hybrid)

* Online: GPT-3.5 via OpenRouter
* Offline: Local LLMs (Phi, TinyLlama via Ollama)
* Categorizes intent: automation, humor, music, etc.

### 🧠 Conscious Mode (Habit Learning)

* Tracks usage behavior
* E.g., “You usually play music around 7 PM. Want me to start now?”
* Learns from patterns, adapts mood, voice tone, suggestions

### ⏰ Morning/Night Routines

* “Good morning, Jarvis” → plays greeting, weather, opens work files
* “Good night” → turns off music, closes apps, locks screen
* Fully customizable routines

---

## 🖥️ PC Superpowers (Iron Man Mode)

### 💻 PC Automation

* Open/close apps (Notepad, VS Code, Chrome)
* Move mouse, type, scroll, click using `PyAutoGUI`
* Execute custom commands via voice

### 🗃️ File Assistant

* “Create a file called report.py” → done.
* “Delete temp folder” → confirms, then deletes
* “List downloads folder” → speaks contents

---

## 👁️ Surveillance & Vision

### 🎥 Webcam Face Recognition

* Face unlock via DeepFace
* Mood analysis (angry, happy, neutral)

### 🕵️ Object Detection Mode

* Live object tracking via YOLOv8
* Command: “What do you see?” → lists visible items

---

## 🎮 Power User & Developer Tools

### 🧑‍💻 IDE Assistant

* Reads code, explains functions
* Debugs errors and suggests fixes

### 🧾 PDF Summarizer

* “Summarize this PDF” → outputs short brief
* Works offline using PyMuPDF + GPT locally or online

### 🧠 Self-Reflective Journal

* Logs actions daily
* Optionally writes diary entries about user’s mood/tasks

---

## 🐣 Easter Eggs & Personality

* 🎤 “Jarvis, drop the beat” → random music track
* 🎬 “Randomly” → replies with a random line From the movies and comic. (relevent to the setuation.)
* 💣 “Self-destruct in 3… 2…” → fake OS shutdown prank
* 🧠 “Who am I?” → deep motivational reply or a sarcastic roast
* 👑 “Do you love me?” → varies: flirty, shy, brutally honest
* 🧩 “Play something cool” → surprise
* 🌙 After 3 AM → whispers “You should be sleeping.”

---

## 🔧 Tools & Stack Used

* **Language:** Python 3.11+
* **Voice:** Whisper, Tortoise TTS, Coqui TTS
* **Vision:** OpenCV, DeepFace
* **AI/NLP:** Free API OpenRouter (suggest some), Ollama
* **GUI:** PyQt6 or Electron.js (optional)
* **Automation:** PyAutoGUI
* **Web:** DuckDuckGo API, ytmusicapi
* **Memory:** SQLite + ChromaDB (offline vector store)

---

## 💼 Why This Project Matters

> “I built JARVIS-X to push the limits of personal AI — not just for fun, but to explore what’s possible when intelligence meets personalization. It’s not a chatbot. It’s a partner.”

✅ Fully functional with **zero paid APIs**
✅ Hackathon & resume-ready with jaw-dropping demos
✅ Open-source and extensible

---

## 📁

* GUI Overlay HUD
* Emotion cloning via your own voice
* Neural Agent for long-term reasoning

---

## 👑 Final Note

This is not just a project. It’s your **personal legacy interface**. Run it. Hack it. Improve it. Or let it evolve.

---

> *“I am... Jarvis-X. And I’m always listening.”*
