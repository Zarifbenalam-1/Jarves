#!/usr/bin/env python3
"""
JARVIS-X ULTIMATE DEMON AI ASSISTANT
The Complete Iron Man Experience - Fully Integrated System
GUI + Voice + AI + File Operations + LiveKit Ready + Multi-Modal

🔥 FEATURES:
- Modern Iron Man GUI with dark theme
- Robust voice recognition and TTS
- Multi-provider AI engine (DeepSeek R1, Claude, Gemini, etc.)
- Advanced file operations with natural language
- LiveKit integration ready for real-time features
- Error handling and fallback systems
- Multi-threaded for smooth performance
"""

import os
import sys
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import queue
import time
import json
from datetime import datetime
from pathlib import Path

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from assistant.ai_engine import JarvisAI
from assistant.file_operations import get_file_operations_manager

class UltimateDemonAssistant:
    """Ultimate Demon AI Assistant - The Complete Iron Man Experience"""
    
    def __init__(self):
        """Initialize the Ultimate Demon Assistant"""
        print("🔥" + "="*60 + "🔥")
        print("   🤖 JARVIS-X ULTIMATE DEMON AI ASSISTANT 🤖")
        print("        The Complete Iron Man Experience")
        print("🔥" + "="*60 + "🔥")
        
        # Core components
        self.ai_engine = JarvisAI()
        self.file_manager = get_file_operations_manager()
        self.voice_engine = None
        self.voice_thread = None
        self.voice_active = False
        
        # GUI state
        self.conversation_history = []
        self.current_model = "deepseek/deepseek-r1-distill-qwen-32b"
        self.message_queue = queue.Queue()
        self.processing = False
        
        # Initialize components
        self.setup_voice_engine()
        self.setup_main_window()
        self.setup_gui_components()
        self.start_message_processor()
        
        # Welcome sequence
        self.show_welcome_sequence()
        
        print("✅ ULTIMATE DEMON AI ASSISTANT READY!")
        print("🎯 All systems online - Ready to serve!")
    
    def setup_voice_engine(self):
        """Setup voice engine with error handling"""
        try:
            from jarvis_voice_robust import RobustVoiceEngine
            self.voice_engine = RobustVoiceEngine()
            
            # Override voice command processing to integrate with GUI
            original_process = self.voice_engine.process_command
            self.voice_engine.process_command = lambda cmd: self.handle_voice_command(cmd, original_process)
            
            print("✅ Voice engine integrated successfully")
        except Exception as e:
            print(f"⚠️  Voice engine error: {e}")
            print("📢 Voice features will be disabled")
            self.voice_engine = None
    
    def setup_main_window(self):
        """Setup the main application window with Iron Man styling"""
        self.root = tk.Tk()
        self.root.title("JARVIS-X ULTIMATE DEMON AI ASSISTANT")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 800)
        
        # Iron Man color scheme
        self.colors = {
            'bg_primary': '#0a0a0a',      # Deep black
            'bg_secondary': '#1a1a1a',    # Dark gray
            'bg_accent': '#2a2a2a',       # Medium gray
            'text_primary': '#ffffff',     # White
            'text_secondary': '#b0b0b0',   # Light gray
            'accent_red': '#ff6b6b',       # Iron Man red
            'accent_gold': '#ffd93d',      # Iron Man gold
            'accent_blue': '#4ecdc4',      # Arc reactor blue
            'success': '#51cf66',          # Success green
            'warning': '#ffa726',          # Warning orange
            'error': '#f44336'             # Error red
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Try to set icon
        try:
            self.root.iconbitmap("jarvis_icon.ico")
        except:
            pass
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui_components(self):
        """Setup all GUI components"""
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title bar with Iron Man styling
        self.create_title_bar(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create main panels
        self.create_main_panels(content_frame)
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_title_bar(self, parent):
        """Create Iron Man styled title bar"""
        title_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=100)
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Main title
        title_label = tk.Label(
            title_frame,
            text="🔥 JARVIS-X ULTIMATE DEMON AI ASSISTANT 🔥",
            font=("Consolas", 20, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(pady=10)
        
        # Subtitle with current model
        subtitle = f"🤖 Iron Man Experience • Model: {self.current_model} • All Systems Online 🤖"
        subtitle_label = tk.Label(
            title_frame,
            text=subtitle,
            font=("Consolas", 10),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_secondary']
        )
        subtitle_label.pack()
        
        # Store subtitle for updates
        self.subtitle_label = subtitle_label
    
    def create_main_panels(self, parent):
        """Create main content panels"""
        
        # Left panel - Chat interface (70% width)
        left_panel = tk.Frame(parent, bg=self.colors['bg_secondary'])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Right panel - Controls (30% width)
        right_panel = tk.Frame(parent, bg=self.colors['bg_secondary'], width=400)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Setup panel components
        self.setup_chat_interface(left_panel)
        self.setup_control_panels(right_panel)
    
    def setup_chat_interface(self, parent):
        """Setup the main chat interface"""
        
        # Chat header
        chat_header = tk.Frame(parent, bg=self.colors['bg_accent'], height=40)
        chat_header.pack(fill="x", padx=10, pady=(10, 5))
        chat_header.pack_propagate(False)
        
        chat_title = tk.Label(
            chat_header,
            text="💬 CONVERSATION WITH JARVIS",
            font=("Consolas", 12, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_accent']
        )
        chat_title.pack(pady=10)
        
        # Chat display with scrollbar
        chat_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_gold'],
            selectbackground=self.colors['accent_blue'],
            selectforeground=self.colors['bg_primary']
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input area
        self.setup_input_area(parent)
    
    def setup_input_area(self, parent):
        """Setup message input area"""
        
        input_frame = tk.Frame(parent, bg=self.colors['bg_accent'], height=120)
        input_frame.pack(fill="x", padx=10, pady=(5, 10))
        input_frame.pack_propagate(False)
        
        # Input field
        input_container = tk.Frame(input_frame, bg=self.colors['bg_accent'])
        input_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text input
        self.input_text = tk.Text(
            input_container,
            height=3,
            font=("Consolas", 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_gold'],
            wrap=tk.WORD
        )
        self.input_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(input_container, bg=self.colors['bg_accent'])
        buttons_frame.pack(fill="x")
        
        # Send button
        self.send_button = tk.Button(
            buttons_frame,
            text="🚀 SEND MESSAGE",
            command=self.send_message,
            font=("Consolas", 10, "bold"),
            bg=self.colors['success'],
            fg=self.colors['bg_primary'],
            activebackground=self.colors['accent_gold'],
            relief="flat",
            padx=20
        )
        self.send_button.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_button = tk.Button(
            buttons_frame,
            text="🗑️ CLEAR CHAT",
            command=self.clear_chat,
            font=("Consolas", 10),
            bg=self.colors['error'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_red'],
            relief="flat",
            padx=15
        )
        clear_button.pack(side="left", padx=(0, 10))
        
        # Voice toggle button
        self.voice_button = tk.Button(
            buttons_frame,
            text="🎤 START VOICE" if not self.voice_active else "🔇 STOP VOICE",
            command=self.toggle_voice,
            font=("Consolas", 10, "bold"),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_gold'],
            relief="flat",
            padx=15
        )
        self.voice_button.pack(side="right")
        
        # Bind events
        self.input_text.bind("<Control-Return>", lambda e: self.send_message())
        self.input_text.bind("<KeyPress>", self.on_typing)
    
    def setup_control_panels(self, parent):
        """Setup right-side control panels"""
        
        # Voice controls
        self.create_voice_panel(parent)
        
        # AI model controls
        self.create_ai_panel(parent)
        
        # File operations
        self.create_file_panel(parent)
        
        # System info
        self.create_system_panel(parent)
    
    def create_voice_panel(self, parent):
        """Create voice control panel"""
        
        voice_frame = tk.LabelFrame(
            parent,
            text="🎤 VOICE CONTROLS",
            font=("Consolas", 11, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_secondary'],
            labelanchor="n"
        )
        voice_frame.pack(fill="x", padx=10, pady=10)
        
        # Voice status
        self.voice_status = tk.Label(
            voice_frame,
            text="Status: Inactive",
            font=("Consolas", 10),
            fg=self.colors['warning'],
            bg=self.colors['bg_secondary']
        )
        self.voice_status.pack(pady=5)
        
        # Wake words info
        wake_words_text = "🎯 Wake Words: JARVIS, Hey JARVIS\\n🎤 Commands: Create file, Read file,\\n   What's the weather, Write code..."
        
        wake_info = tk.Label(
            voice_frame,
            text=wake_words_text,
            font=("Consolas", 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            justify="left"
        )
        wake_info.pack(pady=5, padx=10)
        
        # Voice quality indicator
        self.voice_quality = tk.Label(
            voice_frame,
            text="🔊 Voice Engine: " + ("Ready" if self.voice_engine else "Disabled"),
            font=("Consolas", 9),
            fg=self.colors['success'] if self.voice_engine else self.colors['error'],
            bg=self.colors['bg_secondary']
        )
        self.voice_quality.pack(pady=5)
    
    def create_ai_panel(self, parent):
        """Create AI model control panel"""
        
        ai_frame = tk.LabelFrame(
            parent,
            text="🧠 AI ENGINE",
            font=("Consolas", 11, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_secondary'],
            labelanchor="n"
        )
        ai_frame.pack(fill="x", padx=10, pady=10)
        
        # Model selector
        model_label = tk.Label(
            ai_frame,
            text="Current Model:",
            font=("Consolas", 9),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        model_label.pack(pady=(10, 5))
        
        # Model dropdown
        self.model_var = tk.StringVar(value=self.current_model)
        model_options = [
            "deepseek/deepseek-r1-distill-qwen-32b",
            "anthropic/claude-3-haiku",
            "google/gemini-pro",
            "meta-llama/llama-3.1-8b-instruct",
            "microsoft/wizardlm-2-8x22b",
            "qwen/qwen-2.5-72b-instruct"
        ]
        
        self.model_dropdown = ttk.Combobox(
            ai_frame,
            textvariable=self.model_var,
            values=model_options,
            state="readonly",
            font=("Consolas", 9)
        )
        self.model_dropdown.pack(fill="x", padx=10, pady=5)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.change_model)
        
        # AI status
        self.ai_status = tk.Label(
            ai_frame,
            text="🟢 AI Ready",
            font=("Consolas", 10, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_secondary']
        )
        self.ai_status.pack(pady=10)
        
        # Quick actions
        quick_frame = tk.Frame(ai_frame, bg=self.colors['bg_secondary'])
        quick_frame.pack(fill="x", padx=10, pady=5)
        
        personality_btn = tk.Button(
            quick_frame,
            text="🎭 Personality",
            command=self.change_personality,
            font=("Consolas", 8),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            relief="flat"
        )
        personality_btn.pack(side="left", padx=(0, 5))
        
        memory_btn = tk.Button(
            quick_frame,
            text="🧠 Memory",
            command=self.show_memory,
            font=("Consolas", 8),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            relief="flat"
        )
        memory_btn.pack(side="right")
    
    def create_file_panel(self, parent):
        """Create file operations panel"""
        
        file_frame = tk.LabelFrame(
            parent,
            text="📁 FILE OPERATIONS",
            font=("Consolas", 11, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_secondary'],
            labelanchor="n"
        )
        file_frame.pack(fill="x", padx=10, pady=10)
        
        # File operation buttons
        buttons = [
            ("📄 Create File", self.create_file_dialog, self.colors['accent_blue']),
            ("📖 Read File", self.read_file_dialog, self.colors['accent_blue']),
            ("📋 List Files", self.list_files_dialog, self.colors['accent_blue']),
            ("🗂️ Organize", self.organize_files_dialog, self.colors['warning'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                file_frame,
                text=text,
                command=command,
                font=("Consolas", 9),
                bg=color,
                fg=self.colors['text_primary'],
                activebackground=self.colors['accent_gold'],
                relief="flat",
                width=15
            )
            btn.pack(fill="x", padx=10, pady=3)
    
    def create_system_panel(self, parent):
        """Create system information panel"""
        
        system_frame = tk.LabelFrame(
            parent,
            text="⚡ SYSTEM STATUS",
            font=("Consolas", 11, "bold"),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_secondary'],
            labelanchor="n"
        )
        system_frame.pack(fill="x", padx=10, pady=10)
        
        # System stats
        stats_text = f"""🔥 DEMON Mode: ACTIVE
🤖 AI Provider: OpenRouter
🎤 Voice: {"Enabled" if self.voice_engine else "Disabled"}
💾 Memory: {len(self.conversation_history)} messages
⚡ Status: All Systems Online"""
        
        self.system_stats = tk.Label(
            system_frame,
            text=stats_text,
            font=("Consolas", 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            justify="left"
        )
        self.system_stats.pack(pady=10, padx=10)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        
        status_frame = tk.Frame(parent, bg=self.colors['bg_accent'], height=30)
        status_frame.pack(fill="x", pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="🔥 JARVIS-X DEMON AI Ready • Type a message or use voice commands",
            font=("Consolas", 9),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_accent']
        )
        self.status_label.pack(pady=6)
    
    def start_message_processor(self):
        """Start the message processing thread"""
        self.message_thread = threading.Thread(target=self.process_message_queue, daemon=True)
        self.message_thread.start()
    
    def process_message_queue(self):
        """Process messages from the queue"""
        while True:
            try:
                if not self.message_queue.empty():
                    message_data = self.message_queue.get()
                    self.root.after(0, lambda data=message_data: self.display_message(**data))
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Message queue error: {e}")
    
    def show_welcome_sequence(self):
        """Show Iron Man style welcome sequence"""
        welcome_messages = [
            ("SYSTEM", "🔥 JARVIS-X DEMON AI ASSISTANT INITIALIZING...", "system"),
            ("SYSTEM", "⚡ All systems online - GUI, Voice, AI, File Operations", "system"),
            ("SYSTEM", f"🧠 AI Model: {self.current_model}", "system"),
            ("SYSTEM", f"🎤 Voice Engine: {'Active' if self.voice_engine else 'Disabled'}", "system"),
            ("JARVIS", "Good day, Sir. JARVIS-X Demon AI Assistant at your service.", "ai"),
            ("JARVIS", "I'm ready to assist with any task - just speak or type your command.", "ai")
        ]
        
        for sender, message, msg_type in welcome_messages:
            self.add_message(sender, message, msg_type)
    
    def add_message(self, sender, message, msg_type="user", display_immediately=True):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color and icon mapping
        styles = {
            "user": {"color": self.colors['accent_blue'], "icon": "👤"},
            "ai": {"color": self.colors['success'], "icon": "🤖"},
            "system": {"color": self.colors['warning'], "icon": "⚡"},
            "voice": {"color": self.colors['accent_gold'], "icon": "🎤"},
            "file": {"color": self.colors['accent_red'], "icon": "📁"},
            "error": {"color": self.colors['error'], "icon": "❌"}
        }
        
        style = styles.get(msg_type, styles["user"])
        
        # Format message
        formatted_message = f"[{timestamp}] {style['icon']} {sender}: {message}\\n"
        
        if display_immediately:
            # Add to display immediately
            self.chat_display.insert(tk.END, formatted_message)
            self.chat_display.see(tk.END)
        else:
            # Queue for later display
            self.message_queue.put({
                "sender": sender,
                "message": message,
                "msg_type": msg_type,
                "timestamp": timestamp
            })
        
        # Store in history
        self.conversation_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "type": msg_type
        })
        
        # Update system stats
        self.update_system_stats()
    
    def display_message(self, sender, message, msg_type, timestamp):
        """Display a queued message"""
        styles = {
            "user": {"color": self.colors['accent_blue'], "icon": "👤"},
            "ai": {"color": self.colors['success'], "icon": "🤖"},
            "system": {"color": self.colors['warning'], "icon": "⚡"},
            "voice": {"color": self.colors['accent_gold'], "icon": "🎤"},
            "file": {"color": self.colors['accent_red'], "icon": "📁"},
            "error": {"color": self.colors['error'], "icon": "❌"}
        }
        
        style = styles.get(msg_type, styles["user"])
        formatted_message = f"[{timestamp}] {style['icon']} {sender}: {message}\\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Send a message to the AI"""
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add user message
        self.add_message("You", message, "user")
        
        # Update status
        self.update_status("🤖 JARVIS is thinking...")
        self.ai_status.configure(text="🟡 Processing...", fg=self.colors['warning'])
        
        # Process with AI in background
        threading.Thread(target=self.process_ai_message, args=(message,), daemon=True).start()
    
    def process_ai_message(self, message):
        """Process message with AI engine"""
        try:
            # Get AI response
            response = self.ai_engine.chat(message)
            
            # Queue response for display
            self.message_queue.put({
                "sender": "JARVIS",
                "message": response,
                "msg_type": "ai",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Update status
            self.root.after(0, lambda: self.update_status("🔥 JARVIS-X Ready"))
            self.root.after(0, lambda: self.ai_status.configure(text="🟢 AI Ready", fg=self.colors['success']))
            
        except Exception as e:
            error_msg = f"AI processing error: {str(e)}"
            self.message_queue.put({
                "sender": "ERROR",
                "message": error_msg,
                "msg_type": "error",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            self.root.after(0, lambda: self.update_status("❌ AI Error"))
            self.root.after(0, lambda: self.ai_status.configure(text="🔴 AI Error", fg=self.colors['error']))
    
    def handle_voice_command(self, command, original_process):
        """Handle voice commands and integrate with GUI"""
        try:
            # Add voice command to chat
            self.message_queue.put({
                "sender": "Voice",
                "message": command,
                "msg_type": "voice",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Process command
            response = original_process(command)
            
            # Add response to chat
            self.message_queue.put({
                "sender": "JARVIS",
                "message": response,
                "msg_type": "ai",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Voice command error: {str(e)}"
            self.message_queue.put({
                "sender": "ERROR",
                "message": error_msg,
                "msg_type": "error",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            return "Voice command processing error."
    
    def toggle_voice(self):
        """Toggle voice recognition"""
        if not self.voice_engine:
            messagebox.showerror("Voice Error", "Voice engine not available")
            return
        
        if not self.voice_active:
            # Start voice
            self.voice_active = True
            self.voice_button.configure(text="🔇 STOP VOICE", bg=self.colors['error'])
            self.voice_status.configure(text="Status: Active", fg=self.colors['success'])
            
            # Start voice thread
            self.voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
            self.voice_thread.start()
            
            self.add_message("SYSTEM", "🎤 Voice recognition activated - Say 'JARVIS' to begin", "system")
            self.update_status("🎤 Voice Active - Listening for wake word...")
        else:
            # Stop voice
            self.voice_active = False
            if self.voice_engine:
                self.voice_engine.voice_active = False
            
            self.voice_button.configure(text="🎤 START VOICE", bg=self.colors['accent_blue'])
            self.voice_status.configure(text="Status: Inactive", fg=self.colors['warning'])
            
            self.add_message("SYSTEM", "🔇 Voice recognition deactivated", "system")
            self.update_status("🔥 JARVIS-X Ready")
    
    def voice_loop(self):
        """Voice recognition loop"""
        try:
            self.voice_engine.voice_active = True
            
            while self.voice_active and self.voice_engine.voice_active:
                try:
                    if not self.voice_engine.conversation_active:
                        # Listen for wake word
                        text = self.voice_engine.listen_for_speech(timeout=2, phrase_timeout=4)
                        
                        if text and self.voice_engine.is_wake_word(text):
                            self.voice_engine.conversation_active = True
                            self.voice_engine.speak("Yes, Sir? How may I assist you?")
                            
                            self.root.after(0, lambda: self.update_status("🎤 Voice Active - Listening..."))
                            continue
                    
                    else:
                        # In conversation mode
                        text = self.voice_engine.listen_for_speech(timeout=8, phrase_timeout=12)
                        
                        if text:
                            # Process command (will update GUI through handler)
                            response = self.voice_engine.process_command(text)
                            self.voice_engine.speak(response)
                        else:
                            # End conversation
                            self.voice_engine.speak("I'm here when you need me, Sir.")
                            self.voice_engine.conversation_active = False
                            self.root.after(0, lambda: self.update_status("🎤 Voice Active - Listening for wake word..."))
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"❌ Voice loop iteration error: {e}")
                    time.sleep(1)
                    
        except Exception as e:
            print(f"❌ Voice loop error: {e}")
            self.root.after(0, lambda: self.add_message("ERROR", f"Voice system error: {e}", "error"))
            self.root.after(0, lambda: self.toggle_voice())  # Stop voice on error
    
    def change_model(self, event=None):
        """Change AI model"""
        new_model = self.model_var.get()
        try:
            self.ai_engine.set_model(new_model)
            self.current_model = new_model
            
            # Update subtitle
            subtitle = f"🤖 Iron Man Experience • Model: {new_model} • All Systems Online 🤖"
            self.subtitle_label.configure(text=subtitle)
            
            self.add_message("SYSTEM", f"🧠 Switched to model: {new_model}", "system")
            self.update_status(f"🧠 AI Model changed to {new_model.split('/')[-1]}")
            
        except Exception as e:
            self.add_message("ERROR", f"Model switch failed: {e}", "error")
    
    def change_personality(self):
        """Change AI personality"""
        personalities = ["professional", "friendly", "creative", "analytical", "humorous"]
        current = self.ai_engine.get_current_personality()
        
        # Simple dialog for personality change
        choice = simpledialog.askstring(
            "Change Personality",
            f"Current: {current}\\nChoose: {', '.join(personalities)}"
        )
        
        if choice and choice.lower() in personalities:
            self.ai_engine.set_personality(choice.lower())
            self.add_message("SYSTEM", f"🎭 Personality changed to: {choice}", "system")
    
    def show_memory(self):
        """Show conversation memory"""
        memory_info = self.ai_engine.get_conversation_summary()
        self.add_message("MEMORY", f"Conversation summary: {memory_info}", "system")
    
    def create_file_dialog(self):
        """Create file dialog"""
        filename = simpledialog.askstring("Create File", "Enter filename (with extension):")
        if filename:
            content = simpledialog.askstring("File Content", "Enter file content (or leave empty):")
            try:
                result = self.file_manager.create_file(filename, content or "")
                self.add_message("FILE", f"✅ Created file: {filename}", "file")
            except Exception as e:
                self.add_message("ERROR", f"❌ File creation failed: {e}", "error")
    
    def read_file_dialog(self):
        """Read file dialog"""
        filename = filedialog.askopenfilename(title="Select file to read")
        if filename:
            try:
                result = self.file_manager.read_file(filename)
                self.add_message("FILE", f"📖 Read file: {Path(filename).name}", "file")
                
                # Show content (truncated if too long)
                content = result[:1000] + "..." if len(result) > 1000 else result
                self.add_message("CONTENT", content, "file")
                
            except Exception as e:
                self.add_message("ERROR", f"❌ File read failed: {e}", "error")
    
    def list_files_dialog(self):
        """List files dialog"""
        directory = filedialog.askdirectory(title="Select directory to list")
        if directory:
            try:
                files = self.file_manager.list_files(directory)
                self.add_message("FILE", f"📋 Directory: {Path(directory).name}", "file")
                
                # Show files (limited to first 30)
                file_list = "\\n".join(files[:30])
                if len(files) > 30:
                    file_list += f"\\n... and {len(files) - 30} more files"
                
                self.add_message("FILES", file_list, "file")
                
            except Exception as e:
                self.add_message("ERROR", f"❌ File listing failed: {e}", "error")
    
    def organize_files_dialog(self):
        """Organize files dialog"""
        directory = filedialog.askdirectory(title="Select directory to organize")
        if directory:
            try:
                # This would call a file organization function
                self.add_message("FILE", f"🗂️ Organizing files in: {Path(directory).name}", "file")
                self.add_message("SYSTEM", "File organization feature coming soon!", "system")
                
            except Exception as e:
                self.add_message("ERROR", f"❌ File organization failed: {e}", "error")
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.delete("1.0", tk.END)
        self.conversation_history = []
        self.add_message("SYSTEM", "🗑️ Chat cleared", "system")
        self.update_system_stats()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.configure(text=message)
    
    def update_system_stats(self):
        """Update system statistics display"""
        stats_text = f"""🔥 DEMON Mode: ACTIVE
🤖 AI Provider: OpenRouter
🎤 Voice: {"Enabled" if self.voice_engine else "Disabled"}
💾 Memory: {len(self.conversation_history)} messages
⚡ Status: All Systems Online"""
        
        self.system_stats.configure(text=stats_text)
    
    def on_typing(self, event):
        """Handle typing events"""
        # Update status when user starts typing
        if not self.processing:
            self.update_status("✍️ Typing...")
    
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Shutdown JARVIS-X Demon AI Assistant?"):
            print("👋 Shutting down JARVIS-X Demon AI Assistant...")
            
            # Stop voice if active
            if self.voice_active:
                self.voice_active = False
                if self.voice_engine:
                    self.voice_engine.voice_active = False
            
            # Save conversation history
            try:
                history_file = "conversation_history.json"
                with open(history_file, 'w') as f:
                    json.dump(self.conversation_history, f, indent=2)
                print(f"📝 Conversation saved to {history_file}")
            except Exception as e:
                print(f"⚠️  Could not save conversation: {e}")
            
            self.root.destroy()
            print("✅ JARVIS-X Demon AI Assistant shutdown complete")
    
    def run(self):
        """Run the application"""
        try:
            print("🚀 Starting JARVIS-X Demon AI Assistant GUI...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n👋 Keyboard interrupt - shutting down...")
        except Exception as e:
            print(f"❌ Runtime error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.voice_active:
                self.voice_active = False
            print("✅ JARVIS-X Demon AI Assistant terminated")

def main():
    """Main function"""
    print("🔥 INITIALIZING JARVIS-X ULTIMATE DEMON AI ASSISTANT...")
    print("=" * 70)
    print("🤖 The Complete Iron Man Experience")
    print("🎯 GUI + Voice + AI + File Operations + LiveKit Ready")
    print("=" * 70)
    
    try:
        app = UltimateDemonAssistant()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
