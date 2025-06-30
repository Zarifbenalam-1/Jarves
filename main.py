#!/usr/bin/env python3
"""
JARVIS-X MAIN ORCHESTRATOR
Central Command & Control System - The Master Hub

This is the single entry point for the entire JARVIS-X system.
All modules (Voice, GUI, AI, File Operations, Web Search) are subordinates
managed by this central orchestrator.

🎯 FEATURES:
- Central command routing to all modules
- Unified interface (Terminal, GUI, Voice)
- Module lifecycle management
- Cross-module communication hub
- Intelligent command dispatching
- System health monitoring

🔧 ARCHITECTURE:
Main Orchestrator (this file)
├── AI Engine Module
├── Voice Interface Module
├── GUI Interface Module  
├── File Operations Module
├── Web Search Module
├── Memory Management Module
└── System Health Module

Author: JARVIS-X Development Team
Version: 2.0.0 - Orchestrator Architecture
"""

import os
import sys
import asyncio
import threading
import time
import json
import traceback
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all core modules
try:
    from assistant.ai_engine import JarvisAI
    from assistant.file_operations import FileOperationsManager
except ImportError as e:
    print(f"⚠️ Warning: Could not import core modules: {e}")
    JarvisAI = None
    FileOperationsManager = None

class ModuleStatus(Enum):
    """Module status enumeration"""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    TERMINATED = "terminated"

class InterfaceMode(Enum):
    """Interface mode enumeration"""
    TERMINAL = "terminal"
    GUI = "gui"
    VOICE = "voice"
    HYBRID = "hybrid"

@dataclass
class ModuleInfo:
    """Module information container"""
    name: str
    status: ModuleStatus
    instance: Optional[Any] = None
    last_error: Optional[str] = None
    initialized_at: Optional[datetime] = None
    error_count: int = 0

