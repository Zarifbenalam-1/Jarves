# 🎥 IRON MAN VISION: JARVIS Video & Screen Integration

## COMPREHENSIVE PLAN FOR VISUAL CAPABILITIES

This document outlines the step-by-step implementation of visual capabilities for JARVIS using LiveKit's video, screen sharing, and data channel capabilities.

---

## 🔍 VISION ARCHITECTURE

### Core Components

1. **Video Engine** - Process webcam input and perform visual analysis
2. **Screen Engine** - Analyze displayed content and provide visual assistance
3. **Visual Memory** - Remember and recognize people, objects, and contexts
4. **AR Overlay** - Display information on top of video or screen content

### Data Flow

1. **Input Sources**
   - Webcam video (via LiveKit camera track)
   - Screen capture (via LiveKit screen share track)
   - Image uploads (via data channel)

2. **Processing Pipeline**
   - Frame extraction and buffering
   - Computer vision analysis (object/face detection)
   - Text extraction (OCR)
   - Visual context determination

3. **Integration Points**
   - Voice engine integration (multi-modal input)
   - AI engine integration (understanding visual context)
   - Response generation (including visual context)
   - Visual output (annotations, highlights, generated images)

---

## 🎥 VIDEO ENGINE IMPLEMENTATION

### Phase 1: Basic Camera Integration

```python
class JarvisVideoEngine:
    def __init__(self):
        self.video_source = rtc.VideoSource()
        self.local_video_track = None
        self.room = None
        self.video_enabled = False
        self.frame_processor = None
        self.recent_frames = []  # Last 30 frames buffer
    
    async def initialize(self, room):
        """Initialize video engine with LiveKit room"""
        self.room = room
        self.frame_processor = VideoFrameProcessor()
        
        # Setup event handlers
        self.setup_events()
        
    def setup_events(self):
        """Setup event handlers for video tracks"""
        @self.room.on("track_received")
        def on_track_received(track, publication, participant):
            if track.kind == rtc.TrackKind.KIND_VIDEO:
                print(f"📹 Video track received from {participant.identity}")
                asyncio.create_task(self.process_incoming_video(track))
    
    async def enable_camera(self):
        """Enable camera and publish video track"""
        try:
            # Create local video track
            self.local_video_track = rtc.LocalVideoTrack.create_video_track(
                "jarvis-camera", self.video_source
            )
            
            # Publish track
            if self.room and self.room.local_participant:
                await self.room.local_participant.publish_track(self.local_video_track)
                self.video_enabled = True
                print("📹 Camera enabled and publishing")
                return True
        except Exception as e:
            print(f"❌ Camera enable error: {e}")
            return False
    
    async def disable_camera(self):
        """Disable camera and stop publishing"""
        if self.local_video_track:
            await self.local_video_track.stop()
            self.video_enabled = False
            print("📷 Camera disabled")
    
    async def process_incoming_video(self, track):
        """Process incoming video frames"""
        try:
            video_stream = rtc.VideoStream(track)
            
            async for frame in video_stream:
                # Convert frame to numpy array for processing
                image = self.frame_to_numpy(frame)
                
                # Store in recent frames buffer
                self.recent_frames.append({
                    "timestamp": time.time(),
                    "frame": image
                })
                
                # Keep buffer at reasonable size
                while len(self.recent_frames) > 30:
                    self.recent_frames.pop(0)
                
                # Process frame if we have a processor
                if self.frame_processor:
                    result = await self.frame_processor.process(image)
                    
                    # Handle results (faces, objects, text, etc.)
                    if result:
                        await self.handle_analysis_result(result)
                    
        except Exception as e:
            print(f"❌ Video processing error: {e}")
    
    def frame_to_numpy(self, frame):
        """Convert LiveKit video frame to numpy array"""
        # Implementation depends on LiveKit frame format
        # Typically would convert YUV/RGB data to numpy
        # Placeholder implementation
        import numpy as np
        return np.array(frame.data)
    
    async def handle_analysis_result(self, result):
        """Handle video analysis results"""
        # Send data message with results
        if self.room and self.room.local_participant:
            await self.room.local_participant.publish_data(
                json.dumps({
                    "type": "video_analysis",
                    "faces": result.get("faces", []),
                    "objects": result.get("objects", []),
                    "text": result.get("text", ""),
                    "timestamp": time.time()
                }).encode()
            )
```

