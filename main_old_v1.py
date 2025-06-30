# main.py
# Entry point for Jarvis-X

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.ai_engine import JarvisAI

class JarvisXTerminal:
    def __init__(self):
        self.ai = JarvisAI()
        self.running = True
        
    def print_header(self):
        master_info = self.ai.get_master_identity()
        print("🤖" + "="*50)
        print("    JARVIS: Iron Man AI Assistant")
        print(f"    Serving: {master_info['name']} ({master_info['title']})")
        print("="*52)
        print(f"Current AI Model: {self.ai.get_current_model()}")
        print(f"Personality Mode: {self.ai.get_current_personality().title()}")
        auto_status = "ON" if self.ai.is_auto_personality_enabled() else "OFF"
        print(f"Auto Personality: {auto_status}")
        print("="*52)
        
        # Show JARVIS greeting
        greeting = self.ai.get_session_greeting()
        if greeting:
            print(f"\n🤖 JARVIS: {greeting}")
            print("🤖 JARVIS: How may I assist you today?")
        
    def print_commands(self):
        print("\n💬 Commands:")
        print("  - Type any message to chat with JARVIS")
        print("  - 'models' - Switch AI model")
        print("  - 'personality' - Change Jarvis personality mode")
        print("  - 'auto' - Toggle automatic personality switching")
        print("  - 'memory' - View conversation summary")
        print("  - 'insights' - Get conversation insights and patterns")
        print("  - 'search <query>' - Search conversation history")
        print("  - 'suggestions' - Get smart suggestions from JARVIS")
        print("  📁 FILE OPERATIONS:")
        print("  - 'create project <name> <type>' - Create new project")
        print("  - 'create file <path>' - Create a text file")
        print("  - 'read file <path>' - Read file contents")
        print("  - 'list files [path]' - List directory contents")
        print("  - 'organize files [path]' - Smart file organization")
        print("  - 'file info <path>' - Get detailed file information")
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
            print("🎤 Note: Voice integration is planned for Phase 4. Currently in development.")
        elif action == 'disable':
            print("🎤 JARVIS: Voice interface deactivation requested, Sir.")
        elif action == 'status':
            print("🎤 JARVIS: Voice interface status - Development Mode")
            print("🎤 Available: Text-to-speech capability")
            print("🎤 Planned: Full voice recognition and response")
        elif action == 'test':
            print("🎤 JARVIS: Testing voice capabilities, Sir...")
            print("🎤 Voice Test: 'Good evening, Sir. JARVIS voice systems operational.'")

    def show_voice_help(self):
        """Show voice interface help"""
        print("\n🎤 VOICE INTERFACE HELP:")
        print("  Current Status: Development Phase")
        print("  Available Commands:")
        print("    - 'voice on' - Enable voice interface")
        print("    - 'voice off' - Disable voice interface") 
        print("    - 'voice status' - Check status")
        print("    - 'voice test' - Test voice features")
        print("  Planned Features:")
        print("    - Full speech recognition")
        print("    - Natural voice responses")
        print("    - Personality-based voice adaptation")
        print("    - Voice-activated Beast Mode")

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

# Main execution block - This is what was missing!
if __name__ == "__main__":
    try:
        # Create and run JARVIS terminal interface
        jarvis_terminal = JarvisXTerminal()
        jarvis_terminal.run()
    except KeyboardInterrupt:
        print("\n\n👋 JARVIS: Until next time, Sir. Systems powering down...")
    except Exception as e:
        print(f"\n❌ JARVIS: Critical error occurred: {str(e)}")
        print("🔧 Please check your configuration and try again.")
    finally:
        print("🤖 JARVIS: Session terminated. Goodbye, Sir.")