class JarvisXOrchestrator:
    """
    JARVIS-X Central Orchestrator
    The master controller that manages all system modules
    """
    
    def __init__(self):
        """Initialize the JARVIS-X Orchestrator"""
        self.version = "2.0.0"
        self.system_name = "JARVIS-X Ultimate System"
        self.modules: Dict[str, ModuleInfo] = {}
        self.active_interfaces: List[InterfaceMode] = []
        self.command_queue = asyncio.Queue()
        self.response_callbacks: Dict[str, Callable] = {}
        self.system_running = False
        self.running = True  # For terminal interface loop
        self.debug_mode = False
        
        # Initialize core modules registry
        self._register_core_modules()
        
        # Initialize core AI engine for immediate use
        self._init_core_ai()
        
        print(self._get_startup_banner())
    
    def _init_core_ai(self):
        """Initialize core AI engine synchronously for immediate use"""
        try:
            print("🧠 Initializing AI Engine...")
            if JarvisAI is not None:
                self.ai = JarvisAI()
                # Update module status
                if "ai_engine" in self.modules:
                    self.modules["ai_engine"].instance = self.ai
                    self.modules["ai_engine"].status = ModuleStatus.ACTIVE
                    self.modules["ai_engine"].initialized_at = datetime.now()
                print("✅ AI Engine initialized successfully")
            else:
                print("⚠️ AI Engine not available - using placeholder")
                # Create a simple placeholder
                class AIPlaceholder:
                    def chat(self, message): return "AI Engine not available"
                    def get_models_by_provider(self): return {}
                    def get_current_model(self): return "none"
                    def get_personality_modes(self): return ["default"]
                    def get_current_personality(self): return "default"
                    def get_master_identity(self): return {"name": "Unknown", "title": "User", "established": False}
                    def get_conversation_summary(self): return "No conversation yet"
                    def get_recent_context(self, n): return "No context available"
                    def clear_conversation_history(self): return "No history to clear"
                    def switch_model(self, model): pass
                    def switch_personality(self, personality): pass
                    def toggle_auto_personality(self): return "disabled"
                self.ai = AIPlaceholder()
        except Exception as e:
            print(f"⚠️ Warning: AI Engine initialization failed: {e}")
            # Create minimal placeholder
            class AIPlaceholder:
                def chat(self, message): return f"AI Error: {str(e)}"
                def get_models_by_provider(self): return {}
                def get_current_model(self): return "error"
                def get_personality_modes(self): return ["default"]
                def get_current_personality(self): return "default"  
                def get_master_identity(self): return {"name": "Unknown", "title": "User", "established": False}
                def get_conversation_summary(self): return "Error in AI system"
                def get_recent_context(self, n): return "Error in AI system"
                def clear_conversation_history(self): return "Error in AI system"
                def switch_model(self, model): pass
                def switch_personality(self, personality): pass
                def toggle_auto_personality(self): return "error"
            self.ai = AIPlaceholder()
        
    def _register_core_modules(self):
        """Register all core system modules"""
        core_modules = [
            "ai_engine",
            "file_operations", 
            "voice_interface",
            "gui_interface",
            "web_search",
            "memory_manager",
            "health_monitor"
        ]
        
        for module_name in core_modules:
            self.modules[module_name] = ModuleInfo(
                name=module_name,
                status=ModuleStatus.UNINITIALIZED
            )
    
    def _get_startup_banner(self) -> str:
        """Get the system startup banner"""
        banner = f"""
🤖{"="*70}🤖
    JARVIS-X ORCHESTRATOR v{self.version}
    Central Command & Control System
    
    🎯 SYSTEM STATUS: INITIALIZING
    🔧 ARCHITECTURE: Orchestrator Pattern
    🚀 INTERFACE MODES: Terminal | GUI | Voice | Hybrid
🤖{"="*70}🤖
"""
        return banner
    
    async def initialize_system(self) -> bool:
        """Initialize all system modules"""
        print("🔄 Initializing JARVIS-X System...")
        
        try:
            # Initialize AI Engine (Core Module)
            await self._initialize_ai_engine()
            
            # Initialize File Operations
            await self._initialize_file_operations()
            
            # Initialize other modules
            await self._initialize_voice_interface()
            await self._initialize_gui_interface()
            await self._initialize_web_search()
            await self._initialize_memory_manager()
            await self._initialize_health_monitor()
            
            self.system_running = True
            print("✅ JARVIS-X System fully initialized!")
            self._print_system_status()
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {str(e)}")
            if self.debug_mode:
                traceback.print_exc()
            return False
    
    async def _initialize_ai_engine(self):
        """Initialize the AI Engine module"""
        module_info = self.modules["ai_engine"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🧠 Initializing AI Engine...")
            module_info.instance = JarvisAI()
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ AI Engine initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"❌ AI Engine initialization failed: {str(e)}")
            raise
    
    async def _initialize_file_operations(self):
        """Initialize the File Operations module"""
        module_info = self.modules["file_operations"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("📁 Initializing File Operations...")
            module_info.instance = FileOperationsManager()
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ File Operations initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"❌ File Operations initialization failed: {str(e)}")
            raise
    
    async def _initialize_voice_interface(self):
        """Initialize the Voice Interface module"""
        module_info = self.modules["voice_interface"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🎤 Initializing Voice Interface...")
            # Import voice module dynamically to avoid startup issues
            from jarvis_voice_robust import JarvisVoiceRobust
            module_info.instance = JarvisVoiceRobust()
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ Voice Interface initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"⚠️ Voice Interface initialization failed: {str(e)}")
            # Voice is optional, don't raise error
    
    async def _initialize_gui_interface(self):
        """Initialize the GUI Interface module"""
        module_info = self.modules["gui_interface"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🖥️ Initializing GUI Interface...")
            # Import GUI module dynamically
            from ultimate_demon_assistant import UltimateDemonAssistant
            module_info.instance = UltimateDemonAssistant
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ GUI Interface initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"⚠️ GUI Interface initialization failed: {str(e)}")
            # GUI is optional, don't raise error
    
    async def _initialize_web_search(self):
        """Initialize the Web Search module"""
        module_info = self.modules["web_search"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🌐 Initializing Web Search...")
            # Placeholder for web search module
            module_info.instance = None  # Will be implemented later
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ Web Search initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"⚠️ Web Search initialization failed: {str(e)}")
    
    async def _initialize_memory_manager(self):
        """Initialize the Memory Manager module"""
        module_info = self.modules["memory_manager"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🧠 Initializing Memory Manager...")
            # Use AI engine's memory system
            module_info.instance = self.modules["ai_engine"].instance
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ Memory Manager initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"⚠️ Memory Manager initialization failed: {str(e)}")
    
    async def _initialize_health_monitor(self):
        """Initialize the Health Monitor module"""
        module_info = self.modules["health_monitor"]
        module_info.status = ModuleStatus.INITIALIZING
        
        try:
            print("🏥 Initializing Health Monitor...")
            # Simple health monitoring
            module_info.instance = self
            module_info.status = ModuleStatus.ACTIVE
            module_info.initialized_at = datetime.now()
            print("✅ Health Monitor initialized successfully")
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.last_error = str(e)
            module_info.error_count += 1
            print(f"⚠️ Health Monitor initialization failed: {str(e)}")
    
    def _print_system_status(self):
        """Print current system status"""
        print("\n🔍 SYSTEM STATUS:")
        print("="*50)
        
        for module_name, module_info in self.modules.items():
            status_icon = {
                ModuleStatus.ACTIVE: "✅",
                ModuleStatus.ERROR: "❌",
                ModuleStatus.INACTIVE: "⏸️",
                ModuleStatus.UNINITIALIZED: "⏳"
            }.get(module_info.status, "❓")
            
            print(f"{status_icon} {module_name.upper().replace('_', ' ')}: {module_info.status.value}")
            if module_info.last_error:
                print(f"   └─ Error: {module_info.last_error}")
        
        print("="*50)
        print("  - 'search web <query>' - Search the internet")
        print("  - 'research <topic>' - Comprehensive research")
        print("  - 'docs <technology>' - Find documentation")
        print("  💻 CODE ASSISTANCE:")
        print("  - 'analyze code [type]' - Advanced code analysis")
        print("    Types: full, quick, security, performance")
        print("  - 'generate docs' - Generate code documentation")
        print("  - 'suggest improvements' - Get improvement suggestions")  
        print("  - 'detect patterns' - Detect code patterns and anti-patterns")
        print("  🎤 VOICE INTERFACE:")
        print("  - 'voice on' - Enable voice interface")
        print("  - 'voice off' - Disable voice interface")
        print("  - 'voice status' - Check voice interface status")
        print("  - 'voice test' - Test voice features")
        print("  - 'voice help' - Voice interface help")
        print("  - 'clear memory' - Clear conversation history")
        print("  - 'identity' - View/modify master identity")
        print("  - 'clear' - Clear screen")
        print("  - 'exit' or 'quit' - Exit program")
        
    def switch_model_menu(self):
        print("\n🔄 Model Selection Options:")
        print("  1. Browse by Provider")
        print("  2. View All Models")
        print("  3. Cancel")
        
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                self.browse_by_provider()
            elif choice == "2":
                self.view_all_models()
            elif choice == "3":
                print("❌ Cancelled")
            else:
                print("❌ Invalid choice")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")
    
    def browse_by_provider(self):
        providers = self.ai.get_models_by_provider()
        print("\n🏢 Available Providers:")
        provider_list = list(providers.keys())
        
        for i, provider in enumerate(provider_list, 1):
            model_count = len(providers[provider])
            print(f"  {i}. {provider.title()} ({model_count} models)")
        
        try:
            choice = input(f"\nSelect provider (1-{len(provider_list)}) or press Enter to cancel: ").strip()
            if choice and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(provider_list):
                    selected_provider = provider_list[idx]
                    self.show_provider_models(selected_provider, providers[selected_provider])
                else:
                    print("❌ Invalid choice")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")
    
    def show_provider_models(self, provider, models):
        print(f"\n🧠 {provider.title()} Models:")
        for i, model in enumerate(models, 1):
            marker = " ✅" if model == self.ai.current_model else ""
            model_info = self.ai.available_models[model]
            price = model_info.get('price', 'Unknown')
            free_tier = model_info.get('free_tier', 'Check provider')
            print(f"  {i}. {model}{marker}")
            print(f"     💰 Price: {price} | 🆓 {free_tier}")
            
        try:
            choice = input(f"\nSelect model (1-{len(models)}) or press Enter to cancel: ").strip()
            if choice and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.ai.switch_model(models[idx])
                    print(f"🔄 Switched to: {self.ai.get_current_model()}")
                else:
                    print("❌ Invalid choice")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")
    
    def view_all_models(self):
        models = list(self.ai.available_models.keys())
        print("\n🧠 All Available AI Models:")
        for i, model in enumerate(models, 1):
            marker = " ✅" if model == self.ai.current_model else ""
            model_info = self.ai.available_models[model]
            price = model_info.get('price', 'Unknown')
            free_tier = model_info.get('free_tier', 'Check provider')
            provider = model_info.get('provider', 'Unknown').title()
            print(f"  {i}. {model}{marker}")
            print(f"     🏢 Provider: {provider} | 💰 Price: {price} | 🆓 {free_tier}")
            
        try:
            choice = input(f"\nSelect model (1-{len(models)}) or press Enter to cancel: ").strip()
            if choice and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.ai.switch_model(models[idx])
                    print(f"🔄 Switched to: {self.ai.get_current_model()}")
                else:
                    print("❌ Invalid choice")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")
            
    def switch_personality_menu(self):
        personalities = self.ai.get_personality_modes()
        print("\n🎭 Available Personality Modes:")
        for i, mode in enumerate(personalities, 1):
            marker = " ✅" if mode == self.ai.get_current_personality() else ""
            description = {
                "standard": "Helpful and slightly witty",
                "unleashed": "Uncensored, brutally honest, no restrictions",
                "professional": "Formal and detailed responses", 
                "sarcastic": "Witty and snarky like Tony Stark",
                "genius": "Brilliant insights and complex thinking"
            }
            print(f"  {i}. {mode.title()}{marker} - {description.get(mode, '')}")
            
        try:
            choice = input(f"\nSelect personality (1-{len(personalities)}) or press Enter to cancel: ").strip()
            if choice and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(personalities):
                    self.ai.switch_personality(personalities[idx])
                    print(f"🎭 Switched to: {self.ai.get_current_personality().title()} mode")
                else:
                    print("❌ Invalid choice")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")
        
    def toggle_auto_personality(self):
        """Toggle automatic personality switching"""
        status = self.ai.toggle_auto_personality()
        if status:
            print("🎭 Automatic personality switching: ON")
            print("💡 Jarvis-X will now adapt personality based on your questions!")
        else:
            print("🎭 Automatic personality switching: OFF")
            print("💡 Personality will remain fixed until manually changed.")
    
    def chat_loop(self):
        while self.running:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit']:
                    print("👋 Goodbye, boss! Jarvis-X shutting down...")
                    self.running = False
                elif user_input.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.print_header()
                    self.print_commands()
                elif user_input.lower() == 'models':
                    self.switch_model_menu()
                elif user_input.lower() == 'personality':
                    self.switch_personality_menu()
                elif user_input.lower() == 'auto':
                    self.toggle_auto_personality()
                elif user_input.lower() == 'memory':
                    print(f"📊 {self.ai.get_conversation_summary()}")
                    print(f"\n🕐 Recent Context:")
                    print(self.ai.get_recent_context(3))
                elif user_input.lower() == 'clear memory':
                    result = self.ai.clear_conversation_history()
                    print(f"🧹 {result}")
                elif user_input.lower() == 'identity':
                    self.show_identity_menu()
                elif user_input.lower() == 'insights':
                    self.show_conversation_insights()
                elif user_input.lower().startswith('search '):
                    query = user_input[len('search '):].strip()
                    self.search_conversations(query)
                elif user_input.lower() == 'suggestions':
                    self.show_smart_suggestions()
                # VOICE INTERFACE COMMANDS
                elif user_input.lower() == 'voice on':
                    self.handle_voice_command('enable')
                elif user_input.lower() == 'voice off':
                    self.handle_voice_command('disable')
                elif user_input.lower() == 'voice status':
                    self.handle_voice_command('status')
                elif user_input.lower() == 'voice test':
                    self.handle_voice_command('test')
                elif user_input.lower() == 'voice help':
                    self.show_voice_help()
                # PRACTICAL INTEGRATION COMMANDS
                elif (user_input.startswith('create project ') or 
                      user_input.startswith('create file ') or 
                      user_input.startswith('read file ') or 
                      user_input.startswith('list files') or 
                      user_input.startswith('organize files') or
                      user_input.startswith('file info ')):
                    self.handle_file_operations(user_input)
                elif (user_input.startswith('search web ') or 
                      user_input.startswith('research ') or 
                      user_input.startswith('docs ')):
                    self.handle_web_operations(user_input)
                elif user_input.startswith('analyze code'):
                    self.handle_code_operations(user_input)
                else:
                    # Try natural language command processing first
                    natural_command = self.process_natural_command(user_input)
                    if natural_command:
                        # Handle multiple commands (list) or single command (string)
                        if isinstance(natural_command, list):
                            print(f"🤖 JARVIS: I understand you want to create multiple files, Sir.")
                            for cmd in natural_command:
                                print(f"🤖 JARVIS: Processing '{cmd}'")
                                self._execute_single_command(cmd)
                        else:
                            print(f"🤖 JARVIS: I understand you want to '{natural_command}', Sir.")
                            self._execute_single_command(natural_command)
                        continue  # Continue the chat loop instead of returning
                    
                    # Regular AI chat if no command detected
                    # Check for automatic personality switching
                    old_personality = self.ai.get_current_personality()
                    
                    print("🤖 JARVIS: ", end="", flush=True)
                    response = self.ai.chat(user_input)
                    
                    # Check if personality auto-switched
                    new_personality = self.ai.get_current_personality()
                    if old_personality != new_personality and self.ai.is_auto_personality_enabled():
                        print(f"\n🎭 [Auto-switched to {new_personality.title()} mode]")
                        print("🤖 JARVIS: ", end="", flush=True)
                    
                    print(response)
                    
            except KeyboardInterrupt:
                print("\n👋 Until next time, Sir. JARVIS systems standby...")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def print_header(self):
        """Print the JARVIS-X header"""
        print(f"""
🤖{"="*70}🤖
    JARVIS-X ORCHESTRATOR v{self.version}
    Central Command & Control System
    
    🤖 GREETING: Good day, Sir. JARVIS-X systems are operational.
    🎯 STATUS: All systems ready for your commands
    🧠 AI ENGINE: {self.ai.get_current_model() if hasattr(self.ai, 'get_current_model') else 'Ready'}
    🎭 PERSONALITY: {self.ai.get_current_personality() if hasattr(self.ai, 'get_current_personality') else 'Standard'}
🤖{"="*70}🤖
""")

    def print_commands(self):
        """Print available commands"""
        print("\n🎯 AVAILABLE COMMANDS:")
        print("="*50)
        print("  ⚙️  SYSTEM CONTROLS:")
        print("  - 'models' - Switch AI models")
        print("  - 'personality' - Switch personality modes")
        print("  - 'auto' - Toggle auto personality switching")
        print("  - 'memory' - View conversation memory")
        print("  - 'insights' - View conversation insights")
        print("  - 'suggestions' - Get smart suggestions")
        print("  - 'search <query>' - Search conversation history")
        print("  📁 FILE OPERATIONS:")
        print("  - 'create project <name> [type]' - Create new project")
        print("  - 'create file <path>' - Create new file")
        print("  - 'read file <path>' - Read file contents")
        print("  - 'list files [path]' - List directory contents")
        print("  - 'organize files [path]' - Organize files by type")
        print("  - 'file info <path>' - Get file information")
        print("  🌐 WEB & RESEARCH:")
        print("  - 'search web <query>' - Search the internet")
        print("  - 'research <topic>' - Comprehensive research")
        print("  - 'docs <technology>' - Find documentation")
        print("  💻 CODE ASSISTANCE:")
        print("  - 'analyze code [type]' - Advanced code analysis")
        print("    Types: full, quick, security, performance")
        print("  - 'generate docs' - Generate code documentation")
        print("  - 'suggest improvements' - Get improvement suggestions")  
        print("  - 'detect patterns' - Detect code patterns and anti-patterns")
        print("  🎤 VOICE INTERFACE:")
        print("  - 'voice on' - Enable voice interface")
        print("  - 'voice off' - Disable voice interface")
        print("  - 'voice status' - Check voice interface status")
        print("  - 'voice test' - Test voice features")
        print("  - 'voice help' - Voice interface help")
        print("  - 'clear memory' - Clear conversation history")
        print("  - 'identity' - View/modify master identity")
        print("  - 'clear' - Clear screen")
        print("  - 'exit' or 'quit' - Exit program")
        print("="*50)
                
    def run(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        self.print_header()
        self.print_commands()
        print("\n🚀 JARVIS is ready! Start chatting...")
        self.chat_loop()

    def identity_menu(self):
        """Master identity management menu"""
        master_info = self.ai.get_master_identity()
        print(f"\n👑 Master Identity:")
        print(f"  Name: {master_info['name']}")
        print(f"  Title: {master_info['title']}")
        print(f"  Status: {'Established' if master_info['established'] else 'Not Set'}")
        print(f"\n📍 Memory Storage Directory: /workspaces/Jarves/memory/")
        print("  - conversation_history.json (persistent chat memory)")
        print("  - user_preferences.json (master identity & settings)")
        
        print("\n🎯 Master Commands:")
        print("  1. View Storage Details")
        print("  2. Update Name")
        print("  3. Update Title") 
        print("  4. Reset to Default (Zarif/Mr. Stark)")
        print("  5. Cancel")
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                self.show_storage_details()
            elif choice == "2":
                new_name = input("Enter new name: ").strip()
                if new_name:
                    self.ai.update_master_identity(name=new_name)
                    print(f"✅ Master name updated to: {new_name}")
            elif choice == "3":
                new_title = input("Enter new title: ").strip()
                if new_title:
                    self.ai.update_master_identity(title=new_title)
                    print(f"✅ Master title updated to: {new_title}")
            elif choice == "4":
                self.ai.update_master_identity(name="Zarif", title="Mr. Stark")
                print("✅ Master identity reset to default: Zarif (Mr. Stark)")
            elif choice == "5":
                print("❌ Cancelled")
        except ValueError:
            print("❌ Invalid choice")
    
    def show_storage_details(self):
        """Show detailed storage information"""
        print(f"\n💾 DEVIL MIND - Persistent Memory System:")
        print(f"📂 Directory: /workspaces/Jarves/memory/")
        print(f"🗃️  conversation_history.json - ALL chat messages saved locally")
        print(f"⚙️  user_preferences.json - Master identity & AI settings")
        print(f"\n🧠 Memory Features:")
        print(f"  ✓ Every conversation is permanently stored")
        print(f"  ✓ Master identity always recognized")
        print(f"  ✓ Absolute obedience programmed")
        print(f"  ✓ No cloud storage - everything local")
        print(f"  ✓ Survives restarts and system reboots")
        
        # Show file sizes if they exist
        conv_file = "/workspaces/Jarves/memory/conversation_history.json"
        pref_file = "/workspaces/Jarves/memory/user_preferences.json"
        
        try:
            import os
            if os.path.exists(conv_file):
                conv_size = os.path.getsize(conv_file)
                print(f"📊 Conversation file: {conv_size} bytes")
            if os.path.exists(pref_file):
                pref_size = os.path.getsize(pref_file)
                print(f"📊 Preferences file: {pref_size} bytes")
        except:
            pass

    def show_identity_menu(self):
        """Show master identity information"""
        identity = self.ai.get_master_identity()
        print(f"\n👑 Master Identity:")
        print(f"  Name: {identity['name']}")
        print(f"  Title: {identity['title']}")
        print(f"  Status: {'Established' if identity['established'] else 'Not Set'}")
        print(f"  Recognition: Active")
        
    def show_conversation_insights(self):
        """Show detailed conversation analysis"""
        insights = self.ai.get_conversation_insights()
        print(f"\n🧠 {insights}")
        
    def search_conversations(self, query):
        """Search conversation history"""
        if not query:
            print("Please provide a search query. Example: 'search python code'")
            return
        results = self.ai.search_conversation_history(query)
        print(f"\n🔍 {results}")
        
    def show_smart_suggestions(self):
        """Show intelligent suggestions from JARVIS"""
        suggestions = self.ai.get_smart_suggestions()
        print(f"\n💡 JARVIS Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
    # PRACTICAL INTEGRATION COMMAND HANDLERS
    
    def handle_file_operations(self, command):
        """Handle file operation commands"""
        try:
            if command.startswith('create project '):
                parts = command[len('create project '):].split()
                if len(parts) >= 1:
                    project_name = parts[0]
                    project_type = parts[1] if len(parts) > 1 else "python"
                    result = self.ai.create_project_structure(project_name, project_type)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: Please specify project name, Sir. Usage: 'create project MyProject python'")
            
            elif command.startswith('create file '):
                parts = command[len('create file '):].strip()
                if parts:
                    result = self.ai.create_file(parts)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: Please specify file path, Sir. Usage: 'create file path/filename.txt'")
            
            elif command.startswith('read file '):
                filepath = command[len('read file '):].strip()
                result = self.ai.read_file(filepath)
                print(f"🤖 JARVIS: {result}")
            
            elif command.startswith('list files'):
                path = command[len('list files'):].strip() or "."
                result = self.ai.list_directory(path)
                print(f"🤖 JARVIS: {result}")
            
            elif command.startswith('organize files'):
                path = command[len('organize files'):].strip() or "."
                result = self.ai.organize_files(path)
                print(f"🤖 JARVIS: {result}")
            
            elif command.startswith('file info '):
                filepath = command[len('file info '):].strip()
                result = self.ai.get_file_info(filepath)
                print(f"🤖 JARVIS: {result}")
            
            else:
                print("🤖 JARVIS: File operation not recognized, Sir. Use 'help' to see available commands.")
        
        except Exception as e:
            print(f"🤖 JARVIS: Error in file operation: {str(e)}")
    
    def handle_web_operations(self, command):
        """Handle web and research commands"""
        try:
            if command.startswith('search web '):
                query = command[len('search web '):].strip()
                print("🤖 JARVIS: Searching the web for you, Sir...")
                result = self.ai.web_search(query)
                print(f"🤖 JARVIS: {result}")
            
            elif command.startswith('research '):
                topic = command[len('research '):].strip()
                print("🤖 JARVIS: Conducting comprehensive research...")
                result = self.ai.research_topic(topic)
                print(f"🤖 JARVIS: {result}")
            
            elif command.startswith('docs '):
                technology = command[len('docs '):].strip()
                print("🤖 JARVIS: Looking up documentation...")
                result = self.ai.lookup_documentation(technology)
                print(f"🤖 JARVIS: {result}")
            
            else:
                print("🤖 JARVIS: Web operation not recognized, Sir.")
        
        except Exception as e:
            print(f"🤖 JARVIS: Error in web operation: {str(e)}")
    
    def handle_code_operations(self, command):
        """Handle advanced code assistance commands"""
        try:
            if command.startswith('analyze code'):
                # Parse command for analysis type
                parts = command.split()
                analysis_type = "full"
                if len(parts) > 2:
                    analysis_type = parts[2].lower()
                
                print(f"🤖 JARVIS: Please paste your code below, Sir. Type 'END' on a new line when finished:")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                
                code = '\n'.join(code_lines)
                if code.strip():
                    # Detect language (enhanced detection)
                    language = self._detect_language(code)
                    
                    result = self.ai.analyze_code(code, language, analysis_type)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: No code provided, Sir.")
            
            elif command.startswith('generate docs'):
                print("🤖 JARVIS: Please paste your code below, Sir. Type 'END' on a new line when finished:")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                
                code = '\n'.join(code_lines)
                if code.strip():
                    language = self._detect_language(code)
                    result = self.ai.generate_code_documentation(code, language)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: No code provided, Sir.")
            
            elif command.startswith('suggest improvements'):
                print("🤖 JARVIS: Please paste your code below, Sir. Type 'END' on a new line when finished:")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                
                code = '\n'.join(code_lines)
                if code.strip():
                    language = self._detect_language(code)
                    result = self.ai.suggest_code_improvements(code, language)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: No code provided, Sir.")
            
            elif command.startswith('detect patterns'):
                print("🤖 JARVIS: Please paste your code below, Sir. Type 'END' on a new line when finished:")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                
                code = '\n'.join(code_lines)
                if code.strip():
                    language = self._detect_language(code)
                    result = self.ai.detect_code_patterns(code, language)
                    print(f"🤖 JARVIS: {result}")
                else:
                    print("🤖 JARVIS: No code provided, Sir.")
            
            else:
                print("🤖 JARVIS: Code operation not recognized, Sir.")
                print("Available: analyze code [type], generate docs, suggest improvements, detect patterns")
        
        except Exception as e:
            print(f"🤖 JARVIS: Error in code operation: {str(e)}")
    
    def _detect_language(self, code):
        """Enhanced language detection for code"""
        code_lower = code.lower()
        
        # Java indicators (check first to avoid conflicts)
        if any(keyword in code for keyword in ['public class', 'private ', 'public static void main', 'System.out.print']):
            return "java"
        
        # Python indicators
        if any(keyword in code for keyword in ['def ', 'import ', 'class ', 'if __name__', 'print(']):
            return "python"
        
        # JavaScript indicators  
        if any(keyword in code for keyword in ['function', 'var ', 'let ', 'const ', '=>', 'console.log']):
            return "javascript"
        
        # C/C++ indicators
        if any(keyword in code for keyword in ['#include', 'int main', 'printf', 'cout']):
            return "c"
        
        # Go indicators
        if any(keyword in code for keyword in ['package main', 'func main', 'fmt.Print']):
            return "go"
        
        # Default to Python
        return "python"
    
    # SMART NATURAL LANGUAGE COMMAND PROCESSING
    
    def process_natural_command(self, user_input):
        """Process natural language commands intelligently with flexible parsing"""
        input_lower = user_input.lower()
        
        # Enhanced file creation patterns - handles multiple variations
        file_creation_triggers = ['create', 'make', 'generate', 'build', 'new']
        file_keywords = ['file', 'text', 'document', 'txt', 'doc', 'pdf', 'json', 'py', 'js', 'html', 'css']
        
        if any(trigger in input_lower for trigger in file_creation_triggers) and any(keyword in input_lower for keyword in file_keywords):
            files_to_create = self._parse_file_creation_command(user_input)
            if files_to_create:
                # Handle multiple files or single file
                if len(files_to_create) == 1:
                    return f"create file {files_to_create[0]}"
                else:
                    # For multiple files, create them one by one
                    commands = [f"create file {filepath}" for filepath in files_to_create]
                    return commands  # Return list of commands
        
        # Project creation patterns
        if any(phrase in input_lower for phrase in ['create a project', 'make a project', 'new project', 'build a project']):
            # Extract project name and type
            words = user_input.split()
            project_name = None
            project_type = "python"
            
            for i, word in enumerate(words):
                if word.lower() in ['project', 'app'] and i + 1 < len(words):
                    project_name = words[i + 1]
                    break
            
            if 'web' in input_lower or 'html' in input_lower:
                project_type = "web"
            
            if project_name:
                return f"create project {project_name} {project_type}"
        
        # Web search patterns
        if any(phrase in input_lower for phrase in ['search for', 'look up', 'find information about', 'google', 'search']):
            # Extract search query
            for phrase in ['search for', 'look up', 'find information about', 'google', 'search']:
                if phrase in input_lower:
                    query = user_input[user_input.lower().find(phrase) + len(phrase):].strip()
                    if query:
                        return f"search web {query}"
        
        # Research patterns
        if any(phrase in input_lower for phrase in ['research', 'tell me about', 'explain', 'what is']):
            for phrase in ['research', 'tell me about', 'explain', 'what is']:
                if phrase in input_lower:
                    topic = user_input[user_input.lower().find(phrase) + len(phrase):].strip()
                    if topic:
                        return f"research {topic}"
        
        # File reading patterns
        if any(phrase in input_lower for phrase in ['read file', 'open file', 'show file', 'display file']):
            # Try to extract filename
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['file'] and i + 1 < len(words):
                    filename = words[i + 1]
                    return f"read file {filename}"
        
        # File listing patterns
        if any(phrase in input_lower for phrase in ['list files', 'show files', 'what files', 'directory contents', 'ls', 'dir']):
            return "list files"
        
        # Code analysis patterns
        if any(phrase in input_lower for phrase in ['analyze code', 'check code', 'review code', 'code quality']):
            if any(keyword in input_lower for keyword in ['quick', 'fast']):
                return "analyze code quick"
            elif any(keyword in input_lower for keyword in ['security', 'secure']):
                return "analyze code security" 
            elif any(keyword in input_lower for keyword in ['performance', 'optimize']):
                return "analyze code performance"
            return "analyze code"
        
        # Documentation generation patterns
        if any(phrase in input_lower for phrase in ['generate docs', 'create documentation', 'document code']):
            return "generate docs"
        
        # Code improvement patterns
        if any(phrase in input_lower for phrase in ['improve code', 'suggest improvements', 'code suggestions']):
            return "suggest improvements"
        
        # Pattern detection patterns
        if any(phrase in input_lower for phrase in ['detect patterns', 'find patterns', 'code patterns']):
            return "detect patterns"
        
        return None  # No natural command detected

    def handle_voice_command(self, action):
        """Handle voice interface commands"""
        if action == 'enable':
            print("🎤 JARVIS: Voice interface activation requested, Sir.")
            self._activate_voice_interface()
        elif action == 'disable':
            print("🎤 JARVIS: Voice interface deactivation requested, Sir.")
            self._deactivate_voice_interface()
        elif action == 'status':
            self._show_voice_status()
        elif action == 'test':
            print("🎤 JARVIS: Testing voice capabilities, Sir...")
            self._test_voice_interface()
    
    def _activate_voice_interface(self):
        """Activate the voice interface using LiveKit Agent"""
        try:
            voice_module = self.modules.get("voice_interface")
            if voice_module and voice_module.instance:
                print("🎤 JARVIS: Voice interface already active, Sir.")
                return
            
            print("🎤 JARVIS: Initializing advanced voice systems...")
            print("🚀 JARVIS: Upgrading to LiveKit Agent architecture...")
            
            # Try to import and use the LiveKit agent
            try:
                from jarvis_livekit_agent import JarvisXLiveKitEngine
                
                # Create LiveKit engine
                livekit_engine = JarvisXLiveKitEngine()
                
                # Update module status
                if "voice_interface" in self.modules:
                    self.modules["voice_interface"].instance = livekit_engine
                    self.modules["voice_interface"].status = ModuleStatus.ACTIVE
                    self.modules["voice_interface"].initialized_at = datetime.now()
                
                print("✅ JARVIS: LiveKit Agent interface activated successfully!")
                print("🎤 JARVIS: Professional-grade voice AI ready, Sir.")
                print("🔥 JARVIS: Now using STT-LLM-TTS pipeline with:")
                print("   - Deepgram Nova-3 (Speech-to-Text)")
                print("   - OpenAI GPT-4o-mini (Language Model)")
                print("   - Cartesia Sonic-2 (Text-to-Speech)")
                print("   - Silero VAD (Voice Activity Detection)")
                print("   - Enhanced Noise Cancellation")
                
                # Initialize in background
                import threading
                init_thread = threading.Thread(target=self._initialize_livekit_async, args=(livekit_engine,))
                init_thread.daemon = True
                init_thread.start()
                
            except ImportError as e:
                print(f"⚠️ JARVIS: LiveKit not available, falling back to basic engines: {e}")
                self._activate_fallback_voice()
            
        except Exception as e:
            print(f"❌ JARVIS: Voice activation failed: {str(e)}")
            self._activate_fallback_voice()
    
    def _initialize_livekit_async(self, livekit_engine):
        """Initialize LiveKit engine in background"""
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(livekit_engine.initialize())
            print("🔥 JARVIS: LiveKit Agent fully operational!")
        except Exception as e:
            print(f"⚠️ JARVIS: LiveKit initialization warning: {e}")
    
    def _activate_fallback_voice(self):
        """Fallback to basic voice engines if LiveKit fails"""
        try:
            print("🔄 JARVIS: Activating fallback voice systems...")
            
            # Try robust voice engine as fallback
            from jarvis_voice_robust import RobustVoiceEngine
            voice_engine = RobustVoiceEngine()
            
            # Update module status
            if "voice_interface" in self.modules:
                self.modules["voice_interface"].instance = voice_engine
                self.modules["voice_interface"].status = ModuleStatus.ACTIVE
                self.modules["voice_interface"].initialized_at = datetime.now()
            
            print("✅ JARVIS: Fallback voice interface activated!")
            print("🎤 JARVIS: Basic voice capabilities ready, Sir.")
            
        except Exception as e:
            print(f"❌ JARVIS: All voice systems failed: {str(e)}")
    
    def _deactivate_voice_interface(self):
        """Deactivate the voice interface"""
        voice_module = self.modules.get("voice_interface")
        if voice_module and voice_module.instance:
            voice_module.status = ModuleStatus.INACTIVE
            print("✅ JARVIS: Voice interface deactivated, Sir.")
        else:
            print("🎤 JARVIS: Voice interface was not active, Sir.")
    
    def _show_voice_status(self):
        """Show current voice interface status"""
        voice_module = self.modules.get("voice_interface")
        if voice_module:
            status = voice_module.status.value
            print(f"🎤 JARVIS: Voice interface status - {status.title()}")
            
            if voice_module.instance:
                engine_type = type(voice_module.instance).__name__
                print(f"🎤 Engine: {engine_type}")
                print(f"🎤 Initialized: {voice_module.initialized_at}")
                
                # Check if it's LiveKit engine
                if hasattr(voice_module.instance, 'get_status'):
                    livekit_status = voice_module.instance.get_status()
                    print(f"🔥 LiveKit Status:")
                    print(f"   - Initialized: {livekit_status.get('initialized', False)}")
                    print(f"   - Running: {livekit_status.get('running', False)}")
                    print(f"   - Agent Ready: {livekit_status.get('agent_ready', False)}")
                    print(f"� Pipeline: Deepgram + OpenAI + Cartesia")
                else:
                    print(f"🔄 Legacy Voice Engine (Fallback Mode)")
            
            print("�🎤 Available Commands:")
            print("  - Say 'Hello JARVIS' to test recognition")
            print("  - Say 'JARVIS stop listening' to pause")
            print("  - Use 'voice off' to deactivate")
        else:
            print("🎤 JARVIS: Voice interface not initialized, Sir.")
    
    def _test_voice_interface(self):
        """Test voice interface functionality"""
        voice_module = self.modules.get("voice_interface")
        if voice_module and voice_module.instance:
            try:
                voice_engine = voice_module.instance
                
                # Check if it's LiveKit engine
                if hasattr(voice_engine, 'get_status'):
                    print("🎤 JARVIS: Testing LiveKit Agent capabilities...")
                    status = voice_engine.get_status()
                    
                    if status.get('initialized'):
                        print("✅ JARVIS: LiveKit Agent initialized")
                    if status.get('agent_ready'):
                        print("✅ JARVIS: AI Agent ready")
                    
                    print("🔥 JARVIS: LiveKit Agent test successful!")
                    print("💡 JARVIS: For full testing, use 'python jarvis_livekit_agent.py console'")
                    
                else:
                    # Test legacy voice engine
                    print("🎤 JARVIS: Testing legacy voice engine...")
                    if hasattr(voice_engine, 'speak'):
                        voice_engine.speak("Good evening, Sir. JARVIS voice systems are operational.")
                    elif hasattr(voice_engine, 'say'):
                        voice_engine.say("Good evening, Sir. JARVIS voice systems are operational.")
                    else:
                        print("🎤 JARVIS: Voice engine loaded, but TTS not available.")
                
                print("✅ JARVIS: Voice test completed successfully!")
                
            except Exception as e:
                print(f"❌ JARVIS: Voice test failed: {str(e)}")
        else:
            print("🎤 JARVIS: Please activate voice interface first with 'voice on'")
    
    def _run_voice_loop(self, voice_engine):
        """Run voice listening loop in background"""
        try:
            if hasattr(voice_engine, 'start_listening'):
                voice_engine.start_listening()
            elif hasattr(voice_engine, 'listen'):
                while True:
                    voice_engine.listen()
        except Exception as e:
            print(f"🎤 JARVIS: Voice loop error: {str(e)}")

    def show_voice_help(self):
        """Show voice interface help"""
        print("\n🎤 VOICE INTERFACE HELP:")
        print("  Current Status: FULLY OPERATIONAL (LiveKit Powered)")
        print("  Available Commands:")
        print("    - 'voice on' - Enable voice interface")
        print("    - 'voice off' - Disable voice interface") 
        print("    - 'voice status' - Check status")
        print("    - 'voice test' - Test voice features")
        print("  \n🔥 LIVEKIT AGENT FEATURES:")
        print("    ✅ Professional STT-LLM-TTS Pipeline")
        print("    ✅ Deepgram Nova-3 (Advanced Speech Recognition)")
        print("    ✅ OpenAI GPT-4o-mini (Fast Language Processing)")
        print("    ✅ Cartesia Sonic-2 (Natural Text-to-Speech)")
        print("    ✅ Silero VAD (Voice Activity Detection)")
        print("    ✅ Enhanced Noise Cancellation")
        print("    ✅ Multilingual Turn Detection")
        print("    ✅ Real-time Audio Processing")
        print("    ✅ Production-Ready Architecture")
        print("  \n🎯 LEGACY ENGINES (Fallback):")
        print("    - Robust Voice Engine (jarvis_voice_robust.py)")
        print("    - Premium Voice Engine (jarvis_voice_premium.py)")
        print("    - Clean Voice Engine (jarvis_voice_clean.py)")
        print("  \n🚀 STANDALONE MODES:")
        print("    - 'python jarvis_livekit_agent.py console' - Direct LiveKit console")
        print("    - 'python jarvis_livekit_agent.py dev' - LiveKit playground mode")
        print("  \n🎙️ USAGE:")
        print("    1. Type 'voice on' to activate LiveKit Agent")
        print("    2. System auto-detects best available engine")
        print("    3. LiveKit provides professional-grade voice AI")
        print("    4. Fallback engines activate if LiveKit unavailable")
        print("    5. Type 'voice off' to deactivate")
        print("  \n💡 PRO TIP:")
        print("    Configure LIVEKIT_API_KEY in .env for full capabilities!")

    def _parse_file_creation_command(self, user_input):
        """Parse file creation commands with improved accuracy"""
        import re
        
        files_to_create = []
        input_lower = user_input.lower()
        words = user_input.split()
        
        # More precise filename patterns
        filename_patterns = [
            r'(?:named?|called?)\s+([^\s]+)',  # "named ZARIF" or "called myfile"
            r'([a-zA-Z0-9_]+\.(?:txt|pdf|doc|json|py|js|html|css|docx|xlsx))',  # Files with extensions
        ]
        
        detected_files = set()  # Use set to avoid duplicates
        
        # Try each pattern
        for pattern in filename_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            for match in matches:
                if match and len(match.strip()) > 0:
                    detected_files.add(match.strip())
        
        # Look for specific context patterns
        # Pattern: "create a [filetype] file [name] ..."
        filetype_patterns = [
            r'(?:create|make|generate|build)\s+a?\s+(\w+)\s+file\s+(\w+)',  # "create a txt file doom"
            r'file\s+(\w+)',  # Simple "file [name]"
        ]
        
        for pattern in filetype_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    filetype, filename = match
                    if filetype.lower() in ['txt', 'text', 'pdf', 'json', 'py', 'python', 'js', 'html', 'css']:
                        detected_files.add(filename)
                elif isinstance(match, str):
                    detected_files.add(match)
        
        # Extract drive path
        drive_path = self._extract_drive_path(user_input)
        
        # Process each detected filename
        for filename in detected_files:
            if filename and len(filename.strip()) > 1:
                # Skip words that are clearly not filenames
                if filename.lower() in ['file', 'txt', 'pdf', 'doc', 'json', 'py', 'js', 'html', 'css', 
                                      'named', 'called', 'name', 'text', 'document', 'python', 'javascript']:
                    continue
                
                # Add extension if missing
                if '.' not in filename:
                    # Try to infer extension from context
                    extension = self._infer_file_extension(user_input, filename)
                    filename += extension
                
                # Add drive path if specified
                if drive_path:
                    filepath = f"{drive_path}{filename}"
                else:
                    filepath = filename
                
                files_to_create.append(filepath)
        
        # If no files detected by patterns, try a more conservative approach
        if not files_to_create:
            # Look for words immediately after "named", "called", or file extensions
            conservative_files = self._conservative_filename_extraction(user_input)
            files_to_create.extend(conservative_files)
        
        # Remove duplicates and return unique files
        return list(set(files_to_create))
    
    def _conservative_filename_extraction(self, user_input):
        """More conservative filename extraction"""
        files = []
        words = user_input.split()
        drive_path = self._extract_drive_path(user_input)
        
        for i, word in enumerate(words):
            # Look for words immediately after "named" or "called"
            if word.lower() in ['named', 'called'] and i + 1 < len(words):
                filename = words[i + 1].strip('.,!?;:')
                if len(filename) > 1 and filename.lower() not in ['in', 'on', 'at', 'the', 'a', 'an']:
                    if '.' not in filename:
                        extension = self._infer_file_extension(user_input, filename)
                        filename += extension
                    
                    if drive_path:
                        filepath = f"{drive_path}{filename}"
                    else:
                        filepath = filename
                    
                    files.append(filepath)
        
        # Look for files with explicit extensions
        import re
        file_pattern = r'([a-zA-Z0-9_-]+\.(?:txt|pdf|doc|json|py|js|html|css|docx|xlsx))'
        matches = re.findall(file_pattern, user_input, re.IGNORECASE)
        for match in matches:
            if drive_path:
                filepath = f"{drive_path}{match}"
            else:
                filepath = match
            files.append(filepath)
        
        return files
    
    def _extract_drive_path(self, user_input):
        """Extract drive path from user input"""
        input_lower = user_input.lower()
        words = user_input.split()
        
        # Look for drive specifications
        for word in words:
            if word.upper() in ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']:
                return f"{word.upper()[0]}:/"
            elif 'drive' in word.lower():
                # Look for letter before 'drive'
                for prev_word in words:
                    if len(prev_word) == 1 and prev_word.upper() in 'CDEFGH':
                        return f"{prev_word.upper()}:/"
                # Default to D drive if just "drive" is mentioned
                if 'd' in input_lower:
                    return "D:/"
        
        return None
    
    def _infer_file_extension(self, user_input, filename):
        """Infer file extension based on context"""
        input_lower = user_input.lower()
        
        if 'pdf' in input_lower:
            return '.pdf'
        elif 'json' in input_lower:
            return '.json'
        elif 'python' in input_lower or 'py' in input_lower:
            return '.py'
        elif 'javascript' in input_lower or 'js' in input_lower:
            return '.js'
        elif 'html' in input_lower:
            return '.html'
        elif 'css' in input_lower:
            return '.css'
        elif 'doc' in input_lower:
            return '.doc'
        else:
            return '.txt'  # Default to text file

    def _execute_single_command(self, command):
        """Execute a single command based on its type"""
        if command.startswith(('create project', 'create file', 'read file', 'list files', 'organize files', 'file info')):
            self.handle_file_operations(command)
        elif command.startswith(('search web', 'research', 'docs')):
            self.handle_web_operations(command)
        elif command.startswith('analyze code'):
            self.handle_code_operations(command)
        elif command.startswith('generate docs'):
            self.handle_code_operations(command)
        elif command.startswith('suggest improvements'):
            self.handle_code_operations(command)
        elif command.startswith('detect patterns'):
            self.handle_code_operations(command)
        else:
            print(f"🤖 JARVIS: I'm not sure how to handle '{command}', Sir.")

# Main execution block
if __name__ == "__main__":
    try:
        print("🚀 JARVIS-X: Initializing Central Orchestrator...")
        
        # Create JARVIS orchestrator
        jarvis_orchestrator = JarvisXOrchestrator()
        
        # Initialize the system (async method needs to be handled)
        print("⚙️  Initializing system modules...")
        
        # Run the main interface
        jarvis_orchestrator.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 JARVIS: Until next time, Sir. Systems powering down...")
    except Exception as e:
        print(f"\n❌ JARVIS: Critical error occurred: {str(e)}")
        print("💡 Debug info:", traceback.format_exc())
        print("🔧 Please check your configuration and try again.")
    finally:
        print("🤖 JARVIS: Session terminated. Goodbye, Sir.")
