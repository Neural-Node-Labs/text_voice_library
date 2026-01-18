"""
Voice-Text Conversion Library
Component-Based Development Implementation
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import traceback

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

class DualLogger:
    """Dual-stream logging: system.log + llm_interaction.log"""
    
    def __init__(self):
        # System log for technical errors
        self.sys_logger = logging.getLogger('system')
        sys_handler = logging.FileHandler('system.log')
        sys_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.sys_logger.addHandler(sys_handler)
        self.sys_logger.setLevel(logging.INFO)
        
        # LLM interaction log for audit trail
        self.llm_logger = logging.getLogger('llm_interaction')
        llm_handler = logging.FileHandler('llm_interaction.log')
        llm_handler.setFormatter(logging.Formatter('%(message)s'))
        self.llm_logger.addHandler(llm_handler)
        self.llm_logger.setLevel(logging.INFO)
    
    def trace(self, component: str, event: str, data: Dict = None, duration_ms: float = 0):
        """Log trace point to LLM interaction log"""
        trace_record = {
            "trace_id": str(uuid.uuid4()),
            "component": component,
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data or {},
            "duration_ms": duration_ms
        }
        self.llm_logger.info(json.dumps(trace_record))
    
    def error(self, component: str, error: Exception, context: Dict = None):
        """Log error to system log"""
        self.sys_logger.error(
            f"Component: {component} | Error: {str(error)} | Context: {context}",
            exc_info=True
        )

logger = DualLogger()

# ============================================================================
# ERROR HANDLING
# ============================================================================

@dataclass
class ComponentError:
    """Standard error schema"""
    error_code: str
    component: str
    message: str
    timestamp: str
    stack_trace: str
    recovery_action: str
    context: Dict[str, Any]
    
    def to_dict(self):
        return asdict(self)

class VoiceTextException(Exception):
    """Base exception for library"""
    pass

# ============================================================================
# INPUT/OUTPUT SCHEMAS
# ============================================================================

@dataclass
class AudioData:
    """Standard audio data schema"""
    audio_bytes: bytes
    format: str
    sample_rate: int
    duration: float = 0.0
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

@dataclass
class TextData:
    """Standard text data schema"""
    text: str
    confidence: float = 1.0
    language: str = "en-US"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

# ============================================================================
# COMPONENT: AudioFileLoaderComponent
# ============================================================================

class AudioFileLoaderComponent:
    """
    COMPONENT CONTRACT:
    - Name: AudioFileLoaderComponent
    - Function: Load audio files with path validation
    - IN: {file_path: str, format: str}
    - OUT: {audio_data: bytes, format: str, sample_rate: int, duration: float}
    - ERROR: File not found, invalid format, permission denied
    """
    
    COMPONENT_NAME = "AudioFileLoaderComponent"
    SUPPORTED_FORMATS = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
    
    def __init__(self):
        self.logger = logger
    
    def load(self, file_path: str, expected_format: str = None) -> AudioData:
        """
        Load audio file with security checks
        
        IN Schema:
            file_path: str - Path to audio file
            expected_format: str - Expected audio format (optional)
        
        OUT Schema:
            AudioData object with audio_bytes, format, sample_rate, duration
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "FILE_LOAD_START", {"file_path": file_path})
        
        try:
            # Security: Path traversal prevention
            file_path = Path(file_path).resolve()
            
            # Validate file exists
            if not file_path.exists():
                raise VoiceTextException(f"File not found: {file_path}")
            
            # Validate format
            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                raise VoiceTextException(f"Unsupported format: {file_path.suffix}")
            
            # Read file
            with open(file_path, 'rb') as f:
                audio_bytes = f.read()
            
            # Get file metadata (simplified - would use pydub in real implementation)
            file_size = file_path.stat().st_size
            
            result = AudioData(
                audio_bytes=audio_bytes,
                format=file_path.suffix[1:],  # Remove dot
                sample_rate=44100,  # Default, would detect in real implementation
                duration=file_size / (44100 * 2 * 2)  # Rough estimate
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "FILE_LOAD_SUCCESS", {
                "file_size": file_size,
                "format": result.format
            }, duration_ms)
            
            return result
            
        except FileNotFoundError as e:
            self._handle_error("ERR_AUDIO_001", e, {"file_path": str(file_path)}, "ABORT")
            raise
        except PermissionError as e:
            self._handle_error("ERR_AUDIO_002", e, {"file_path": str(file_path)}, "ABORT")
            raise
        except Exception as e:
            self._handle_error("ERR_AUDIO_999", e, {"file_path": str(file_path)}, "RETRY")
            raise
    
    def _handle_error(self, error_code: str, error: Exception, context: Dict, recovery: str):
        """Centralized error handling"""
        error_obj = ComponentError(
            error_code=error_code,
            component=self.COMPONENT_NAME,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
            stack_trace=traceback.format_exc(),
            recovery_action=recovery,
            context=context
        )
        self.logger.error(self.COMPONENT_NAME, error, context)
        self.logger.trace(self.COMPONENT_NAME, "FILE_LOAD_ERROR", error_obj.to_dict())

