#!/usr/bin/env python3
"""
JARVIS-X DEMON AI ASSISTANT
Ultimate Integrated System - GUI + Voice + AI + File Operations
The Complete Iron Man Experience
"""

import os
import sys
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import customtkinter as ctk
from datetime import datetime
import json
import time

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all our modules
from assistant.ai_engine import JarvisAI
from assistant.file_operations import get_file_operations_manager
from jarvis_voice_robust import RobustVoiceEngine

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DemonAIAssistant:
    """Ultimate AI Assistant - GUI + Voice + AI + File Operations"""
    
    def __init__(self):
        """Initialize the Demon AI Assistant"""
        print("🔥 Initializing JARVIS-X DEMON AI ASSISTANT...")
        
        # Core components
        self.ai_engine = JarvisAI()
        self.file_manager = get_file_operations_manager()
        self.voice_engine = None
        self.voice_thread = None
        self.voice_active = False
        
        # GUI state
        self.conversation_history = []
        self.current_model = "deepseek/deepseek-r1-distill-qwen-32b"
        
        # Initialize GUI
        self.setup_main_window()
        self.setup_gui_components()
        self.setup_voice_integration()
        
        # Welcome message
        self.add_message("JARVIS", "🔥 DEMON AI ASSISTANT ONLINE 🔥", "system")
        self.add_message("JARVIS", "GUI, Voice, AI, and File Operations integrated!", "system")
        self.add_message("JARVIS", "Ready to assist you, Sir.", "ai")
        
        print("✅ DEMON AI ASSISTANT READY!")
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root = ctk.CTk()
        self.root.title("JARVIS-X DEMON AI ASSISTANT")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#0a0a0a")
        
        # Icon and styling
        try:
            self.root.iconbitmap("jarvis_icon.ico")
        except:
            pass
    
    def setup_gui_components(self):
        """Setup all GUI components"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = ctk.CTkFrame(main_frame, height=80, fg_color="#1a1a1a")
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Title and status
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🔥 JARVIS-X DEMON AI ASSISTANT 🔥",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00ff41"
        )
        title_label.pack(pady=20)
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Chat and controls
        left_panel = ctk.CTkFrame(content_frame, width=900, fg_color="#1a1a1a")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Right panel - Voice and file operations
        right_panel = ctk.CTkFrame(content_frame, width=400, fg_color="#1a1a1a")
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        
        # Setup left panel components
        self.setup_chat_area(left_panel)
        self.setup_input_area(left_panel)
        
        # Setup right panel components
        self.setup_voice_controls(right_panel)
        self.setup_file_operations(right_panel)
        self.setup_ai_controls(right_panel)
    
    def setup_chat_area(self, parent):
        """Setup the chat conversation area"""
        # Chat header
        chat_header = ctk.CTkFrame(parent, height=40, fg_color="#2a2a2a")
        chat_header.pack(fill="x", padx=10, pady=(10, 5))
        chat_header.pack_propagate(False)
        
        chat_title = ctk.CTkLabel(
            chat_header, 
            text="💬 CONVERSATION",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff41"
        )
        chat_title.pack(pady=8)
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            parent,
            font=ctk.CTkFont(size=12),
            fg_color="#0a0a0a",
            text_color="#ffffff",
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=5)
    
    def setup_input_area(self, parent):
        """Setup the input area"""
        input_frame = ctk.CTkFrame(parent, height=120, fg_color="#2a2a2a")
        input_frame.pack(fill="x", padx=10, pady=(5, 10))
        input_frame.pack_propagate(False)
        
        # Input field
        self.input_field = ctk.CTkTextbox(
            input_frame,
            height=60,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1a1a",
            text_color="#ffffff",
            placeholder_text="Type your message here..."
        )
        self.input_field.pack(fill="x", padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Send button
        self.send_button = ctk.CTkButton(
            buttons_frame,
            text="🚀 SEND",
            command=self.send_message,
            fg_color="#00ff41",
            text_color="#000000",
            hover_color="#00cc33",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.send_button.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ CLEAR",
            command=self.clear_chat,
            fg_color="#ff4444",
            hover_color="#cc3333"
        )
        clear_button.pack(side="left", padx=(0, 10))
        
        # Voice toggle button
        self.voice_toggle_button = ctk.CTkButton(
            buttons_frame,
            text="🎤 START VOICE",
            command=self.toggle_voice,
            fg_color="#4444ff",
            hover_color="#3333cc"
        )
        self.voice_toggle_button.pack(side="right")
        
        # Bind Enter key to send message
        self.input_field.bind("<Control-Return>", lambda e: self.send_message())
    
    def setup_voice_controls(self, parent):
        """Setup voice control panel"""
        voice_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a")
        voice_frame.pack(fill="x", padx=10, pady=10)
        
        # Voice header
        voice_header = ctk.CTkLabel(
            voice_frame,
            text="🎤 VOICE CONTROLS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff41"
        )
        voice_header.pack(pady=10)
        
        # Voice status
        self.voice_status = ctk.CTkLabel(
            voice_frame,
            text="Status: Inactive",
            font=ctk.CTkFont(size=12),
            text_color="#ffff00"
        )
        self.voice_status.pack(pady=5)
        
        # Voice commands info
        commands_text = ctk.CTkTextbox(
            voice_frame,
            height=100,
            font=ctk.CTkFont(size=10),
            fg_color="#1a1a1a"
        )
        commands_text.pack(fill="x", padx=10, pady=10)
        
        voice_commands = """🎯 VOICE COMMANDS:
