#!/usr/bin/env python3
"""
Quick test of the main orchestrator with LiveKit
"""

try:
    from main import JarvisXOrchestrator
    
    print("🔬 Testing JARVIS-X Orchestrator with LiveKit...")
    
    # Create orchestrator
    orchestrator = JarvisXOrchestrator()
    
    # Test voice help
    print("\n1. Testing voice help:")
    orchestrator.show_voice_help()
    
    # Test voice activation
    print("\n2. Testing voice activation:")
    orchestrator.handle_voice_command('enable')
    
    # Test voice status
    print("\n3. Testing voice status:")
    orchestrator.handle_voice_command('status')
    
    print("\n✅ Orchestrator + LiveKit integration working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
