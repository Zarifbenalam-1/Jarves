"""
JARVIS-X System Status Check
Test all core components: AI models, voice engine, file operations
"""

import os
import sys
import traceback

def test_ai_engine():
    """Test AI engine with different models"""
    print("🤖 Testing AI Engine...")
    
    try:
        sys.path.append('assistant')
        from assistant.ai_engine import JarvisAI
        
        ai = JarvisAI()
        print(f"✅ AI engine initialized")
        print(f"✅ Current model: {ai.get_current_model()}")
        print(f"✅ Available models: {len(ai.available_models)} models")
        
        # List your preferred models
        preferred_models = [
            "DeepSeek V3 (OpenRouter)",
            "DeepSeek Coder (OpenRouter)", 
            "Gemini Pro (OpenRouter)",
            "Claude 3 Haiku (OpenRouter)"
        ]
        
        print("\n🎯 Your preferred models:")
        for model in preferred_models:
            if model in ai.available_models:
                model_info = ai.available_models[model]
                print(f"  ✅ {model}")
                print(f"     Provider: {model_info['provider']}")
                print(f"     Price: {model_info.get('price', 'N/A')}")
                print(f"     Free tier: {model_info.get('free_tier', 'N/A')}")
            else:
                print(f"  ❌ {model} - Not found")
        
        # Test a simple query with OpenRouter (should work)
        print("\n🧪 Testing AI response...")
        test_response = ai.get_response("Hello JARVIS, just say 'AI system operational' briefly")
        print(f"✅ AI Response: {test_response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Engine Error: {e}")
        traceback.print_exc()
        return False

def test_voice_engine():
    """Test voice engine (basic import)"""
    print("\n🎙️ Testing Voice Engine...")
    
    try:
        import voice_engine
        print("✅ Voice engine imports successfully")
        
        # Check if LiveKit credentials are set
        livekit_url = os.getenv('LIVEKIT_URL')
        livekit_key = os.getenv('LIVEKIT_API_KEY')
        livekit_secret = os.getenv('LIVEKIT_API_SECRET')
        
        if livekit_url and livekit_key and livekit_secret:
            print("✅ LiveKit credentials configured")
            print(f"✅ LiveKit URL: {livekit_url}")
        else:
            print("⚠️ LiveKit credentials missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Voice Engine Error: {e}")
        return False

def test_file_operations():
    """Test file operations module"""
    print("\n📁 Testing File Operations...")
    
    try:
        from assistant.file_operations import get_file_operations_manager
        
        file_ops = get_file_operations_manager()
        print("✅ File operations module loaded")
        
        # Test creating a test file
        test_content = "JARVIS-X system test file"
        result = file_ops.create_file("test_jarvis_system.txt", test_content)
        
        if "successfully" in result.lower():
            print("✅ File creation test passed")
            
            # Clean up
            try:
                os.remove("test_jarvis_system.txt")
                print("✅ Test file cleaned up")
            except:
                pass
        else:
            print(f"⚠️ File creation test result: {result}")
            
        return True
        
    except Exception as e:
        print(f"❌ File Operations Error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🌍 Testing Environment Configuration...")
    
    env_vars = [
        ("OPENROUTER_API_KEY", "✅ Required for your preferred models"),
        ("LIVEKIT_URL", "✅ Required for voice features"),
        ("LIVEKIT_API_KEY", "✅ Required for voice features"),
        ("LIVEKIT_API_SECRET", "✅ Required for voice features"),
        ("GOOGLE_AI_API_KEY", "⚠️ Optional - for direct Google AI access"),
        ("DEEPSEEK_API_KEY", "⚠️ Optional - for direct DeepSeek access"),
    ]
    
    for var, desc in env_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✅ {var}: {masked_value} - {desc}")
        else:
            print(f"  ❌ {var}: Not set - {desc}")

def main():
    """Run all system tests"""
    print("🚀 JARVIS-X System Status Check")
    print("=" * 50)
    
    # Test environment first
    test_environment()
    
    # Test core components
    ai_ok = test_ai_engine()
    voice_ok = test_voice_engine()
    file_ok = test_file_operations()
    
    print("\n" + "=" * 50)
    print("📊 SYSTEM STATUS SUMMARY")
    print(f"🤖 AI Engine: {'✅ OPERATIONAL' if ai_ok else '❌ ISSUES'}")
    print(f"🎙️ Voice Engine: {'✅ READY' if voice_ok else '❌ ISSUES'}")
    print(f"📁 File Operations: {'✅ OPERATIONAL' if file_ok else '❌ ISSUES'}")
    
    if ai_ok and voice_ok and file_ok:
        print("\n🎉 ALL SYSTEMS READY! JARVIS-X is operational!")
        print("\n🎯 NEXT STEPS:")
        print("1. Get Google AI API key (free): https://aistudio.google.com/")
        print("2. Get DeepSeek API key (free): https://platform.deepseek.com/")
        print("3. Test voice interface: python voice_engine.py")
        print("4. Launch JARVIS: python main.py")
    else:
        print("\n⚠️ Some components need attention. Check errors above.")

if __name__ == "__main__":
    main()