### Phase 2: Computer Vision Integration

```python
class VideoFrameProcessor:
    """Processes video frames for computer vision tasks"""
    
    def __init__(self):
        self.face_detector = self.load_face_detector()
        self.object_detector = self.load_object_detector()
        self.text_detector = self.load_text_detector()
        
        # Processing state
        self.processing_interval = 1.0  # Process every 1 second
        self.last_processed = {
            "face": 0,
            "object": 0,
            "text": 0
        }
        
    def load_face_detector(self):
        """Load face detection model"""
        try:
            import cv2
            return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            print("⚠️ OpenCV face detector not available")
            return None
            
    def load_object_detector(self):
        """Load object detection model"""
        try:
            # Placeholder - would use YOLOv5/v8, EfficientDet, etc.
            return None
        except:
            print("⚠️ Object detector not available")
            return None
            
    def load_text_detector(self):
        """Load text detection model (OCR)"""
        try:
            import pytesseract
            return pytesseract
        except:
            print("⚠️ Text detector (OCR) not available")
            return None
    
    async def process(self, frame):
        """Process a video frame with all detectors"""
        result = {}
        current_time = time.time()
        
        # Face detection (every 1 second)
        if current_time - self.last_processed["face"] >= self.processing_interval:
            result["faces"] = await self.detect_faces(frame)
            self.last_processed["face"] = current_time
        
        # Object detection (every 2 seconds)
        if current_time - self.last_processed["object"] >= self.processing_interval * 2:
            result["objects"] = await self.detect_objects(frame)
            self.last_processed["object"] = current_time
        
        # Text detection (every 3 seconds)
        if current_time - self.last_processed["text"] >= self.processing_interval * 3:
            result["text"] = await self.detect_text(frame)
            self.last_processed["text"] = current_time
            
        return result
    
    async def detect_faces(self, frame):
        """Detect faces in frame"""
        if not self.face_detector:
            return []
            
        try:
            # Convert frame to grayscale for face detection
            import cv2
            import numpy as np
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            # Convert to list of face details
            face_list = []
            for (x, y, w, h) in faces:
                face_list.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                })
                
            return face_list
        except Exception as e:
            print(f"Face detection error: {e}")
            return []
    
    async def detect_objects(self, frame):
        """Detect objects in frame"""
        if not self.object_detector:
            return []
            
        # In a real implementation, this would use a model like YOLO
        return []
    
    async def detect_text(self, frame):
        """Detect and OCR text in frame"""
        if not self.text_detector:
            return ""
            
        try:
            # Use pytesseract to extract text
            text = self.text_detector.image_to_string(frame)
            return text
        except Exception as e:
            print(f"Text detection error: {e}")
            return ""
```

---

## 🖥️ SCREEN ENGINE IMPLEMENTATION

### Phase 1: Screen Sharing Setup