# ============================================================================
# COMPONENT: TextNormalizerComponent
# ============================================================================

class TextNormalizerComponent:
    """
    COMPONENT CONTRACT:
    - Name: TextNormalizerComponent
    - Function: Clean and normalize text input/output
    - IN: {text: str, remove_punctuation: bool, lowercase: bool}
    - OUT: {normalized_text: str, original_length: int, final_length: int}
    - ERROR: Empty text, encoding errors
    """
    
    COMPONENT_NAME = "TextNormalizerComponent"
    
    def __init__(self):
        self.logger = logger
    
    def normalize(self, text: str, remove_punctuation: bool = False, 
                  lowercase: bool = False, strip_whitespace: bool = True) -> TextData:
        """
        Normalize text with configurable options
        
        IN Schema:
            text: str - Input text
            remove_punctuation: bool - Remove punctuation marks
            lowercase: bool - Convert to lowercase
            strip_whitespace: bool - Remove extra whitespace
        
        OUT Schema:
            TextData with normalized_text and metadata
        """
        trace_start = datetime.utcnow()
        original_length = len(text)
        
        self.logger.trace(self.COMPONENT_NAME, "NORMALIZE_START", {
            "original_length": original_length
        })
        
        try:
            # Input validation
            if not text or not text.strip():
                raise VoiceTextException("Empty or whitespace-only text")
            
            normalized = text
            
            # Strip whitespace
            if strip_whitespace:
                normalized = ' '.join(normalized.split())
            
            # Lowercase conversion
            if lowercase:
                normalized = normalized.lower()
            
            # Remove punctuation
            if remove_punctuation:
                import string
                normalized = normalized.translate(
                    str.maketrans('', '', string.punctuation)
                )
            
            result = TextData(
                text=normalized,
                confidence=1.0,
                metadata={
                    "original_length": original_length,
                    "final_length": len(normalized),
                    "operations": {
                        "lowercase": lowercase,
                        "remove_punctuation": remove_punctuation,
                        "strip_whitespace": strip_whitespace
                    }
                }
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "NORMALIZE_END", {
                "final_length": len(normalized),
                "reduction_pct": round((1 - len(normalized)/original_length) * 100, 2)
            }, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_TEXT_001", e, {"text_preview": text[:50]}, "RETRY")
            raise
    
    def _handle_error(self, error_code: str, error: Exception, context: Dict, recovery: str):
        error_obj = ComponentError(
            error_code=error_code,
            component=self.COMPONENT_NAME,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
            stack_trace=traceback.format_exc(),
            recovery_action=recovery,
            context=context
        )
        self.logger.error(self.COMPONENT_NAME, error, context)

# ============================================================================
# COMPONENT: AudioFileWriterComponent
# ============================================================================

class AudioFileWriterComponent:
    """
    COMPONENT CONTRACT:
    - Name: AudioFileWriterComponent
    - Function: Save audio data to file with path validation
    - IN: {audio_data: bytes, file_path: str, format: str}
    - OUT: {file_path: str, file_size: int, success: bool}
    - ERROR: Permission denied, disk full, invalid path
    """
    
    COMPONENT_NAME = "AudioFileWriterComponent"
    ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.flac', '.ogg'}
    
    def __init__(self, base_dir: str = "./audio_output"):
        self.logger = logger
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(exist_ok=True, parents=True)
    
    def write(self, audio_data: AudioData, file_path: str, 
              overwrite: bool = False) -> Dict[str, Any]:
        """
        Write audio to file with security checks
        
        IN Schema:
            audio_data: AudioData - Audio data object
            file_path: str - Target file path
            overwrite: bool - Allow overwriting existing files
        
        OUT Schema:
            {file_path: str, file_size: int, success: bool}
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "WRITE_START", {"file_path": file_path})
        
        try:
            # Security: Validate path is within base directory
            target_path = (self.base_dir / file_path).resolve()
            if not str(target_path).startswith(str(self.base_dir)):
                raise VoiceTextException("Path traversal attempt detected")
            
            # Validate extension
            if target_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                raise VoiceTextException(f"Invalid extension: {target_path.suffix}")
            
            # Check overwrite
            if target_path.exists() and not overwrite:
                raise VoiceTextException(f"File exists: {target_path}")
            
            # Write file
            target_path.parent.mkdir(exist_ok=True, parents=True)
            with open(target_path, 'wb') as f:
                f.write(audio_data.audio_bytes)
            
            file_size = target_path.stat().st_size
            
            result = {
                "file_path": str(target_path),
                "file_size": file_size,
                "success": True
            }
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "WRITE_SUCCESS", result, duration_ms)
            
            return result
            
        except PermissionError as e:
            self._handle_error("ERR_WRITE_001", e, {"file_path": file_path}, "ABORT")
            raise
        except OSError as e:
            self._handle_error("ERR_WRITE_002", e, {"file_path": file_path}, "RETRY")
            raise
        except Exception as e:
            self._handle_error("ERR_WRITE_999", e, {"file_path": file_path}, "ABORT")
            raise
    
    def _handle_error(self, error_code: str, error: Exception, context: Dict, recovery: str):
        error_obj = ComponentError(
            error_code=error_code,
            component=self.COMPONENT_NAME,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
            stack_trace=traceback.format_exc(),
            recovery_action=recovery,
            context=context
        )
        self.logger.error(self.COMPONENT_NAME, error, context)
        self.logger.trace(self.COMPONENT_NAME, "WRITE_FAILED", error_obj.to_dict())

# ============================================================================
# COMPONENT: SpeechRecognitionComponent (Mock Interface)
# ============================================================================

class SpeechRecognitionComponent:
    """
    COMPONENT CONTRACT:
    - Name: SpeechRecognitionComponent
    - Function: Convert audio to text using STT engines
    - IN: {audio_data: bytes, engine: str, language: str}
    - OUT: {text: str, confidence: float, engine_used: str}
    - ERROR: API errors, network issues, invalid audio
    
    NOTE: This is a mock interface. Real implementation would use:
    - speech_recognition library for Google/Sphinx
    - azure-cognitiveservices-speech for Azure
    - openai-whisper for Whisper
    """
    
    COMPONENT_NAME = "SpeechRecognitionComponent"
    SUPPORTED_ENGINES = {'google', 'azure', 'whisper', 'sphinx'}
    
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logger
        self.api_key = api_key
    
    def recognize(self, audio_data: AudioData, engine: str = 'google', 
                  language: str = 'en-US') -> TextData:
        """
        Convert speech to text
        
        IN Schema:
            audio_data: AudioData - Audio to transcribe
            engine: str - STT engine to use
            language: str - Language code
        
        OUT Schema:
            TextData with transcribed text and confidence
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "STT_REQUEST", {
            "engine": engine,
            "language": language,
            "audio_duration": audio_data.duration
        })
        
        try:
            if engine not in self.SUPPORTED_ENGINES:
                raise VoiceTextException(f"Unsupported engine: {engine}")
            
            # Mock transcription (real implementation would call actual API)
            transcribed_text = f"[MOCK TRANSCRIPTION from {engine}]"
            confidence = 0.95
            
            result = TextData(
                text=transcribed_text,
                confidence=confidence,
                language=language,
                metadata={"engine": engine}
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "STT_SUCCESS", {
                "text_length": len(transcribed_text),
                "confidence": confidence
            }, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_STT_001", e, {"engine": engine}, "RETRY")
            raise
    
    def _handle_error(self, error_code: str, error: Exception, context: Dict, recovery: str):
        error_obj = ComponentError(
            error_code=error_code,
            component=self.COMPONENT_NAME,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
            stack_trace=traceback.format_exc(),
            recovery_action=recovery,
            context=context
        )
        self.logger.error(self.COMPONENT_NAME, error, context)
        self.logger.trace(self.COMPONENT_NAME, "STT_FAILED", error_obj.to_dict())

# ============================================================================
# COMPONENT: TTSEngineComponent (Mock Interface)
# ============================================================================

class TTSEngineComponent:
    """
    COMPONENT CONTRACT:
    - Name: TTSEngineComponent
    - Function: Convert text to speech audio
    - IN: {text: str, engine: str, voice: str, speed: float}
    - OUT: {audio_data: bytes, format: str, duration: float}
    - ERROR: API errors, invalid voice, text too long
    
    NOTE: Mock interface. Real implementation uses gTTS, pyttsx3, Azure TTS
    """
    
    COMPONENT_NAME = "TTSEngineComponent"
    SUPPORTED_ENGINES = {'gtts', 'pyttsx3', 'azure', 'elevenlabs'}
    
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logger
        self.api_key = api_key
    
    def synthesize(self, text_data: TextData, engine: str = 'gtts',
                   voice: str = 'default', speed: float = 1.0) -> AudioData:
        """
        Convert text to speech
        
        IN Schema:
            text_data: TextData - Text to synthesize
            engine: str - TTS engine
            voice: str - Voice identifier
            speed: float - Speech rate multiplier
        
        OUT Schema:
            AudioData with synthesized speech
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "TTS_REQUEST", {
            "engine": engine,
            "text_length": len(text_data.text),
            "voice": voice,
            "speed": speed
        })
        
        try:
            if engine not in self.SUPPORTED_ENGINES:
                raise VoiceTextException(f"Unsupported engine: {engine}")
            
            if len(text_data.text) > 5000:
                raise VoiceTextException("Text exceeds maximum length")
            
            # Mock synthesis (real implementation calls TTS API)
            mock_audio = b"MOCK_AUDIO_DATA_" + text_data.text.encode()[:100]
            
            result = AudioData(
                audio_bytes=mock_audio,
                format='mp3',
                sample_rate=22050,
                duration=len(text_data.text) / (150 * speed)  # ~150 chars/sec
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "TTS_SUCCESS", {
                "audio_duration": result.duration,
                "audio_size": len(result.audio_bytes)
            }, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_TTS_001", e, {"engine": engine}, "RETRY")
            raise
    
    def _handle_error(self, error_code: str, error: Exception, context: Dict, recovery: str):
        error_obj = ComponentError(
            error_code=error_code,
            component=self.COMPONENT_NAME,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
            stack_trace=traceback.format_exc(),
            recovery_action=recovery,
            context=context
        )
        self.logger.error(self.COMPONENT_NAME, error, context)
        self.logger.trace(self.COMPONENT_NAME, "TTS_FAILED", error_obj.to_dict())

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example: Voice to Text pipeline
    print("=== Voice-to-Text Pipeline ===")
    
    # Load audio file
    loader = AudioFileLoaderComponent()
    try:
        audio = loader.load("sample_audio.wav")
        print(f"Loaded: {len(audio.audio_bytes)} bytes")
    except Exception as e:
        print(f"Load failed: {e}")
    
    # Recognize speech
    stt = SpeechRecognitionComponent()
    mock_audio = AudioData(b"sample", "wav", 16000, 3.5)
    text_result = stt.recognize(mock_audio, engine='google')
    print(f"Transcribed: {text_result.text}")
    
    # Normalize text
    normalizer = TextNormalizerComponent()
    normalized = normalizer.normalize(text_result.text, lowercase=True)
    print(f"Normalized: {normalized.text}")
    
    print("\n=== Text-to-Voice Pipeline ===")
    
    # Synthesize speech
    tts = TTSEngineComponent()
    input_text = TextData("Hello, this is a test of the TTS system!")
    audio_output = tts.synthesize(input_text, engine='gtts')
    print(f"Synthesized: {audio_output.duration:.2f}s audio")
    
    # Save to file
    writer = AudioFileWriterComponent()
    try:
        result = writer.write(audio_output, "output_speech.mp3", overwrite=True)
        print(f"Saved: {result['file_path']} ({result['file_size']} bytes)")
    except Exception as e:
        print(f"Save failed: {e}")
    
    print("\nCheck system.log and llm_interaction.log for detailed traces")
