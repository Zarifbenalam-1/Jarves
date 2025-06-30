# jesko_gui.py - Koenigsegg Jesko-inspired GUI for JARVIS

class JeskoGUI:
    """
    Koenigsegg Jesko-inspired GUI for JARVIS
    Elegant, powerful, and lightweight design
    Optimized for 4GB RAM systems
    """
    
    def __init__(self):
        """Initialize the Jesko GUI theme and components"""
        # Jesko-inspired color scheme
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
        
        # Window configuration
        self.window_config = {
            'title': 'JARVIS - Koenigsegg Edition',
            'width': 1000,
            'height': 700,
            'resizable': True,
            'alpha': 0.95,  # Slight transparency for modern look
            'corner_radius': 10,  # Rounded corners
        }
        
        # Performance settings for low-end hardware
        self.performance_mode = {
            'hardware_acceleration': False,  # Disable for old GPUs
            'animation_enabled': False,      # Disable for very low-end systems
            'use_cached_rendering': True,    # Enable for better performance
            'lazy_loading': True,            # Load components only when needed
        }
        
        self.window = None
        self.customtkinter_loaded = False
        self.components = {}
        self.is_initialized = False
    
    def initialize(self, aggressive_mode=False):
        """
        Initialize the GUI with appropriate settings for the system
        
        Args:
            aggressive_mode (bool): Enable extreme performance optimizations
        """        # Try to import CustomTkinter - lightweight alternative to PyQt6
        try:
            import customtkinter as ctk
            self.ctk = ctk
            self.customtkinter_loaded = True
            print("✅ CustomTkinter loaded successfully")
        except ImportError:
            print("⚠️ CustomTkinter not found. Please run 'pip install customtkinter'")
            self.customtkinter_loaded = False
            
            # Set appearance mode and default color theme
            ctk.set_appearance_mode("Dark")
            ctk.set_default_color_theme("blue")  # We'll override most colors
            
        except ImportError:
            # Fallback to standard tkinter if CustomTkinter not available
            try:
                import tkinter as tk
                from tkinter import ttk
                self.tk = tk
                self.ttk = ttk
                print("CustomTkinter not available, falling back to standard tkinter")
            except ImportError:
                print("ERROR: Neither CustomTkinter nor tkinter available")
                return False
        
        # Adjust settings based on aggressive mode
        if aggressive_mode:
            self.performance_mode['animation_enabled'] = False
            self.performance_mode['use_cached_rendering'] = True
            self.performance_mode['lazy_loading'] = True
            # Reduce window size
            self.window_config['width'] = 800
            self.window_config['height'] = 600
        
        self.is_initialized = True
        return True
    
    def create_main_window(self):
        """
        Create the main application window with Jesko styling
        Returns a window object based on the chosen framework
        """
        if not self.is_initialized:
            success = self.initialize()
            if not success:
                return None
        
        if self.customtkinter_loaded:
            # Create window with CustomTkinter
            self.window = self.ctk.CTk()
            self.window.title(self.window_config['title'])
            self.window.geometry(f"{self.window_config['width']}x{self.window_config['height']}")
            self.window.configure(fg_color=self.theme['bg_color'])
            
            # Apply Jesko styling
            self._apply_jesko_style_ctk()
        else:
            # Fallback to standard tkinter
            self.window = self.tk.Tk()
            self.window.title(self.window_config['title'])
            self.window.geometry(f"{self.window_config['width']}x{self.window_config['height']}")
            self.window.configure(bg=self.theme['bg_color'])
            
            # Apply Jesko styling
            self._apply_jesko_style_tk()
        
        return self.window
    
    def _apply_jesko_style_ctk(self):
        """Apply Jesko styling to CustomTkinter"""
        # Set custom colors
        for widget in ["CTkButton", "CTkFrame", "CTkLabel", "CTkEntry", "CTkTextbox"]:
            self.ctk.set_widget_scaling(1.0)  # Normal scaling for low-end systems
            
    def _apply_jesko_style_tk(self):
        """Apply Jesko styling to standard tkinter"""
        style = self.ttk.Style()
        style.configure("TButton", background=self.theme['panel_color'], 
                       foreground=self.theme['text_color'], 
                       bordercolor=self.theme['accent_color'])
        style.configure("TButton", padding=6)  # Add padding to buttons
        
        style.configure("TFrame", background=self.theme['bg_color'])
        style.configure("TLabel", background=self.theme['bg_color'],
                       foreground=self.theme['text_color'])
    
    def create_chat_interface(self):
        """Create the chat interface component"""
        if not self.window:
            self.create_main_window()
        
        if self.customtkinter_loaded:
            # Create main frame
            chat_frame = self.ctk.CTkFrame(self.window, fg_color=self.theme['panel_color'])
            chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Chat history display
            chat_display = self.ctk.CTkTextbox(chat_frame, fg_color=self.theme['bg_color'],
                                           text_color=self.theme['text_color'],
                                           border_width=1,
                                           border_color=self.theme['accent_color'])
            chat_display.pack(fill="both", expand=True, padx=10, pady=10)
            chat_display.configure(state="disabled")  # Read-only
            
            # Input area
            input_frame = self.ctk.CTkFrame(chat_frame, fg_color=self.theme['panel_color'])
            input_frame.pack(fill="x", padx=10, pady=10)
            
            chat_input = self.ctk.CTkEntry(input_frame, placeholder_text="Message JARVIS...",
                                      fg_color=self.theme['bg_color'],
                                      text_color=self.theme['text_color'],
                                      border_color=self.theme['accent_color'])
            chat_input.pack(fill="x", expand=True, side="left", padx=(0, 10))
            
            send_button = self.ctk.CTkButton(input_frame, text="Send",
                                         fg_color=self.theme['accent_color'],
                                         text_color=self.theme['text_color'])
            send_button.pack(side="right")
            
            # Store components for later access
            self.components["chat_display"] = chat_display
            self.components["chat_input"] = chat_input
            self.components["send_button"] = send_button
            
            return chat_display, chat_input, send_button
    
    def add_message(self, message, is_user=True):
        """Add a message to the chat display"""
        if "chat_display" not in self.components:
            return
        
        chat_display = self.components["chat_display"]
        chat_display.configure(state="normal")
        
        # Format based on message type
        prefix = "You: " if is_user else "JARVIS: "
        tag = "user" if is_user else "jarvis"
        
        # Insert message with appropriate styling
        chat_display.insert("end", prefix, tag+"_prefix")
        chat_display.insert("end", message+"\n\n", tag)
        
        # Auto-scroll to bottom
        chat_display.see("end")
        chat_display.configure(state="disabled")
    
    def get_theme(self):
        """Get the current theme settings"""
        return self.theme
    
    def set_theme_variant(self, variant):
        """
        Change theme to a different Jesko variant
        
        Args:
            variant (str): 'attack' (red), 'absolut' (blue), or 'standard' (orange)
        """
        if variant == 'attack':
            self.theme['accent_color'] = '#FF3333'  # Aggressive red
        elif variant == 'absolut':
            self.theme['accent_color'] = '#00A8E0'  # Electric blue
        else:
            self.theme['accent_color'] = '#FF6B35'  # Jesko orange
        
        # Update UI if initialized
        if self.window:
            if self.customtkinter_loaded:
                self._apply_jesko_style_ctk()
            else:
                self._apply_jesko_style_tk()
    
    def run(self):
        """Run the GUI main loop"""
        if not self.window:
            self.create_main_window()
            self.create_chat_interface()
        
        self.window.mainloop()


# Example usage (for testing)
if __name__ == "__main__":
    gui = JeskoGUI()
    gui.initialize()
    gui.create_main_window()
    gui.create_chat_interface()
    
    # Test messages
    gui.add_message("Hello JARVIS, how are you today?", is_user=True)
    gui.add_message("I'm functioning perfectly, Sir. How may I assist you?", is_user=False)
    
    gui.run()