```python
class JarvisScreenEngine:
    def __init__(self):
        self.screen_source = rtc.ScreenShareSource()
        self.local_screen_track = None
        self.room = None
        self.screen_enabled = False
        self.screen_processor = None
        self.recent_screens = []  # Last 10 screens
    
    async def initialize(self, room):
        """Initialize screen engine with LiveKit room"""
        self.room = room
        self.screen_processor = ScreenContentProcessor()
        
        # Setup event handlers
        self.setup_events()
    
    def setup_events(self):
        """Setup event handlers for screen tracks"""
        @self.room.on("track_received")
        def on_track_received(track, publication, participant):
            if track.kind == rtc.TrackKind.KIND_VIDEO and publication.name == "screen":
                print(f"🖥️ Screen share received from {participant.identity}")
                asyncio.create_task(self.process_screen_share(track))
    
    async def enable_screen_share(self):
        """Enable screen sharing"""
        try:
            # Create local screen share track
            self.local_screen_track = rtc.LocalVideoTrack.create_video_track(
                "jarvis-screen", self.screen_source
            )
            
            # Publish track
            if self.room and self.room.local_participant:
                await self.room.local_participant.publish_track(
                    self.local_screen_track, 
                    rtc.TrackPublishOptions(name="screen")
                )
                self.screen_enabled = True
                print("🖥️ Screen sharing enabled")
                return True
        except Exception as e:
            print(f"❌ Screen share error: {e}")
            return False
    
    async def disable_screen_share(self):
        """Disable screen sharing"""
        if self.local_screen_track:
            await self.local_screen_track.stop()
            self.screen_enabled = False
            print("🖥️ Screen sharing disabled")
    
    async def process_screen_share(self, track):
        """Process incoming screen share"""
        try:
            video_stream = rtc.VideoStream(track)
            
            async for frame in video_stream:
                # Convert frame to numpy array for processing
                screen_image = self.frame_to_numpy(frame)
                
                # Store in recent screens buffer
                self.recent_screens.append({
                    "timestamp": time.time(),
                    "screen": screen_image
                })
                
                # Keep buffer at reasonable size
                while len(self.recent_screens) > 10:
                    self.recent_screens.pop(0)
                
                # Process screen content
                if self.screen_processor:
                    result = await self.screen_processor.process(screen_image)
                    
                    # Handle results (app detection, code, text, etc.)
                    if result:
                        await self.handle_screen_analysis(result)
                    
        except Exception as e:
            print(f"❌ Screen processing error: {e}")
    
    def frame_to_numpy(self, frame):
        """Convert LiveKit video frame to numpy array"""
        # Implementation depends on LiveKit frame format
        # Similar to video frame conversion
        import numpy as np
        return np.array(frame.data)
    
    async def handle_screen_analysis(self, result):
        """Handle screen content analysis results"""
        # Send data message with results
        if self.room and self.room.local_participant:
            await self.room.local_participant.publish_data(
                json.dumps({
                    "type": "screen_analysis",
                    "app_context": result.get("app_context", "unknown"),
                    "text_content": result.get("text", ""),
                    "code_detected": result.get("is_code", False),
                    "code_language": result.get("code_language", ""),
                    "timestamp": time.time()
                }).encode()
            )
```

### Phase 2: Screen Content Analysis

