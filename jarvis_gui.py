"""
JARVIS-X GUI Interface
Modern Iron Man-inspired interface for JARVIS AI Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import sys
import os
from datetime import datetime

# Add the project path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.ai_engine import JarvisAI

class JarvisGUI:
    def __init__(self):
        self.ai = JarvisAI()
        self.root = tk.Tk()
        self.message_queue = queue.Queue()
        
        # GUI State
        self.is_processing = False
        self.voice_enabled = False
        
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
        self.start_message_processor()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("JARVIS-X: Iron Man AI Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
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
            'warning': '#ffd43b',          # Warning yellow
            'error': '#ff5252'             # Error red
        }
        
        # Apply dark theme
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure styles
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom styles for widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles with Iron Man theme
        self.style.configure('Jarvis.TFrame', 
                           background=self.colors['bg_primary'])
        
        self.style.configure('JarvisPanel.TFrame', 
                           background=self.colors['bg_secondary'],
                           relief='raised', borderwidth=1)
        
        self.style.configure('Jarvis.TLabel', 
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10))
        
        self.style.configure('JarvisTitle.TLabel', 
                           background=self.colors['bg_primary'],
                           foreground=self.colors['accent_gold'],
                           font=('Segoe UI', 16, 'bold'))
        
        self.style.configure('Jarvis.TButton', 
                           background=self.colors['bg_accent'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9),
                           focuscolor='none')
        
        self.style.map('Jarvis.TButton',
                      background=[('active', self.colors['accent_blue']),
                                ('pressed', self.colors['accent_red'])])
        
        self.style.configure('JarvisAccent.TButton', 
                           background=self.colors['accent_red'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9, 'bold'),
                           focuscolor='none')
        
        self.style.map('JarvisAccent.TButton',
                      background=[('active', self.colors['accent_gold']),
                                ('pressed', self.colors['accent_blue'])])
                                
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Jarvis.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header()
        
        # Main content area (horizontal split)
        self.content_frame = ttk.Frame(self.main_frame, style='Jarvis.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel (chat and input)
        self.create_chat_panel()
        
        # Right panel (controls and info)
        self.create_control_panel()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self):
        """Create the header with JARVIS branding"""
        header_frame = ttk.Frame(self.main_frame, style='JarvisPanel.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # JARVIS logo/title
        title_label = ttk.Label(header_frame, 
                               text="🤖 JARVIS-X: Iron Man AI Assistant", 
                               style='JarvisTitle.TLabel')
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Master info
        master_info = self.ai.get_master_identity()
        master_label = ttk.Label(header_frame, 
                                text=f"Serving: {master_info['name']} ({master_info['title']})",
                                style='Jarvis.TLabel')
        master_label.pack(side=tk.RIGHT, padx=15, pady=10)
        
    def create_chat_panel(self):
        """Create the main chat interface"""
        # Chat panel container
        chat_container = ttk.Frame(self.content_frame, style='JarvisPanel.TFrame')
        chat_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Chat title
        chat_title = ttk.Label(chat_container, 
                              text="💬 Conversation with JARVIS", 
                              style='Jarvis.TLabel', 
                              font=('Segoe UI', 12, 'bold'))
        chat_title.pack(pady=(10, 5), padx=10, anchor=tk.W)
        
        # Chat display area
        self.create_chat_display(chat_container)
        
        # Input area
        self.create_input_area(chat_container)
        
    def create_chat_display(self, parent):
        """Create the chat display area"""
        # Chat frame with scrollbar
        chat_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Chat text widget with custom styling
        self.chat_display = tk.Text(chat_frame,
                                   bg=self.colors['bg_accent'],
                                   fg=self.colors['text_primary'],
                                   font=('Consolas', 10),
                                   wrap=tk.WORD,
                                   state=tk.DISABLED,
                                   cursor='arrow')
        
        # Scrollbar for chat
        chat_scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, 
                                      command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=chat_scrollbar.set)
        
        # Pack chat components
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags for different message types
        self.setup_chat_tags()
        
        # Add welcome message
        self.add_chat_message("JARVIS", "Good evening, Sir. JARVIS systems online and ready for your commands.", "system")
        
    def setup_chat_tags(self):
        """Setup text tags for different message types"""
        self.chat_display.tag_configure("user", 
                                       foreground=self.colors['accent_blue'],
                                       font=('Consolas', 10, 'bold'))
        
        self.chat_display.tag_configure("jarvis", 
                                       foreground=self.colors['accent_gold'],
                                       font=('Consolas', 10, 'bold'))
        
        self.chat_display.tag_configure("system", 
                                       foreground=self.colors['accent_red'],
                                       font=('Consolas', 10, 'italic'))
        
        self.chat_display.tag_configure("error", 
                                       foreground=self.colors['error'],
                                       font=('Consolas', 10))
        
        self.chat_display.tag_configure("success", 
                                       foreground=self.colors['success'],
                                       font=('Consolas', 10))
        
    def create_input_area(self, parent):
        """Create the input area for user messages"""
        input_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Input field
        self.input_field = tk.Text(input_frame,
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_primary'],
                                  font=('Segoe UI', 11),
                                  height=3,
                                  wrap=tk.WORD)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Button frame
        button_frame = ttk.Frame(input_frame, style='Jarvis.TFrame')
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Send button
        self.send_button = ttk.Button(button_frame,
                                     text="Send",
                                     style='JarvisAccent.TButton',
                                     command=self.send_message)
        self.send_button.pack(fill=tk.X, pady=(0, 2))
        
        # Clear button
        clear_button = ttk.Button(button_frame,
                                 text="Clear",
                                 style='Jarvis.TButton',
                                 command=self.clear_input)
        clear_button.pack(fill=tk.X)
        
    def create_control_panel(self):
        """Create the right control panel"""
        # Control panel container
        control_container = ttk.Frame(self.content_frame, style='JarvisPanel.TFrame')
        control_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        control_container.configure(width=300)
        
        # AI Settings section
        self.create_ai_settings(control_container)
        
        # File Operations section
        self.create_file_operations(control_container)
        
        # System Info section
        self.create_system_info(control_container)
        
    def create_ai_settings(self, parent):
        """Create AI settings section"""
        ai_frame = ttk.LabelFrame(parent, text="🧠 AI Settings", 
                                 style='JarvisPanel.TFrame')
        ai_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Current model display
        model_label = ttk.Label(ai_frame, text="Current Model:", style='Jarvis.TLabel')
        model_label.pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.model_var = tk.StringVar(value=self.ai.get_current_model())
        model_display = ttk.Label(ai_frame, textvariable=self.model_var, 
                                 style='Jarvis.TLabel', font=('Segoe UI', 9, 'bold'))
        model_display.pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        # Model selection button
        model_button = ttk.Button(ai_frame, text="Switch Model", 
                                 style='Jarvis.TButton',
                                 command=self.show_model_selection)
        model_button.pack(fill=tk.X, padx=10, pady=2)
        
        # Personality display
        personality_label = ttk.Label(ai_frame, text="Personality:", style='Jarvis.TLabel')
        personality_label.pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        self.personality_var = tk.StringVar(value=self.ai.get_current_personality().title())
        personality_display = ttk.Label(ai_frame, textvariable=self.personality_var, 
                                       style='Jarvis.TLabel', font=('Segoe UI', 9, 'bold'))
        personality_display.pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        # Personality selection button
        personality_button = ttk.Button(ai_frame, text="Change Personality", 
                                       style='Jarvis.TButton',
                                       command=self.show_personality_selection)
        personality_button.pack(fill=tk.X, padx=10, pady=2)
        
        # Auto personality toggle
        self.auto_personality_var = tk.BooleanVar(value=self.ai.is_auto_personality_enabled())
        auto_check = ttk.Checkbutton(ai_frame, text="Auto Personality", 
                                    variable=self.auto_personality_var,
                                    command=self.toggle_auto_personality,
                                    style='Jarvis.TCheckbutton')
        auto_check.pack(anchor=tk.W, padx=10, pady=5)
        
    def create_file_operations(self, parent):
        """Create file operations section"""
        file_frame = ttk.LabelFrame(parent, text="📁 File Operations", 
                                   style='JarvisPanel.TFrame')
        file_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # File operation buttons
        operations = [
            ("Create File", self.create_file_dialog),
            ("Read File", self.read_file_dialog),
            ("List Files", self.list_files_dialog),
            ("Create Project", self.create_project_dialog)
        ]
        
        for text, command in operations:
            button = ttk.Button(file_frame, text=text, 
                               style='Jarvis.TButton',
                               command=command)
            button.pack(fill=tk.X, padx=10, pady=2)
            
    def create_system_info(self, parent):
        """Create system information section"""
        info_frame = ttk.LabelFrame(parent, text="📊 System Info", 
                                   style='JarvisPanel.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipady=5)
        
        # System info text area
        self.info_display = tk.Text(info_frame,
                                   bg=self.colors['bg_accent'],
                                   fg=self.colors['text_secondary'],
                                   font=('Consolas', 8),
                                   height=8,
                                   state=tk.DISABLED)
        self.info_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Update system info
        self.update_system_info()
        
        # Auto-refresh button
        refresh_button = ttk.Button(info_frame, text="Refresh Info", 
                                   style='Jarvis.TButton',
                                   command=self.update_system_info)
        refresh_button.pack(fill=tk.X, padx=10, pady=(0, 5))
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_frame = ttk.Frame(self.main_frame, style='JarvisPanel.TFrame')
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status text
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                style='Jarvis.TLabel')
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Processing indicator
        self.processing_var = tk.StringVar(value="")
        processing_label = ttk.Label(self.status_frame, textvariable=self.processing_var,
                                    style='Jarvis.TLabel', foreground=self.colors['accent_blue'])
        processing_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def setup_bindings(self):
        """Setup keyboard and event bindings"""
        # Bind Enter key to send message (Ctrl+Enter for new line)
        self.input_field.bind('<Return>', self.on_enter_key)
        self.input_field.bind('<Control-Return>', self.insert_newline)
        
        # Focus on input field by default
        self.input_field.focus_set()
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not event.state & 0x4:  # If Ctrl is not pressed
            self.send_message()
            return 'break'  # Prevent default behavior
        
    def insert_newline(self, event):
        """Insert newline in input field"""
        self.input_field.insert(tk.INSERT, '\n')
        return 'break'
        
    def add_chat_message(self, sender, message, msg_type="normal"):
        """Add a message to the chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message based on sender
        if sender == "You":
            formatted_msg = f"[{timestamp}] 👤 {sender}: {message}\n\n"
            tag = "user"
        elif sender == "JARVIS":
            formatted_msg = f"[{timestamp}] 🤖 {sender}: {message}\n\n"
            tag = "jarvis"
        else:
            formatted_msg = f"[{timestamp}] {message}\n\n"
            tag = msg_type
        
        # Insert message with appropriate tag
        self.chat_display.insert(tk.END, formatted_msg, tag)
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        
        self.chat_display.configure(state=tk.DISABLED)
        
    def send_message(self):
        """Send user message to JARVIS"""
        if self.is_processing:
            return
            
        user_message = self.input_field.get(1.0, tk.END).strip()
        if not user_message:
            return
            
        # Add user message to chat
        self.add_chat_message("You", user_message)
        
        # Clear input field
        self.clear_input()
        
        # Process message in background thread
        self.is_processing = True
        self.update_status("Processing...")
        self.send_button.configure(state=tk.DISABLED)
        
        # Start processing thread
        thread = threading.Thread(target=self.process_message, args=(user_message,))
        thread.daemon = True
        thread.start()
        
    def process_message(self, message):
        """Process user message in background thread"""
        try:
            # Check if it's a command or chat
            if self.is_command(message):
                response = self.handle_command(message)
            else:
                # Regular AI chat
                response = self.ai.chat(message)
                
            # Send response back to main thread
            self.message_queue.put(('response', response))
            
        except Exception as e:
            self.message_queue.put(('error', f"Error processing message: {str(e)}"))
        finally:
            self.message_queue.put(('done', None))
            
    def is_command(self, message):
        """Check if message is a command"""
        message_lower = message.lower()
        commands = ['create file', 'read file', 'list files', 'create project', 
                   'search web', 'research', 'analyze code']
        return any(message_lower.startswith(cmd) for cmd in commands)
        
    def handle_command(self, message):
        """Handle command messages"""
        # Import the command handler from main
        from main import JarvisXTerminal
        
        # Create a temporary instance to use command handlers
        temp_jarvis = JarvisXTerminal()
        
        # Process the command based on type
        if message.startswith('create file'):
            temp_jarvis.handle_file_operations(message)
            return "File operation completed."
        elif message.startswith('read file'):
            temp_jarvis.handle_file_operations(message)
            return "File read operation completed."
        # Add more command handlers as needed
        
        return "Command processed."
        
    def start_message_processor(self):
        """Start the message processor for background threads"""
        def process_queue():
            try:
                while True:
                    msg_type, data = self.message_queue.get_nowait()
                    
                    if msg_type == 'response':
                        self.add_chat_message("JARVIS", data)
                    elif msg_type == 'error':
                        self.add_chat_message("SYSTEM", data, "error")
                    elif msg_type == 'done':
                        self.is_processing = False
                        self.update_status("Ready")
                        self.send_button.configure(state=tk.NORMAL)
                        
            except queue.Empty:
                pass
            
            # Schedule next check
            self.root.after(100, process_queue)
            
        # Start the processor
        self.root.after(100, process_queue)
        
    def clear_input(self):
        """Clear the input field"""
        self.input_field.delete(1.0, tk.END)
        
    def update_status(self, status):
        """Update status bar"""
        self.status_var.set(status)
        if status == "Processing...":
            self.processing_var.set("🔄")
        else:
            self.processing_var.set("")
            
    def show_model_selection(self):
        """Show model selection dialog"""
        # TODO: Implement model selection dialog
        messagebox.showinfo("Model Selection", "Model selection dialog coming soon!")
        
    def show_personality_selection(self):
        """Show personality selection dialog"""
        # TODO: Implement personality selection dialog
        messagebox.showinfo("Personality Selection", "Personality selection dialog coming soon!")
        
    def toggle_auto_personality(self):
        """Toggle auto personality switching"""
        self.ai.toggle_auto_personality()
        
    def create_file_dialog(self):
        """Show create file dialog"""
        filename = filedialog.asksaveasfilename(
            title="Create New File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.send_message_programmatically(f"create file {filename}")
            
    def read_file_dialog(self):
        """Show read file dialog"""
        filename = filedialog.askopenfilename(
            title="Select File to Read",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.send_message_programmatically(f"read file {filename}")
            
    def list_files_dialog(self):
        """Show list files dialog"""
        directory = filedialog.askdirectory(title="Select Directory to List")
        if directory:
            self.send_message_programmatically(f"list files {directory}")
            
    def create_project_dialog(self):
        """Show create project dialog"""
        # TODO: Implement project creation dialog
        messagebox.showinfo("Create Project", "Project creation dialog coming soon!")
        
    def send_message_programmatically(self, message):
        """Send a message programmatically"""
        self.input_field.delete(1.0, tk.END)
        self.input_field.insert(1.0, message)
        self.send_message()
        
    def update_system_info(self):
        """Update system information display"""
        self.info_display.configure(state=tk.NORMAL)
        self.info_display.delete(1.0, tk.END)
        
        # Get system info
        info_text = f"""Current Model: {self.ai.get_current_model()}
Personality: {self.ai.get_current_personality().title()}
Auto Personality: {'ON' if self.ai.is_auto_personality_enabled() else 'OFF'}

Master Identity:
{self.ai.get_master_identity()['name']} ({self.ai.get_master_identity()['title']})

Memory Status: Active
Voice Interface: Development

System Status: Online
GUI Version: 1.0.0
"""
        
        self.info_display.insert(1.0, info_text)
        self.info_display.configure(state=tk.DISABLED)
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point for GUI application"""
    try:
        print("🤖 Starting JARVIS GUI Interface...")
        print("🔧 Initializing components...")
        
        # Check dependencies
        try:
            import tkinter
            print("✅ tkinter available")
        except ImportError as e:
            print(f"❌ tkinter import error: {e}")
            return
            
        # Initialize and run
        app = JarvisGUI()
        print("✅ GUI initialized successfully")
        print("🚀 Launching JARVIS GUI...")
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 JARVIS GUI shutting down...")
    except Exception as e:
        print(f"❌ Error starting JARVIS GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
