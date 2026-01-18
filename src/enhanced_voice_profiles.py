"""
Enhanced Voice Profile & Sound Customization System
Component-Based Development - Voice Transformation Extension
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from enum import Enum
import traceback

# Import base components
try:
    from voice_text_lib import (
        AudioData, TextData, VoiceTextException, 
        ComponentError, logger, DualLogger
    )
except ImportError:
    # Fallback definitions for standalone testing
    class AudioData:
        def __init__(self, audio_bytes, format, sample_rate, duration=0.0, timestamp=""):
            self.audio_bytes = audio_bytes
            self.format = format
            self.sample_rate = sample_rate
            self.duration = duration
            self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    class TextData:
        def __init__(self, text, confidence=1.0, language="en-US", metadata=None):
            self.text = text
            self.confidence = confidence
            self.language = language
            self.metadata = metadata or {}
    
    class VoiceTextException(Exception):
        pass
    
    class DualLogger:
        def trace(self, component, event, data=None, duration_ms=0): pass
        def error(self, component, error, context=None): pass
    
    logger = DualLogger()

# ============================================================================
# ENUMERATIONS
# ============================================================================

class Gender(Enum):
    """Voice gender options"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"
    CUSTOM = "custom"

class Emotion(Enum):
    """Emotional tones for speech"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"
    CALM = "calm"
    FEARFUL = "fearful"
    CONFIDENT = "confident"

class AudioEffect(Enum):
    """Available audio effects"""
    REVERB = "reverb"
    ECHO = "echo"
    CHORUS = "chorus"
    DISTORTION = "distortion"
    EQUALIZER = "equalizer"
    COMPRESSOR = "compressor"
    NOISE_GATE = "noise_gate"
    PITCH_SHIFT = "pitch_shift"
    TIME_STRETCH = "time_stretch"

# ============================================================================
# DATA SCHEMAS
# ============================================================================

@dataclass
class VoiceProfile:
    """
    Complete voice profile specification
    
    Schema:
        profile_id: Unique identifier
        name: Human-readable name
        gender: Voice gender
        pitch: Pitch adjustment (-12 to +12 semitones)
        speed: Speech rate (0.5 to 2.0)
        volume: Volume level (0.0 to 2.0)
        timbre: Voice quality characteristics
        language: Primary language
        accent: Regional accent
        age_range: Approximate age (child, young, adult, elderly)
        emotion_default: Default emotional tone
        custom_params: Engine-specific parameters
    """
    profile_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Default Voice"
    gender: str = Gender.NEUTRAL.value
    pitch: float = 0.0  # -12 to +12 semitones
    speed: float = 1.0  # 0.5 to 2.0
    volume: float = 1.0  # 0.0 to 2.0
    timbre: Dict[str, float] = field(default_factory=dict)
    language: str = "en-US"
    accent: str = "neutral"
    age_range: str = "adult"
    emotion_default: str = Emotion.NEUTRAL.value
    custom_params: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def validate(self) -> Dict[str, Any]:
        """Validate profile parameters"""
        errors = []
        
        if not -12 <= self.pitch <= 12:
            errors.append("Pitch must be between -12 and +12 semitones")
        
        if not 0.5 <= self.speed <= 2.0:
            errors.append("Speed must be between 0.5 and 2.0")
        
        if not 0.0 <= self.volume <= 2.0:
            errors.append("Volume must be between 0.0 and 2.0")
        
        if self.gender not in [g.value for g in Gender]:
            errors.append(f"Invalid gender: {self.gender}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        return cls(**data)

@dataclass
class EffectConfig:
    """Configuration for audio effect"""
    effect_type: str
    intensity: float = 0.5  # 0.0 to 1.0
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate effect configuration"""
        if self.effect_type not in [e.value for e in AudioEffect]:
            return False
        if not 0.0 <= self.intensity <= 1.0:
            return False
        return True

@dataclass
class VoiceTransform:
    """Voice transformation specification"""
    pitch_shift: float = 0.0  # Semitones
    formant_shift: float = 0.0  # Formant frequency ratio
    timbre_morph: float = 0.0  # Timbre transformation (-1 to +1)
    breathiness: float = 0.0  # Add breath noise (0 to 1)
    roughness: float = 0.0  # Add vocal roughness (0 to 1)