• "JARVIS" - Wake up
• "Create file [name]" - File ops
• "What's the weather?" - Questions  
• "Write code for..." - Programming
• "Stop listening" - Pause voice
• "Shut down" - Exit voice mode"""
        
        commands_text.insert("1.0", voice_commands)
        commands_text.configure(state="disabled")
    
    def setup_file_operations(self, parent):
        """Setup file operations panel"""
        file_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a")
        file_frame.pack(fill="x", padx=10, pady=10)
        
        # File header
        file_header = ctk.CTkLabel(
            file_frame,
            text="📁 FILE OPERATIONS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff41"
        )
        file_header.pack(pady=10)
        
        # File buttons
        file_create_btn = ctk.CTkButton(
            file_frame,
            text="📄 Create File",
            command=self.create_file_dialog,
            fg_color="#4444ff"
        )
        file_create_btn.pack(pady=5, padx=10, fill="x")
        
        file_read_btn = ctk.CTkButton(
            file_frame,
            text="📖 Read File",
            command=self.read_file_dialog,
            fg_color="#4444ff"
        )
        file_read_btn.pack(pady=5, padx=10, fill="x")
        
        file_list_btn = ctk.CTkButton(
            file_frame,
            text="📋 List Files",
            command=self.list_files_dialog,
            fg_color="#4444ff"
        )
        file_list_btn.pack(pady=5, padx=10, fill="x")
    
    def setup_ai_controls(self, parent):
        """Setup AI model controls"""
        ai_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a")
        ai_frame.pack(fill="x", padx=10, pady=10)
        
        # AI header
        ai_header = ctk.CTkLabel(
            ai_frame,
            text="🧠 AI CONTROLS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff41"
        )
        ai_header.pack(pady=10)
        
        # Model selector
        model_label = ctk.CTkLabel(ai_frame, text="Model:", text_color="#ffffff")
        model_label.pack(pady=(10, 5))
        
        self.model_selector = ctk.CTkComboBox(
            ai_frame,
            values=[
                "deepseek/deepseek-r1-distill-qwen-32b",
                "anthropic/claude-3-haiku",
                "google/gemini-pro",
                "meta-llama/llama-3.1-8b-instruct"
            ],
            command=self.change_model
        )
        self.model_selector.pack(pady=5, padx=10, fill="x")
        self.model_selector.set(self.current_model)
        
        # AI status
        self.ai_status = ctk.CTkLabel(
            ai_frame,
            text="🟢 AI Ready",
            font=ctk.CTkFont(size=12),
            text_color="#00ff41"
        )
        self.ai_status.pack(pady=10)
    
    def setup_voice_integration(self):
        """Setup voice engine integration"""
        try:
            self.voice_engine = RobustVoiceEngine()
            # Override the voice engine's process_command to integrate with GUI
            self.voice_engine.original_process_command = self.voice_engine.process_command
            self.voice_engine.process_command = self.voice_command_handler
            print("✅ Voice integration ready")
        except Exception as e:
            print(f"❌ Voice integration error: {e}")
            self.voice_engine = None
    
    def voice_command_handler(self, command):
        """Handle voice commands and update GUI"""
        try:
            # Process command with AI
            response = self.voice_engine.original_process_command(command)
            
            # Update GUI
            self.root.after(0, lambda: self.add_message("You", command, "user"))
            self.root.after(0, lambda: self.add_message("JARVIS", response, "ai"))
            
            return response
        except Exception as e:
            print(f"❌ Voice command error: {e}")
            return "Voice command processing error."
    
    def add_message(self, sender, message, msg_type="user"):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        colors = {
            "user": "#00ff41",
            "ai": "#4da6ff", 
            "system": "#ff6b6b",
            "voice": "#ffaa00"
        }
        
        # Icons
        icons = {
            "user": "👤",
            "ai": "🤖",
            "system": "⚡",
            "voice": "🎤"
        }
        
        formatted_message = f"\n[{timestamp}] {icons.get(msg_type, '💬')} {sender}: {message}\n"
        
        self.chat_display.insert("end", formatted_message)
        self.chat_display.see("end")
        
        # Store in history
        self.conversation_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "type": msg_type
        })
    
    def send_message(self):
        """Send a message to the AI"""
        message = self.input_field.get("1.0", "end-1c").strip()
        if not message:
            return
        
        # Clear input
        self.input_field.delete("1.0", "end")
        
        # Add user message
        self.add_message("You", message, "user")
        
        # Update AI status
        self.ai_status.configure(text="🟡 Processing...", text_color="#ffff00")
        
        # Process with AI in background
        threading.Thread(target=self.process_ai_message, args=(message,), daemon=True).start()
    
    def process_ai_message(self, message):
        """Process message with AI engine"""
        try:
            # Get AI response
            response = self.ai_engine.chat(message)
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.add_message("JARVIS", response, "ai"))
            self.root.after(0, lambda: self.ai_status.configure(text="🟢 AI Ready", text_color="#00ff41"))
            
        except Exception as e:
            error_msg = f"AI processing error: {str(e)}"
            self.root.after(0, lambda: self.add_message("SYSTEM", error_msg, "system"))
            self.root.after(0, lambda: self.ai_status.configure(text="🔴 AI Error", text_color="#ff4444"))
    
    def toggle_voice(self):
        """Toggle voice recognition"""
        if not self.voice_engine:
            messagebox.showerror("Error", "Voice engine not available")
            return
        
        if not self.voice_active:
            # Start voice
            self.voice_active = True
            self.voice_toggle_button.configure(text="🔇 STOP VOICE")
            self.voice_status.configure(text="Status: Active", text_color="#00ff41")
            
            # Start voice thread
            self.voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
            self.voice_thread.start()
            
            self.add_message("SYSTEM", "Voice recognition activated", "system")
        else:
            # Stop voice
            self.voice_active = False
            self.voice_engine.voice_active = False
            self.voice_toggle_button.configure(text="🎤 START VOICE")
            self.voice_status.configure(text="Status: Inactive", text_color="#ffaa00")
            
            self.add_message("SYSTEM", "Voice recognition deactivated", "system")
    
    def voice_loop(self):
        """Voice recognition loop"""
        try:
            self.voice_engine.voice_active = True
            
            while self.voice_active and self.voice_engine.voice_active:
                # Listen for wake word or command
                if not self.voice_engine.conversation_active:
                    # Listen for wake word
                    text = self.voice_engine.listen_for_speech(timeout=2, phrase_timeout=4)
                    
                    if text and self.voice_engine.is_wake_word(text):
                        self.voice_engine.conversation_active = True
                        self.voice_engine.speak("Yes, Sir?")
                        self.root.after(0, lambda: self.add_message("JARVIS", "Voice activated", "voice"))
                        continue
                
                else:
                    # In conversation mode
                    text = self.voice_engine.listen_for_speech(timeout=6, phrase_timeout=10)
                    
                    if text:
                        # Process command (will update GUI through voice_command_handler)
                        response = self.voice_engine.process_command(text)
                        self.voice_engine.speak(response)
                    else:
                        # End conversation
                        self.voice_engine.speak("I'm here when you need me.")
                        self.voice_engine.conversation_active = False
                
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Voice loop error: {e}")
            self.root.after(0, lambda: self.add_message("SYSTEM", f"Voice error: {e}", "system"))
    
    def change_model(self, model):
        """Change AI model"""
        self.current_model = model
        self.ai_engine.set_model(model)
        self.add_message("SYSTEM", f"Switched to model: {model}", "system")
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.delete("1.0", "end")
        self.conversation_history = []
        self.add_message("SYSTEM", "Chat cleared", "system")
    
    def create_file_dialog(self):
        """Create file dialog"""
        filename = tk.simpledialog.askstring("Create File", "Enter filename:")
        if filename:
            content = tk.simpledialog.askstring("File Content", "Enter file content:")
            if content:
                try:
                    result = self.file_manager.create_file(filename, content)
                    self.add_message("FILE", f"Created: {filename}", "system")
                except Exception as e:
                    self.add_message("ERROR", f"File creation failed: {e}", "system")
    
    def read_file_dialog(self):
        """Read file dialog"""
        filename = filedialog.askopenfilename()
        if filename:
            try:
                result = self.file_manager.read_file(filename)
                self.add_message("FILE", f"Read file: {filename}", "system")
                self.add_message("CONTENT", result[:500] + "..." if len(result) > 500 else result, "system")
            except Exception as e:
                self.add_message("ERROR", f"File read failed: {e}", "system")
    
    def list_files_dialog(self):
        """List files dialog"""
        directory = filedialog.askdirectory()
        if directory:
            try:
                files = self.file_manager.list_files(directory)
                self.add_message("FILES", f"Directory: {directory}", "system")
                self.add_message("FILES", "\n".join(files[:20]), "system")
            except Exception as e:
                self.add_message("ERROR", f"File list failed: {e}", "system")
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Shutting down DEMON AI ASSISTANT...")
        finally:
            if self.voice_active:
                self.voice_active = False
            print("✅ DEMON AI ASSISTANT shutdown complete")

def main():
    """Main function"""
    print("🔥 STARTING JARVIS-X DEMON AI ASSISTANT...")
    print("=" * 50)
    
    try:
        app = DemonAIAssistant()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
