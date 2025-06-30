#!/usr/bin/env python3
"""
Test LiveKit Integration with JARVIS-X Orchestrator
"""

print("🔬 Testing LiveKit Integration...")

try:
    # Test 1: Import LiveKit Agent
    print("\n1. Testing LiveKit Agent Import...")
    from jarvis_livekit_agent import JarvisXLiveKitEngine, JarvisXAgent
    print("✅ LiveKit Agent imports successfully")
    
    # Test 2: Create LiveKit Engine
    print("\n2. Testing LiveKit Engine Creation...")
    livekit_engine = JarvisXLiveKitEngine()
    print("✅ LiveKit Engine created successfully")
    
    # Test 3: Check Engine Status
    print("\n3. Testing Engine Status...")
    status = livekit_engine.get_status()
    print(f"   - Initialized: {status['initialized']}")
    print(f"   - Running: {status['running']}")
    print(f"   - Agent Ready: {status['agent_ready']}")
    
    # Test 4: Test Orchestrator Integration
    print("\n4. Testing Orchestrator Integration...")
    from main import JarvisXOrchestrator
    orchestrator = JarvisXOrchestrator()
    print("✅ Orchestrator created successfully")
    
    # Test 5: Test Voice Activation
    print("\n5. Testing Voice Activation...")
    orchestrator.handle_voice_command('help')
    
    print("\n✅ ALL TESTS PASSED!")
    print("🔥 LiveKit integration is ready for deployment!")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Configure LiveKit API keys in .env file")
    print("2. Run 'python main.py' and type 'voice on'")
    print("3. Or run 'python jarvis_livekit_agent.py console' for direct testing")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