# ============================================================================
# COMPONENT: VoiceProfileComponent
# ============================================================================

class VoiceProfileComponent:
    """
    COMPONENT CONTRACT:
    - Name: VoiceProfileComponent
    - Function: Create, manage, and validate voice profiles
    - IN: {profile_id: str, parameters: dict}
    - OUT: {profile: VoiceProfile, validation: dict}
    - ERROR: Invalid parameters, profile not found
    """
    
    COMPONENT_NAME = "VoiceProfileComponent"
    
    # Predefined voice profiles
    PRESET_PROFILES = {
        "professional_male": VoiceProfile(
            name="Professional Male",
            gender=Gender.MALE.value,
            pitch=-2.0,
            speed=0.95,
            volume=1.0,
            accent="american",
            age_range="adult"
        ),
        "professional_female": VoiceProfile(
            name="Professional Female",
            gender=Gender.FEMALE.value,
            pitch=2.0,
            speed=1.0,
            volume=1.0,
            accent="american",
            age_range="adult"
        ),
        "friendly_assistant": VoiceProfile(
            name="Friendly Assistant",
            gender=Gender.NEUTRAL.value,
            pitch=1.0,
            speed=1.1,
            volume=1.0,
            emotion_default=Emotion.HAPPY.value,
            age_range="young"
        ),
        "narrator_deep": VoiceProfile(
            name="Deep Narrator",
            gender=Gender.MALE.value,
            pitch=-4.0,
            speed=0.85,
            volume=1.1,
            accent="british",
            age_range="adult"
        ),
        "child_voice": VoiceProfile(
            name="Child Voice",
            gender=Gender.NEUTRAL.value,
            pitch=6.0,
            speed=1.2,
            volume=0.9,
            age_range="child"
        ),
        "elderly_wise": VoiceProfile(
            name="Elderly Wise",
            gender=Gender.MALE.value,
            pitch=-1.0,
            speed=0.8,
            volume=0.95,
            age_range="elderly",
            custom_params={"tremolo": 0.3}
        )
    }
    
    def __init__(self):
        self.logger = logger
        self.profiles_cache: Dict[str, VoiceProfile] = {}
    
    def create_profile(self, name: str, **parameters) -> VoiceProfile:
        """
        Create new voice profile
        
        IN Schema:
            name: str - Profile name
            **parameters: Voice parameters (pitch, speed, gender, etc.)
        
        OUT Schema:
            VoiceProfile object
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "PROFILE_CREATE", {"name": name})
        
        try:
            # Create profile
            profile = VoiceProfile(name=name, **parameters)
            
            # Validate
            validation = profile.validate()
            if not validation["valid"]:
                raise VoiceTextException(f"Invalid profile: {validation['errors']}")
            
            # Cache
            self.profiles_cache[profile.profile_id] = profile
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "PROFILE_CREATE_SUCCESS", {
                "profile_id": profile.profile_id,
                "name": name
            }, duration_ms)
            
            return profile
            
        except Exception as e:
            self._handle_error("ERR_PROFILE_001", e, {"name": name}, "RETRY")
            raise
    
    def load_preset(self, preset_name: str) -> VoiceProfile:
        """
        Load predefined voice profile
        
        IN Schema:
            preset_name: str - Name of preset profile
        
        OUT Schema:
            VoiceProfile object
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "PROFILE_LOAD_PRESET", {"preset": preset_name})
        
        try:
            if preset_name not in self.PRESET_PROFILES:
                raise VoiceTextException(f"Preset not found: {preset_name}")
            
            # Clone preset
            preset = self.PRESET_PROFILES[preset_name]
            profile = VoiceProfile(**asdict(preset))
            profile.profile_id = str(uuid.uuid4())
            
            # Cache
            self.profiles_cache[profile.profile_id] = profile
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "PROFILE_LOAD_SUCCESS", {
                "preset": preset_name,
                "profile_id": profile.profile_id
            }, duration_ms)
            
            return profile
            
        except Exception as e:
            self._handle_error("ERR_PROFILE_002", e, {"preset": preset_name}, "ABORT")
            raise
    
    def update_profile(self, profile_id: str, **updates) -> VoiceProfile:
        """
        Update existing profile parameters
        
        IN Schema:
            profile_id: str - Profile ID
            **updates: Parameters to update
        
        OUT Schema:
            Updated VoiceProfile
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "PROFILE_UPDATE", {
            "profile_id": profile_id,
            "updates": list(updates.keys())
        })
        
        try:
            if profile_id not in self.profiles_cache:
                raise VoiceTextException(f"Profile not found: {profile_id}")
            
            profile = self.profiles_cache[profile_id]
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            profile.updated_at = datetime.utcnow().isoformat()
            
            # Validate
            validation = profile.validate()
            if not validation["valid"]:
                raise VoiceTextException(f"Invalid update: {validation['errors']}")
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "PROFILE_UPDATE_SUCCESS", {
                "profile_id": profile_id
            }, duration_ms)
            
            return profile
            
        except Exception as e:
            self._handle_error("ERR_PROFILE_003", e, {"profile_id": profile_id}, "RETRY")
            raise
    
    def list_presets(self) -> List[str]:
        """Get list of available preset profiles"""
        return list(self.PRESET_PROFILES.keys())
    
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
# COMPONENT: AudioEffectsComponent
# ============================================================================

class AudioEffectsComponent:
    """
    COMPONENT CONTRACT:
    - Name: AudioEffectsComponent
    - Function: Apply audio effects (reverb, echo, EQ, etc.)
    - IN: {audio: AudioData, effects: list[EffectConfig]}
    - OUT: {processed_audio: AudioData, effects_applied: list}
    - ERROR: Invalid effect type, processing failure
    """
    
    COMPONENT_NAME = "AudioEffectsComponent"
    
    def __init__(self):
        self.logger = logger
    
    def apply_effects(self, audio: AudioData, effects: List[EffectConfig]) -> AudioData:
        """
        Apply chain of audio effects
        
        IN Schema:
            audio: AudioData - Input audio
            effects: list[EffectConfig] - Effects to apply
        
        OUT Schema:
            AudioData with effects applied
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "EFFECT_START", {
            "num_effects": len(effects),
            "effect_types": [e.effect_type for e in effects]
        })
        
        try:
            # Validate effects
            for effect in effects:
                if not effect.validate():
                    raise VoiceTextException(f"Invalid effect: {effect.effect_type}")
            
            # Process audio (mock implementation)
            processed_bytes = audio.audio_bytes
            effects_applied = []
            
            for effect in effects:
                # Apply effect (in real implementation, would use DSP library)
                processed_bytes = self._apply_single_effect(
                    processed_bytes,
                    effect
                )
                effects_applied.append(effect.effect_type)
            
            result = AudioData(
                audio_bytes=processed_bytes,
                format=audio.format,
                sample_rate=audio.sample_rate,
                duration=audio.duration
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "EFFECT_APPLIED", {
                "effects": effects_applied
            }, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_EFFECT_001", e, {
                "num_effects": len(effects)
            }, "RETRY")
            raise
    
    def _apply_single_effect(self, audio_bytes: bytes, effect: EffectConfig) -> bytes:
        """
        Apply single effect (mock implementation)
        
        Real implementation would use:
        - pydub for basic effects
        - pedalboard for advanced effects
        - librosa for analysis-based effects
        """
        # Mock effect application
        effect_marker = f"[{effect.effect_type}:{effect.intensity}]".encode()
        return effect_marker + audio_bytes
    
    def create_reverb(self, room_size: float = 0.5, damping: float = 0.5) -> EffectConfig:
        """Create reverb effect configuration"""
        return EffectConfig(
            effect_type=AudioEffect.REVERB.value,
            intensity=room_size,
            parameters={"damping": damping}
        )
    
    def create_echo(self, delay_ms: float = 500, feedback: float = 0.3) -> EffectConfig:
        """Create echo effect configuration"""
        return EffectConfig(
            effect_type=AudioEffect.ECHO.value,
            intensity=feedback,
            parameters={"delay_ms": delay_ms}
        )
    
    def create_equalizer(self, bass: float = 0, mid: float = 0, treble: float = 0) -> EffectConfig:
        """Create equalizer effect configuration"""
        return EffectConfig(
            effect_type=AudioEffect.EQUALIZER.value,
            intensity=0.5,
            parameters={
                "bass": bass,  # -12 to +12 dB
                "mid": mid,
                "treble": treble
            }
        )
    
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
# COMPONENT: VoiceTransformComponent
# ============================================================================

