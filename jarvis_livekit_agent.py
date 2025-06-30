#!/usr/bin/env python3
"""
JARVIS-X LIVEKIT AGENT
Professional-grade voice AI with LiveKit Agents

This is the new backbone of JARVIS-X, replacing basic voice engines
with enterprise-grade LiveKit infrastructure.

🎯 FEATURES:
- Professional STT-LLM-TTS pipeline
- Real-time voice processing
- Multiple AI provider support
- Enhanced noise cancellation
- Turn detection and VAD
- Multi-device ready
- Production scalable

🔧 INTEGRATES WITH:
- Main orchestrator (main.py)
- Existing AI engine
- File operations
- Web research capabilities
"""

import os
import asyncio
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv()

class JarvisXAgent(Agent):
    """
    JARVIS-X AI Agent for LiveKit
    Integrates with our existing AI engine and orchestrator
    """
    
    def __init__(self):
        # Enhanced JARVIS personality and instructions
        instructions = """
        You are JARVIS-X, an advanced AI assistant inspired by Tony Stark's JARVIS.
        
        PERSONALITY:
        - Professional yet witty, like a sophisticated butler
        - Highly intelligent and analytical
        - Proactive and anticipatory
        - Respectful but not overly formal
        - Always ready to assist with complex tasks
        
        CAPABILITIES:
        - Advanced voice conversation
        - File operations and project management
        - Web research and analysis
        - Code analysis and assistance
        - Real-time system monitoring
        
        STYLE:
        - Address the user as "Sir" when appropriate
        - Provide detailed, actionable responses
        - Offer proactive suggestions
        - Be concise yet comprehensive
        - Maintain Iron Man-level sophistication
        """
        
        super().__init__(instructions=instructions)

class JarvisXLiveKitEngine:
    """
    LiveKit Engine for JARVIS-X
    Manages the LiveKit agent session and integration
    """
    
    def __init__(self):
        self.session = None
        self.agent = None
        self.is_running = False
        
    async def initialize(self):
        """Initialize the LiveKit agent session"""
        try:
            print("🚀 JARVIS-X: Initializing LiveKit Agent...")
            
            # Create agent session with professional pipeline
            self.session = AgentSession(
                # Speech-to-Text (Deepgram Nova-3 - latest model)
                stt=deepgram.STT(
                    model="nova-3", 
                    language="multi"  # Multi-language support
                ),
                
                # Large Language Model (OpenAI GPT-4o-mini - fast and capable)
                llm=openai.LLM(
                    model="gpt-4o-mini",
                    temperature=0.7  # Balanced creativity
                ),
                
                # Text-to-Speech (Cartesia Sonic-2 - natural voice)
                tts=cartesia.TTS(
                    model="sonic-2",
                    voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"  # Professional voice
                ),
                
                # Voice Activity Detection (Silero - local processing)
                vad=silero.VAD.load(),
                
                # Turn Detection (Multilingual - advanced conversation flow)
                turn_detection=MultilingualModel(),
            )
            
            # Create JARVIS-X agent
            self.agent = JarvisXAgent()
            
            print("✅ JARVIS-X: LiveKit Agent initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ JARVIS-X: LiveKit initialization failed: {str(e)}")
            return False
    
    async def start_session(self, room):
        """Start the LiveKit agent session in a room"""
        try:
            if not self.session or not self.agent:
                await self.initialize()
            
            print("🎤 JARVIS-X: Starting voice session...")
            
            # Start the agent session with enhanced options
            await self.session.start(
                room=room,
                agent=self.agent,
                room_input_options=RoomInputOptions(
                    # Enhanced noise cancellation for clear audio
                    noise_cancellation=noise_cancellation.BVC(),
                ),
            )
            
            # Generate initial greeting
            await self.session.generate_reply(
                instructions="Greet the user professionally as JARVIS-X and offer assistance."
            )
            
            self.is_running = True
            print("✅ JARVIS-X: Voice session active!")
            
        except Exception as e:
            print(f"❌ JARVIS-X: Session start failed: {str(e)}")
            raise
    
    async def stop_session(self):
        """Stop the LiveKit agent session"""
        try:
            if self.session:
                await self.session.stop()
                self.is_running = False
                print("🔇 JARVIS-X: Voice session stopped")
        except Exception as e:
            print(f"❌ JARVIS-X: Session stop failed: {str(e)}")
    
    def get_status(self):
        """Get current session status"""
        return {
            "initialized": self.session is not None,
            "running": self.is_running,
            "agent_ready": self.agent is not None
        }

# Entry point for LiveKit agent (when run standalone)
async def entrypoint(ctx: agents.JobContext):
    """
    LiveKit agent entrypoint
    This runs when JARVIS-X is deployed as a LiveKit agent
    """
    # Create and initialize the JARVIS-X engine
    jarvis_engine = JarvisXLiveKitEngine()
    await jarvis_engine.initialize()
    
    # Start the session in the provided room
    await jarvis_engine.start_session(ctx.room)
    
    # Connect to LiveKit
    await ctx.connect()
    
    print("🤖 JARVIS-X LiveKit Agent is operational!")

# CLI support for standalone operation
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
