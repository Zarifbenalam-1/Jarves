# console_test.py
# Console-based test for model selection (fallback for GUI)

# List of available models
AVAILABLE_MODELS = [
    "GPT-3.5 Turbo (OpenRouter)",
    "Mixtral 8x7B (OpenRouter)", 
    "Llama-3 (OpenRouter)",
    "Gemini (OpenRouter)",
    "Phi-3 Mini (Local)",
    "TinyLlama (Local)",
    "Llama-2 7B (Local)"
]

class JarvisXConsole:
    def __init__(self):
        self.selected_model = AVAILABLE_MODELS[0]
        print("🤖 Jarvis-X Console Test - AI Model Selector")
        print("=" * 50)
        
    def show_models(self):
        print("\nAvailable AI Models:")
        for i, model in enumerate(AVAILABLE_MODELS, 1):
            marker = " ✅" if model == self.selected_model else ""
            print(f"{i}. {model}{marker}")
            
    def select_model(self, choice):
        if 1 <= choice <= len(AVAILABLE_MODELS):
            self.selected_model = AVAILABLE_MODELS[choice - 1]
            print(f"\n🔄 Switched to: {self.selected_model}")
            return True
        else:
            print("❌ Invalid choice. Try again.")
            return False
            
    def run(self):
        while True:
            self.show_models()
            print(f"\nCurrent Model: {self.selected_model}")
            print("\nOptions:")
            print("1-7: Select a model")
            print("0: Exit")
            
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 0:
                    print("👋 Goodbye, boss!")
                    break
                else:
                    self.select_model(choice)
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye, boss!")
                break

if __name__ == "__main__":
    console = JarvisXConsole()
    console.run()