class VoiceTransformComponent:
    """
    COMPONENT CONTRACT:
    - Name: VoiceTransformComponent
    - Function: Transform voice characteristics (pitch, formant, timbre)
    - IN: {audio: AudioData, transform: VoiceTransform}
    - OUT: {transformed_audio: AudioData}
    - ERROR: Invalid transform parameters, processing failure
    """
    
    COMPONENT_NAME = "VoiceTransformComponent"
    
    def __init__(self):
        self.logger = logger
    
    def transform_voice(self, audio: AudioData, transform: VoiceTransform) -> AudioData:
        """
        Transform voice characteristics
        
        IN Schema:
            audio: AudioData - Input audio
            transform: VoiceTransform - Transformation parameters
        
        OUT Schema:
            AudioData with transformed voice
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "TRANSFORM_START", {
            "pitch_shift": transform.pitch_shift,
            "formant_shift": transform.formant_shift
        })
        
        try:
            # Apply transformations (mock implementation)
            # Real implementation would use:
            # - librosa for pitch shifting
            # - praat-parselmouth for formant manipulation
            # - world vocoder for advanced voice transformation
            
            transformed_bytes = audio.audio_bytes
            
            # Pitch shift
            if transform.pitch_shift != 0:
                transformed_bytes = self._pitch_shift(
                    transformed_bytes,
                    transform.pitch_shift
                )
            
            # Formant shift
            if transform.formant_shift != 0:
                transformed_bytes = self._formant_shift(
                    transformed_bytes,
                    transform.formant_shift
                )
            
            # Timbre morph
            if transform.timbre_morph != 0:
                transformed_bytes = self._timbre_morph(
                    transformed_bytes,
                    transform.timbre_morph
                )
            
            result = AudioData(
                audio_bytes=transformed_bytes,
                format=audio.format,
                sample_rate=audio.sample_rate,
                duration=audio.duration
            )
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "TRANSFORM_END", {
                "transformations_applied": [
                    k for k, v in asdict(transform).items() if v != 0
                ]
            }, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_TRANSFORM_001", e, {
                "transform": asdict(transform)
            }, "RETRY")
            raise
    
    def _pitch_shift(self, audio_bytes: bytes, semitones: float) -> bytes:
        """Shift pitch by semitones (mock)"""
        marker = f"[PITCH:{semitones:+.1f}]".encode()
        return marker + audio_bytes
    
    def _formant_shift(self, audio_bytes: bytes, ratio: float) -> bytes:
        """Shift formant frequencies (mock)"""
        marker = f"[FORMANT:{ratio:+.2f}]".encode()
        return marker + audio_bytes
    
    def _timbre_morph(self, audio_bytes: bytes, amount: float) -> bytes:
        """Morph timbre characteristics (mock)"""
        marker = f"[TIMBRE:{amount:+.2f}]".encode()
        return marker + audio_bytes
    
    def male_to_female(self) -> VoiceTransform:
        """Preset: Transform male voice to female"""
        return VoiceTransform(
            pitch_shift=4.0,
            formant_shift=1.15,
            timbre_morph=0.5
        )
    
    def female_to_male(self) -> VoiceTransform:
        """Preset: Transform female voice to male"""
        return VoiceTransform(
            pitch_shift=-4.0,
            formant_shift=0.85,
            timbre_morph=-0.5
        )
    
    def robot_voice(self) -> VoiceTransform:
        """Preset: Create robot voice effect"""
        return VoiceTransform(
            pitch_shift=0.0,
            formant_shift=1.0,
            timbre_morph=-1.0,
            roughness=0.8
        )
    
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
# COMPONENT: EmotionEngineComponent
# ============================================================================

class EmotionEngineComponent:
    """
    COMPONENT CONTRACT:
    - Name: EmotionEngineComponent
    - Function: Add emotional tone to synthesized speech
    - IN: {text: str, emotion: str, intensity: float}
    - OUT: {emotional_params: dict, prosody_changes: dict}
    - ERROR: Invalid emotion type, intensity out of range
    """
    
    COMPONENT_NAME = "EmotionEngineComponent"
    
    # Emotion-to-prosody mapping
    EMOTION_PROFILES = {
        Emotion.HAPPY.value: {
            "pitch_modifier": +2.0,
            "speed_modifier": 1.1,
            "volume_modifier": 1.05,
            "pitch_variance": 1.3
        },
        Emotion.SAD.value: {
            "pitch_modifier": -1.5,
            "speed_modifier": 0.85,
            "volume_modifier": 0.9,
            "pitch_variance": 0.7
        },
        Emotion.ANGRY.value: {
            "pitch_modifier": +1.0,
            "speed_modifier": 1.2,
            "volume_modifier": 1.2,
            "pitch_variance": 1.5
        },
        Emotion.EXCITED.value: {
            "pitch_modifier": +3.0,
            "speed_modifier": 1.3,
            "volume_modifier": 1.1,
            "pitch_variance": 1.6
        },
        Emotion.CALM.value: {
            "pitch_modifier": 0.0,
            "speed_modifier": 0.9,
            "volume_modifier": 0.95,
            "pitch_variance": 0.5
        },
        Emotion.FEARFUL.value: {
            "pitch_modifier": +2.5,
            "speed_modifier": 1.15,
            "volume_modifier": 0.85,
            "pitch_variance": 1.4
        },
        Emotion.CONFIDENT.value: {
            "pitch_modifier": -0.5,
            "speed_modifier": 0.95,
            "volume_modifier": 1.1,
            "pitch_variance": 0.8
        }
    }
    
    def __init__(self):
        self.logger = logger
    
    def apply_emotion(self, emotion: str, intensity: float = 1.0,
                     base_profile: Optional[VoiceProfile] = None) -> Dict[str, Any]:
        """
        Calculate emotional prosody modifications
        
        IN Schema:
            emotion: str - Emotion type (from Emotion enum)
            intensity: float - Emotion intensity (0.0 to 1.0)
            base_profile: VoiceProfile - Base profile to modify (optional)
        
        OUT Schema:
            Dictionary with prosody modifications
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "EMOTION_APPLY", {
            "emotion": emotion,
            "intensity": intensity
        })
        
        try:
            # Validate
            if emotion not in [e.value for e in Emotion]:
                raise VoiceTextException(f"Invalid emotion: {emotion}")
            
            if not 0.0 <= intensity <= 1.0:
                raise VoiceTextException(f"Intensity must be 0.0-1.0: {intensity}")
            
            # Get emotion profile
            emotion_profile = self.EMOTION_PROFILES[emotion]
            
            # Scale by intensity
            modifications = {
                "pitch_shift": emotion_profile["pitch_modifier"] * intensity,
                "speed_multiplier": 1.0 + (emotion_profile["speed_modifier"] - 1.0) * intensity,
                "volume_multiplier": 1.0 + (emotion_profile["volume_modifier"] - 1.0) * intensity,
                "pitch_variance": 1.0 + (emotion_profile["pitch_variance"] - 1.0) * intensity,
                "emotion": emotion,
                "intensity": intensity
            }
            
            # Apply to base profile if provided
            if base_profile:
                modifications["final_pitch"] = base_profile.pitch + modifications["pitch_shift"]
                modifications["final_speed"] = base_profile.speed * modifications["speed_multiplier"]
                modifications["final_volume"] = base_profile.volume * modifications["volume_multiplier"]
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "EMOTION_SUCCESS", {
                "emotion": emotion,
                "modifications": list(modifications.keys())
            }, duration_ms)
            
            return modifications
            
        except Exception as e:
            self._handle_error("ERR_EMOTION_001", e, {
                "emotion": emotion,
                "intensity": intensity
            }, "RETRY")
            raise
    
    def list_emotions(self) -> List[str]:
        """Get list of available emotions"""
        return [e.value for e in Emotion]
    
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
# COMPONENT: VoiceProfileStorageComponent
# ============================================================================