```python
class ScreenContentProcessor:
    """Analyzes screen content to understand context"""
    
    def __init__(self):
        self.ocr_engine = None
        self.app_detector = AppContextDetector()
        self.code_detector = CodeDetector()
        
        try:
            import pytesseract
            self.ocr_engine = pytesseract
        except:
            print("⚠️ OCR engine not available")
    
    async def process(self, screen_image):
        """Process screen capture"""
        result = {}
        
        # Detect application context
        app_context = await self.app_detector.detect(screen_image)
        result["app_context"] = app_context
        
        # Extract text via OCR
        if self.ocr_engine:
            text = await self.extract_text(screen_image)
            result["text"] = text
            
            # If we have text, detect if it's code
            if text and len(text) > 10:
                code_result = await self.code_detector.analyze(text)
                result.update(code_result)
        
        return result
    
    async def extract_text(self, image):
        """Extract text from screen using OCR"""
        try:
            text = self.ocr_engine.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR error: {e}")
            return ""

class AppContextDetector:
    """Detects what application is currently being used"""
    
    def __init__(self):
        # Application signatures (visual patterns, colors, layouts)
        self.app_signatures = {
            "code_editor": {
                "keywords": ["def ", "class ", "function", "import ", "from ", 
                            "public class", "private ", "#include", "var ", "let ", "const "],
                "color_schemes": [(40, 44, 52), (30, 30, 30)]  # Dark backgrounds common in editors
            },
            "browser": {
                "keywords": ["http://", "https://", "www.", ".com", ".org", ".net"],
                "patterns": ["Search", "Bookmark", "New Tab"]
            },
            "document": {
                "keywords": ["Page ", "paragraph", "font", "style", "format"],
                "patterns": ["File", "Edit", "View", "Insert", "Tools"]
            },
            "terminal": {
                "keywords": ["$", "C:\\", "PS>", "bash", "cmd", "powershell", "terminal"],
                "color_schemes": [(0, 0, 0), (25, 25, 25), (46, 52, 64)]  # Dark backgrounds
            },
            "spreadsheet": {
                "keywords": ["=SUM(", "=AVERAGE(", "A1", "B2", "Sheet1"],
                "patterns": ["Cell", "Formula", "Chart"]
            }
        }
    
    async def detect(self, screen_image):
        """Detect application context from screen image"""
        # Placeholder implementation
        # In a real implementation, would use image analysis + OCR + heuristics
        return "unknown"

class CodeDetector:
    """Detects and analyzes code in text"""
    
    def __init__(self):
        # Programming language signatures
        self.lang_signatures = {
            "python": ["def ", "import ", "class ", "if __name__", "print(", "# "],
            "javascript": ["function ", "const ", "let ", "var ", "=> {", "// "],
            "java": ["public class", "private ", "void ", "String ", "@Override"],
            "csharp": ["namespace ", "using ", "public class", "private ", "void "],
            "cpp": ["#include", "int main", "void ", "std::", "cout <<"],
            "go": ["package ", "import ", "func ", "type ", "var "],
            "rust": ["fn ", "let ", "mut ", "struct ", "impl ", "use "]
        }
        
    async def analyze(self, text):
        """Analyze text to detect code and identify language"""
        result = {
            "is_code": False,
            "code_language": "",
            "code_structure": {}
        }
        
        # Check if text contains code
        lang_matches = {}
        total_lines = text.count('\n') + 1
        code_lines = 0
        
        # Count language signature matches
        for lang, signatures in self.lang_signatures.items():
            matches = 0
            for sig in signatures:
                matches += text.count(sig)
                if sig in text:
                    code_lines += 1
            
            if matches > 0:
                lang_matches[lang] = matches
        
        # If significant matches found, consider it code
        if lang_matches and max(lang_matches.values()) > 2:
            result["is_code"] = True
            result["code_language"] = max(lang_matches, key=lang_matches.get)
            
            # Extract basic code structure
            if result["code_language"] == "python":
                result["code_structure"] = self.analyze_python_structure(text)
            elif result["code_language"] in ["javascript", "typescript"]:
                result["code_structure"] = self.analyze_js_structure(text)
        
        return result
        
    def analyze_python_structure(self, text):
        """Analyze Python code structure"""
        structure = {
            "functions": [],
            "classes": [],
            "imports": []
        }
        
        import re
        
        # Find function definitions
        functions = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\(', text)
        structure["functions"] = functions
        
        # Find class definitions
        classes = re.findall(r'class\s+([a-zA-Z0-9_]+)', text)
        structure["classes"] = classes
        
        # Find imports
        imports = re.findall(r'import\s+([a-zA-Z0-9_\.]+)', text)
        imports += re.findall(r'from\s+([a-zA-Z0-9_\.]+)\s+import', text)
        structure["imports"] = imports
        
        return structure
    
    def analyze_js_structure(self, text):
        """Analyze JavaScript code structure"""
        structure = {
            "functions": [],
            "classes": [],
            "imports": []
        }
        
        import re
        
        # Find function definitions
        functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
        functions += re.findall(r'const\s+([a-zA-Z0-9_]+)\s*=\s*\([^\)]*\)\s*=>', text)
        structure["functions"] = functions
        
        # Find class definitions
        classes = re.findall(r'class\s+([a-zA-Z0-9_]+)', text)
        structure["classes"] = classes
        
        # Find imports
        imports = re.findall(r'import\s+.*from\s+[\'"]([^\'"]+)[\'"]', text)
        structure["imports"] = imports
        
        return structure
```

---

## 🧠 IRON MAN INTEGRATION

### Multi-modal Integration

```python
class JarvisMultiModalEngine:
    """Integrates voice, video, and screen for full JARVIS experience"""
    
    def __init__(self):
        self.voice_engine = None
        self.video_engine = None
        self.screen_engine = None
        self.ai = None
        self.room = None
        
        # Multi-modal context
        self.context = {
            "voice": {},
            "video": {},
            "screen": {},
            "web": {}
        }
        
    async def initialize(self):
        """Initialize all engines"""
        try:
            # Initialize AI
            from assistant.ai_engine import JarvisAI
            self.ai = JarvisAI()
            
            # Set up LiveKit room
            token = self.create_access_token()
            self.room = rtc.Room()
            await self.room.connect(os.getenv("LIVEKIT_URL"), token.to_jwt())
            
            # Initialize engines
            from enhanced_voice_engine import EnhancedVoiceEngine
            self.voice_engine = EnhancedVoiceEngine()
            self.voice_engine.room = self.room
            await self.voice_engine.initialize()
            
            self.video_engine = JarvisVideoEngine()
            await self.video_engine.initialize(self.room)
            
            self.screen_engine = JarvisScreenEngine()
            await self.screen_engine.initialize(self.room)
            
            # Setup combined data handlers
            self.setup_data_handlers()
            
            print("🧠 Multi-modal JARVIS initialized")
            return True
            
        except Exception as e:
            print(f"❌ Multi-modal initialization error: {e}")
            return False
    
    def create_access_token(self):
        """Create LiveKit access token"""
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")
        
        token = api.AccessToken(api_key, api_secret)
        token.with_identity("jarvis-multi-modal")
        token.with_name("JARVIS AI System")
        token.with_grants(api.VideoGrants(
            room_join=True,
            room="jarvis-room",
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True
        ))
        
        return token
    
    def setup_data_handlers(self):
        """Setup handlers for data messages"""
        @self.room.on("data_received")
        def on_data_received(data, participant):
            try:
                message = json.loads(data.decode())
                asyncio.create_task(self.process_data_message(message, participant))
            except Exception as e:
                print(f"❌ Data message error: {e}")
    
    async def process_data_message(self, message, participant):
        """Process data messages from all sources"""
        msg_type = message.get("type", "")
        
        # Update appropriate context
        if "voice" in msg_type:
            self.context["voice"].update(message)
        elif "video" in msg_type:
            self.context["video"].update(message)
        elif "screen" in msg_type:
            self.context["screen"].update(message)
        elif "web" in msg_type:
            self.context["web"].update(message)
            
        # Handle specific message types
        if msg_type == "voice_command":
            # Enhance command with visual context
            enhanced_command = await self.enhance_command_with_context(
                message.get("command", ""), 
                message.get("user", "unknown")
            )
            
            # Process enhanced command
            if self.voice_engine:
                await self.voice_engine.process_voice_command(enhanced_command)
    
    async def enhance_command_with_context(self, command, user_id):
        """Enhance voice command with visual context"""
        context_info = []
        
        # Add video context if available
        if self.context["video"].get("faces"):
            faces_count = len(self.context["video"].get("faces", []))
            if faces_count > 0:
                context_info.append(f"I can see {faces_count} {'person' if faces_count == 1 else 'people'}.")
        
        # Add screen context if available
        if self.context["screen"].get("app_context") != "unknown":
            app = self.context["screen"].get("app_context")
            context_info.append(f"You're using a {app}.")
            
            # If code is detected, add language
            if self.context["screen"].get("is_code", False):
                lang = self.context["screen"].get("code_language", "")
                if lang:
                    context_info.append(f"I can see {lang} code on your screen.")
        
        # Combine original command with context
        if context_info:
            enhanced = f"{command} [Context: {' '.join(context_info)}]"
            print(f"⚡ Enhanced command with context: {enhanced}")
            return enhanced
        
        return command
        
    async def enable_all(self):
        """Enable all JARVIS capabilities"""
        try:
            if self.voice_engine:
                await self.voice_engine.start_listening()
                
            if self.video_engine:
                await self.video_engine.enable_camera()
                
            print("✅ All JARVIS capabilities enabled")
            
        except Exception as e:
            print(f"❌ Error enabling capabilities: {e}")
    
    async def disable_all(self):
        """Disable all JARVIS capabilities"""
        try:
            if self.voice_engine:
                await self.voice_engine.stop_listening()
                
            if self.video_engine:
                await self.video_engine.disable_camera()
                
            if self.screen_engine:
                await self.screen_engine.disable_screen_share()
                
            print("🛑 All JARVIS capabilities disabled")
            
        except Exception as e:
            print(f"❌ Error disabling capabilities: {e}")
    
    async def cleanup(self):
        """Clean up all resources"""
        try:
            if self.voice_engine:
                await self.voice_engine.cleanup()
                
            if self.room:
                await self.room.disconnect()
                
            print("🧹 JARVIS multi-modal system cleaned up")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
```