class VoiceProfileStorageComponent:
    """
    COMPONENT CONTRACT:
    - Name: VoiceProfileStorageComponent
    - Function: Persist and retrieve voice profiles
    - IN: {operation: str, profile: VoiceProfile}
    - OUT: {success: bool, profile_id: str}
    - ERROR: Storage failure, profile not found
    """
    
    COMPONENT_NAME = "VoiceProfileStorageComponent"
    
    def __init__(self, storage_path: str = "./voice_profiles"):
        self.logger = logger
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)
    
    def save_profile(self, profile: VoiceProfile) -> Dict[str, Any]:
        """
        Save voice profile to storage
        
        IN Schema:
            profile: VoiceProfile - Profile to save
        
        OUT Schema:
            {success: bool, profile_id: str, file_path: str}
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "STORAGE_SAVE", {
            "profile_id": profile.profile_id,
            "name": profile.name
        })
        
        try:
            # Validate profile
            validation = profile.validate()
            if not validation["valid"]:
                raise VoiceTextException(f"Invalid profile: {validation['errors']}")
            
            # Create filename
            safe_name = "".join(c for c in profile.name if c.isalnum() or c in (' ', '-', '_'))
            filename = f"{profile.profile_id}_{safe_name}.json"
            file_path = self.storage_path / filename
            
            # Save to JSON
            with open(file_path, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
            
            result = {
                "success": True,
                "profile_id": profile.profile_id,
                "file_path": str(file_path)
            }
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "STORAGE_SAVE_SUCCESS", result, duration_ms)
            
            return result
            
        except Exception as e:
            self._handle_error("ERR_STORAGE_001", e, {
                "profile_id": profile.profile_id
            }, "RETRY")
            raise
    
    def load_profile(self, profile_id: str) -> VoiceProfile:
        """
        Load voice profile from storage
        
        IN Schema:
            profile_id: str - Profile ID to load
        
        OUT Schema:
            VoiceProfile object
        """
        trace_start = datetime.utcnow()
        self.logger.trace(self.COMPONENT_NAME, "STORAGE_LOAD", {"profile_id": profile_id})
        
        try:
            # Find profile file
            profile_files = list(self.storage_path.glob(f"{profile_id}_*.json"))
            
            if not profile_files:
                raise VoiceTextException(f"Profile not found: {profile_id}")
            
            # Load from JSON
            with open(profile_files[0], 'r') as f:
                data = json.load(f)
            
            profile = VoiceProfile.from_dict(data)
            
            duration_ms = (datetime.utcnow() - trace_start).total_seconds() * 1000
            self.logger.trace(self.COMPONENT_NAME, "STORAGE_LOAD_SUCCESS", {
                "profile_id": profile_id,
                "name": profile.name
            }, duration_ms)
            
            return profile
            
        except Exception as e:
            self._handle_error("ERR_STORAGE_002", e, {"profile_id": profile_id}, "ABORT")
            raise
    
    def list_profiles(self) -> List[Dict[str, str]]:
        """List all saved profiles"""
        profiles = []
        
        for file_path in self.storage_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    profiles.append({
                        "profile_id": data.get("profile_id"),
                        "name": data.get("name"),
                        "gender": data.get("gender"),
                        "language": data.get("language")
                    })
            except Exception:
                pass
        
        return profiles
    
    def delete_profile(self, profile_id: str) -> Dict[str, Any]:
        """Delete profile from storage"""
        try:
            profile_files = list(self.storage_path.glob(f"{profile_id}_*.json"))
            
            if not profile_files:
                raise VoiceTextException(f"Profile not found: {profile_id}")
            
            profile_files[0].unlink()
            
            return {"success": True, "profile_id": profile_id}
            
        except Exception as e:
            self._handle_error("ERR_STORAGE_003", e, {"profile_id": profile_id}, "ABORT")
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
# HIGH-LEVEL API: VoiceCustomizationEngine
# ============================================================================

class VoiceCustomizationEngine:
    """
    High-level API combining all voice customization components
    Provides simple interface for complex voice transformations
    """
    
    def __init__(self, storage_path: str = "./voice_profiles"):
        self.profile_manager = VoiceProfileComponent()
        self.effects = AudioEffectsComponent()
        self.transformer = VoiceTransformComponent()
        self.emotion_engine = EmotionEngineComponent()
        self.storage = VoiceProfileStorageComponent(storage_path)
    
    def create_custom_voice(self, name: str, base_preset: str = None, 
                           **customizations) -> VoiceProfile:
        """
        Create custom voice profile with easy customization
        
        Args:
            name: Profile name
            base_preset: Optional preset to start from
            **customizations: Voice parameters to customize
        
        Returns:
            VoiceProfile object
        
        Example:
            voice = engine.create_custom_voice(
                name="My Custom Voice",
                base_preset="professional_male",
                pitch=-1.0,
                speed=0.9,
                emotion_default="confident"
            )
        """
        if base_preset:
            profile = self.profile_manager.load_preset(base_preset)
            profile.name = name
            profile.profile_id = str(uuid.uuid4())
            
            # Apply customizations
            for key, value in customizations.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
        else:
            profile = self.profile_manager.create_profile(name, **customizations)
        
        # Save to storage
        self.storage.save_profile(profile)
        
        return profile
    
    def apply_voice_profile(self, audio: AudioData, profile: VoiceProfile,
                           emotion: Optional[str] = None,
                           emotion_intensity: float = 1.0,
                           effects: Optional[List[EffectConfig]] = None) -> AudioData:
        """
        Apply complete voice profile to audio
        
        Args:
            audio: Input audio
            profile: Voice profile to apply
            emotion: Optional emotional tone
            emotion_intensity: Emotion intensity (0.0-1.0)
            effects: Optional audio effects to apply
        
        Returns:
            Transformed AudioData
        """
        # Apply voice transformations
        transform = VoiceTransform(
            pitch_shift=profile.pitch,
            formant_shift=1.0 + (profile.pitch / 12.0) * 0.15  # Approximate formant
        )
        
        transformed_audio = self.transformer.transform_voice(audio, transform)
        
        # Apply emotion if specified
        if emotion:
            emotion_params = self.emotion_engine.apply_emotion(
                emotion,
                emotion_intensity,
                profile
            )
            # Apply emotional prosody (would modify audio in real implementation)
        
        # Apply effects if specified
        if effects:
            transformed_audio = self.effects.apply_effects(transformed_audio, effects)
        
        return transformed_audio
    
    def get_preset_list(self) -> List[str]:
        """Get list of available preset voice profiles"""
        return self.profile_manager.list_presets()
    
    def get_saved_profiles(self) -> List[Dict[str, str]]:
        """Get list of user-saved profiles"""
        return self.storage.list_profiles()
    
    def load_saved_profile(self, profile_id: str) -> VoiceProfile:
        """Load a saved custom profile"""
        return self.storage.load_profile(profile_id)

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Enhanced Voice Profile & Sound Customization Demo")
    print("=" * 70)
    
    # Initialize engine
    engine = VoiceCustomizationEngine()
    
    # Example 1: Create voice profile from preset
    print("\n[Example 1] Creating custom voice from preset...")
    voice1 = engine.create_custom_voice(
        name="My Professional Voice",
        base_preset="professional_male",
        pitch=-1.0,
        speed=0.95,
        emotion_default="confident"
    )
    print(f"✓ Created: {voice1.name}")
    print(f"  Profile ID: {voice1.profile_id}")
    print(f"  Pitch: {voice1.pitch}, Speed: {voice1.speed}")
    
    # Example 2: Create completely custom voice
    print("\n[Example 2] Creating custom voice from scratch...")
    voice2 = engine.create_custom_voice(
        name="Friendly Robot",
        gender=Gender.NEUTRAL.value,
        pitch=0.0,
        speed=1.1,
        volume=1.0,
        accent="robotic",
        emotion_default=Emotion.HAPPY.value
    )
    print(f"✓ Created: {voice2.name}")
    
    # Example 3: Apply audio effects
    print("\n[Example 3] Applying audio effects...")
    effects_component = AudioEffectsComponent()
    
    reverb = effects_component.create_reverb(room_size=0.7, damping=0.5)
    echo = effects_component.create_echo(delay_ms=300, feedback=0.4)
    eq = effects_component.create_equalizer(bass=3, mid=0, treble=-2)
    
    mock_audio = AudioData(b"SAMPLE_AUDIO", "wav", 44100, 3.0)
    processed = effects_component.apply_effects(mock_audio, [reverb, echo, eq])
    print(f"✓ Applied {len([reverb, echo, eq])} effects")
    print(f"  Original size: {len(mock_audio.audio_bytes)} bytes")
    print(f"  Processed size: {len(processed.audio_bytes)} bytes")
    
    # Example 4: Voice transformation
    print("\n[Example 4] Voice transformation presets...")
    transformer = VoiceTransformComponent()
    
    transform_presets = {
        "Male to Female": transformer.male_to_female(),
        "Female to Male": transformer.female_to_male(),
        "Robot Voice": transformer.robot_voice()
    }
    
    for preset_name, transform in transform_presets.items():
        result = transformer.transform_voice(mock_audio, transform)
        print(f"✓ {preset_name}: Pitch {transform.pitch_shift:+.1f}, "
              f"Formant {transform.formant_shift:.2f}")
    
    # Example 5: Emotion application
    print("\n[Example 5] Applying emotional tones...")
    emotion_engine = EmotionEngineComponent()
    
    emotions_to_test = [Emotion.HAPPY.value, Emotion.SAD.value, Emotion.ANGRY.value]
    
    for emotion in emotions_to_test:
        mods = emotion_engine.apply_emotion(emotion, intensity=0.8, base_profile=voice1)
        print(f"✓ {emotion.capitalize()}: "
              f"Pitch {mods['pitch_shift']:+.1f}, "
              f"Speed {mods['speed_multiplier']:.2f}x, "
              f"Volume {mods['volume_multiplier']:.2f}x")
    
    # Example 6: List available presets
    print("\n[Example 6] Available preset voices...")
    presets = engine.get_preset_list()
    print(f"Found {len(presets)} preset voices:")
    for preset in presets:
        print(f"  - {preset}")
    
    # Example 7: Load and modify saved profile
    print("\n[Example 7] Saved profiles...")
    saved = engine.get_saved_profiles()
    print(f"Found {len(saved)} saved profiles:")
    for profile_info in saved:
        print(f"  - {profile_info['name']} ({profile_info['gender']}, {profile_info['language']})")
    
    # Example 8: Complete voice customization pipeline
    print("\n[Example 8] Complete customization pipeline...")
    
    # Create custom voice
    custom_voice = engine.create_custom_voice(
        name="Energetic Presenter",
        base_preset="friendly_assistant",
        pitch=1.5,
        speed=1.15,
        emotion_default=Emotion.EXCITED.value
    )
    
    # Prepare effects
    effects_chain = [
        effects_component.create_reverb(room_size=0.3, damping=0.6),
        effects_component.create_equalizer(bass=2, mid=1, treble=0)
    ]
    
    # Apply complete profile
    final_audio = engine.apply_voice_profile(
        audio=mock_audio,
        profile=custom_voice,
        emotion=Emotion.EXCITED.value,
        emotion_intensity=0.7,
        effects=effects_chain
    )
    
    print(f"✓ Complete pipeline executed:")
    print(f"  Voice: {custom_voice.name}")
    print(f"  Emotion: {Emotion.EXCITED.value} (70% intensity)")
    print(f"  Effects: {len(effects_chain)} applied")
    print(f"  Output: {len(final_audio.audio_bytes)} bytes")
    
    print("\n" + "=" * 70)
    print("Demo complete! Check voice_profiles/ for saved profiles.")
    print("Check llm_interaction.log for detailed trace logs.")
    print("=" * 70)