---

## 🚀 IMPLEMENTATION ROADMAP

### Phase 1: Enhanced Voice (Days 1-2)
- ✓ Setup LiveKit voice integration
- ✓ Develop enhanced voice engine with emotion detection
- ✅ Test wake word detection and continuous conversation

### Phase 2: Basic Video (Days 3-4)
1. Setup LiveKit video track integration
2. Implement basic webcam access and publishing
3. Create frame processing pipeline
4. Add simple face detection

### Phase 3: Basic Screen Sharing (Days 5-6)
1. Implement screen capture via LiveKit
2. Create screen content analyzer
3. Add OCR for text extraction from screen
4. Develop app context detection

### Phase 4: Advanced Computer Vision (Days 7-9)
1. Integrate more sophisticated object detection
2. Add face recognition (not just detection)
3. Implement gesture recognition
4. Create visual memory system

### Phase 5: Visual UI Integration (Days 10-14)
1. Create visual overlay system
2. Implement screen annotation capabilities
3. Add visual feedback to voice responses
4. Build dashboard for JARVIS visual status

### Phase 6: Multi-modal Integration (Days 15-20)
1. Combine voice, video, and screen engines
2. Create unified context system
3. Enhance AI prompts with visual context
4. Build complete Iron Man JARVIS experience

---

## 📊 TESTING PLAN

### Individual Component Tests
1. **Video Engine Test**
   - Check camera access and publishing
   - Verify face detection works
   - Test object detection accuracy
   - Measure frame processing performance

2. **Screen Engine Test**
   - Verify screen capture works
   - Test OCR text extraction accuracy
   - Check app context detection
   - Evaluate code detection capability

### Integration Tests
1. **Voice + Video**
   - Test wake word with face present/absent
   - Check emotion detection accuracy
   - Verify multi-modal command enhancement

2. **Voice + Screen**
   - Test commands about screen content
   - Verify code-specific assistance
   - Check context-aware responses

3. **Full System**
   - Complete Iron Man experience test
   - Multi-user testing with video+voice
   - Performance under load testing

---

## 🔌 DEPENDENCY REQUIREMENTS

Additional dependencies for visual capabilities:

```
# Computer Vision
opencv-python>=4.8.0
pytesseract>=0.3.10
numpy>=1.24.0
pillow>=10.0.0

# Screen Capture
mss>=9.0.1

# Video Processing
av>=11.0.0  # PyAV for video frame handling

# Machine Learning
torch>=2.0.0  # For running ML models
torchvision>=0.15.0
```

---

This concludes the comprehensive plan for implementing visual capabilities for JARVIS using LiveKit. This implementation will transform JARVIS from a voice-only assistant into a true Iron Man experience with full visual awareness.
