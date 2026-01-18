"""
Enhanced Voice Profile System - Comprehensive Test Suite
Tests for voice profiles, effects, transformations, and emotions
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import json

# Import enhanced components
try:
    from enhanced_voice_profiles import (
        VoiceProfile,
        VoiceProfileComponent,
        AudioEffectsComponent,
        VoiceTransformComponent,
        EmotionEngineComponent,
        VoiceProfileStorageComponent,
        VoiceCustomizationEngine,
        EffectConfig,
        VoiceTransform,
        Gender,
        Emotion,
        AudioEffect,
        VoiceTextException
    )
    from voice_text_lib import AudioData
except ImportError:
    pytest.skip("Enhanced voice modules not available", allow_module_level=True)

# ============================================================================
# TEST SUITE: VoiceProfile Data Schema
# ============================================================================

class TestVoiceProfile:
    """Test VoiceProfile data structure and validation"""
    
    def test_create_default_profile(self):
        """TC001: Create profile with default values"""
        profile = VoiceProfile(name="Test Voice")
        
        assert profile.name == "Test Voice"
        assert profile.gender == Gender.NEUTRAL.value
        assert profile.pitch == 0.0
        assert profile.speed == 1.0
        assert profile.volume == 1.0
        assert profile.profile_id is not None
    
    def test_create_custom_profile(self):
        """TC002: Create profile with custom parameters"""
        profile = VoiceProfile(
            name="Custom Voice",
            gender=Gender.MALE.value,
            pitch=-2.0,
            speed=0.9,
            volume=1.1,
            language="en-GB",
            accent="british"
        )
        
        assert profile.pitch == -2.0
        assert profile.speed == 0.9
        assert profile.language == "en-GB"
        assert profile.accent == "british"
    
    def test_validate_valid_profile(self):
        """TC003: Validation passes for valid profile"""
        profile = VoiceProfile(
            pitch=5.0,
            speed=1.5,
            volume=1.0
        )
        
        validation = profile.validate()
        assert validation["valid"] == True
        assert len(validation["errors"]) == 0
    
    def test_validate_invalid_pitch(self):
        """TC004: Validation fails for out-of-range pitch"""
        profile = VoiceProfile(pitch=15.0)
        
        validation = profile.validate()
        assert validation["valid"] == False
        assert any("Pitch" in error for error in validation["errors"])
    
    def test_validate_invalid_speed(self):
        """TC005: Validation fails for out-of-range speed"""
        profile = VoiceProfile(speed=3.0)
        
        validation = profile.validate()
        assert validation["valid"] == False
        assert any("Speed" in error for error in validation["errors"])
    
    def test_validate_invalid_volume(self):
        """TC006: Validation fails for out-of-range volume"""
        profile = VoiceProfile(volume=5.0)
        
        validation = profile.validate()
        assert validation["valid"] == False
        assert any("Volume" in error for error in validation["errors"])
    
    def test_validate_invalid_gender(self):
        """TC007: Validation fails for invalid gender"""
        profile = VoiceProfile(gender="invalid")
        
        validation = profile.validate()
        assert validation["valid"] == False
        assert any("gender" in error for error in validation["errors"])
    
    def test_profile_serialization(self):
        """TC008: Profile converts to/from dictionary"""
        original = VoiceProfile(
            name="Test",
            pitch=2.0,
            speed=1.1
        )
        
        # To dict
        data = original.to_dict()
        assert isinstance(data, dict)
        assert data["name"] == "Test"
        assert data["pitch"] == 2.0
        
        # From dict
        restored = VoiceProfile.from_dict(data)
        assert restored.name == original.name
        assert restored.pitch == original.pitch

# ============================================================================
# TEST SUITE: VoiceProfileComponent
# ============================================================================

class TestVoiceProfileComponent:
    """Test voice profile management"""
    
    @pytest.fixture
    def component(self):
        return VoiceProfileComponent()
    
    # POSITIVE TESTS
    
    def test_create_profile(self, component):
        """TC101: Create new voice profile"""
        profile = component.create_profile(
            name="Test Voice",
            pitch=-1.0,
            speed=0.95
        )
        
        assert profile.name == "Test Voice"
        assert profile.pitch == -1.0
        assert profile.profile_id in component.profiles_cache
    
    def test_load_preset(self, component):
        """TC102: Load predefined preset"""
        profile = component.load_preset("professional_male")
        
        assert profile is not None
        assert profile.name == "Professional Male"
        assert profile.gender == Gender.MALE.value
    
    def test_update_profile(self, component):
        """TC103: Update existing profile"""
        profile = component.create_profile(name="Original", pitch=0.0)
        
        updated = component.update_profile(
            profile.profile_id,
            pitch=2.0,
            speed=1.2
        )
        
        assert updated.pitch == 2.0
        assert updated.speed == 1.2
        assert updated.name == "Original"
    
    def test_list_presets(self, component):
        """TC104: List available presets"""
        presets = component.list_presets()
        
        assert isinstance(presets, list)
        assert len(presets) > 0
        assert "professional_male" in presets
        assert "professional_female" in presets
    
    def test_cache_management(self, component):
        """TC105: Profiles are cached correctly"""
        profile1 = component.create_profile(name="Voice1")
        profile2 = component.create_profile(name="Voice2")
        
        assert len(component.profiles_cache) == 2
        assert profile1.profile_id in component.profiles_cache
        assert profile2.profile_id in component.profiles_cache
    
    # NEGATIVE TESTS
    
    def test_create_invalid_profile(self, component):
        """TC106: Reject invalid profile parameters"""
        with pytest.raises(VoiceTextException):
            component.create_profile(
                name="Invalid",
                pitch=20.0  # Out of range
            )
    
    def test_load_nonexistent_preset(self, component):
        """TC107: Error on nonexistent preset"""
        with pytest.raises(VoiceTextException, match="Preset not found"):
            component.load_preset("nonexistent_preset")
    
    def test_update_nonexistent_profile(self, component):
        """TC108: Error updating nonexistent profile"""
        with pytest.raises(VoiceTextException, match="Profile not found"):
            component.update_profile("fake_id", pitch=1.0)
    
    def test_update_with_invalid_params(self, component):
        """TC109: Reject invalid update parameters"""
        profile = component.create_profile(name="Test")
        
        with pytest.raises(VoiceTextException):
            component.update_profile(profile.profile_id, pitch=25.0)

# ============================================================================
# TEST SUITE: AudioEffectsComponent
# ============================================================================

class TestAudioEffectsComponent:
    """Test audio effects processing"""
    
    @pytest.fixture
    def component(self):
        return AudioEffectsComponent()
    
    @pytest.fixture
    def sample_audio(self):
        return AudioData(b"SAMPLE_AUDIO_DATA", "wav", 44100, 3.0)
    
    # POSITIVE TESTS
    
    def test_create_reverb_effect(self, component):
        """TC201: Create reverb effect configuration"""
        reverb = component.create_reverb(room_size=0.7, damping=0.5)
        
        assert reverb.effect_type == AudioEffect.REVERB.value
        assert reverb.intensity == 0.7
        assert reverb.parameters["damping"] == 0.5
    
    def test_create_echo_effect(self, component):
        """TC202: Create echo effect configuration"""
        echo = component.create_echo(delay_ms=500, feedback=0.3)
        
        assert echo.effect_type == AudioEffect.ECHO.value
        assert echo.parameters["delay_ms"] == 500
        assert echo.parameters["feedback"] == 0.3
    
    def test_create_equalizer_effect(self, component):
        """TC203: Create equalizer configuration"""
        eq = component.create_equalizer(bass=3, mid=0, treble=-2)
        
        assert eq.effect_type == AudioEffect.EQUALIZER.value
        assert eq.parameters["bass"] == 3
        assert eq.parameters["treble"] == -2
    
    def test_apply_single_effect(self, component, sample_audio):
        """TC204: Apply single effect to audio"""
        reverb = component.create_reverb(room_size=0.5)
        
        result = component.apply_effects(sample_audio, [reverb])
        
        assert isinstance(result, AudioData)
        assert result.format == sample_audio.format
        assert result.sample_rate == sample_audio.sample_rate
    
    def test_apply_multiple_effects(self, component, sample_audio):
        """TC205: Apply chain of effects"""
        effects = [
            component.create_reverb(room_size=0.5),
            component.create_echo(delay_ms=300),
            component.create_equalizer(bass=2)
        ]
        
        result = component.apply_effects(sample_audio, effects)
        
        assert isinstance(result, AudioData)
        # In mock implementation, effects are marked in bytes
        assert len(result.audio_bytes) > len(sample_audio.audio_bytes)
    
    def test_effect_validation(self, component):
        """TC206: Validate effect configurations"""
        valid_effect = EffectConfig(
            effect_type=AudioEffect.REVERB.value,
            intensity=0.5
        )
        
        assert valid_effect.validate() == True
    
    # NEGATIVE TESTS
    
    def test_invalid_effect_type(self, component, sample_audio):
        """TC207: Reject invalid effect type"""
        invalid_effect = EffectConfig(
            effect_type="invalid_effect",
            intensity=0.5
        )
        
        with pytest.raises(VoiceTextException):
            component.apply_effects(sample_audio, [invalid_effect])
    
    def test_invalid_effect_intensity(self):
        """TC208: Reject out-of-range intensity"""
        effect = EffectConfig(
            effect_type=AudioEffect.REVERB.value,
            intensity=2.0  # > 1.0
        )
        
        assert effect.validate() == False
    
    def test_empty_effects_list(self, component, sample_audio):
        """TC209: Handle empty effects list"""
        result = component.apply_effects(sample_audio, [])
        
        assert result is not None

# ============================================================================
# TEST SUITE: VoiceTransformComponent
# ============================================================================

class TestVoiceTransformComponent:
    """Test voice transformation"""
    
    @pytest.fixture
    def component(self):
        return VoiceTransformComponent()
    
    @pytest.fixture
    def sample_audio(self):
        return AudioData(b"VOICE_SAMPLE", "wav", 16000, 2.0)
    
    # POSITIVE TESTS
    
    def test_pitch_shift_transform(self, component, sample_audio):
        """TC301: Apply pitch shift transformation"""
        transform = VoiceTransform(pitch_shift=3.0)
        
        result = component.transform_voice(sample_audio, transform)
        
        assert isinstance(result, AudioData)
        assert b"PITCH:+3.0" in result.audio_bytes
    
    def test_formant_shift_transform(self, component, sample_audio):
        """TC302: Apply formant shift"""
        transform = VoiceTransform(formant_shift=1.15)
        
        result = component.transform_voice(sample_audio, transform)
        
        assert isinstance(result, AudioData)
        assert b"FORMANT:" in result.audio_bytes
    
    def test_timbre_morph_transform(self, component, sample_audio):
        """TC303: Apply timbre morphing"""
        transform = VoiceTransform(timbre_morph=0.5)
        
        result = component.transform_voice(sample_audio, transform)
        
        assert isinstance(result, AudioData)
        assert b"TIMBRE:" in result.audio_bytes
    
    def test_combined_transforms(self, component, sample_audio):
        """TC304: Apply multiple transformations"""
        transform = VoiceTransform(
            pitch_shift=2.0,
            formant_shift=1.1,
            timbre_morph=0.3
        )
        
        result = component.transform_voice(sample_audio, transform)
        
        # All transformations should be applied
        assert b"PITCH:" in result.audio_bytes
        assert b"FORMANT:" in result.audio_bytes
        assert b"TIMBRE:" in result.audio_bytes
    
    def test_male_to_female_preset(self, component, sample_audio):
        """TC305: Male-to-female transformation preset"""
        transform = component.male_to_female()
        
        assert transform.pitch_shift > 0
        assert transform.formant_shift > 1.0
        
        result = component.transform_voice(sample_audio, transform)
        assert result is not None
    
    def test_female_to_male_preset(self, component, sample_audio):
        """TC306: Female-to-male transformation preset"""
        transform = component.female_to_male()
        
        assert transform.pitch_shift < 0
        assert transform.formant_shift < 1.0
        
        result = component.transform_voice(sample_audio, transform)
        assert result is not None
    
    def test_robot_voice_preset(self, component, sample_audio):
        """TC307: Robot voice transformation"""
        transform = component.robot_voice()
        
        assert transform.roughness > 0
        
        result = component.transform_voice(sample_audio, transform)
        assert result is not None
    
    # NEGATIVE TESTS
    
    def test_zero_transforms(self, component, sample_audio):
        """TC308: Handle no transformations"""
        transform = VoiceTransform()  # All zeros
        
        result = component.transform_voice(sample_audio, transform)
        assert result is not None

# ============================================================================
# TEST SUITE: EmotionEngineComponent
# ============================================================================

class TestEmotionEngineComponent:
    """Test emotional tone application"""
    
    @pytest.fixture
    def component(self):
        return EmotionEngineComponent()
    
    @pytest.fixture
    def base_profile(self):
        return VoiceProfile(name="Test", pitch=0.0, speed=1.0, volume=1.0)
    
    # POSITIVE TESTS
    
    def test_apply_happy_emotion(self, component, base_profile):
        """TC401: Apply happy emotion"""
        mods = component.apply_emotion(
            Emotion.HAPPY.value,
            intensity=1.0,
            base_profile=base_profile
        )
        
        assert mods["emotion"] == Emotion.HAPPY.value
        assert mods["pitch_shift"] > 0  # Higher pitch
        assert mods["speed_multiplier"] > 1.0  # Faster
    
    def test_apply_sad_emotion(self, component, base_profile):
        """TC402: Apply sad emotion"""
        mods = component.apply_emotion(
            Emotion.SAD.value,
            intensity=1.0,
            base_profile=base_profile
        )
        
        assert mods["emotion"] == Emotion.SAD.value
        assert mods["pitch_shift"] < 0  # Lower pitch
        assert mods["speed_multiplier"] < 1.0  # Slower
    
    def test_apply_angry_emotion(self, component, base_profile):
        """TC403: Apply angry emotion"""
        mods = component.apply_emotion(
            Emotion.ANGRY.value,
            intensity=1.0,
            base_profile=base_profile
        )
        
        assert mods["volume_multiplier"] > 1.0  # Louder
        assert mods["speed_multiplier"] > 1.0  # Faster
    
    def test_emotion_intensity_scaling(self, component, base_profile):
        """TC404: Intensity scales emotion effects"""
        low = component.apply_emotion(
            Emotion.HAPPY.value,
            intensity=0.3,
            base_profile=base_profile
        )
        high = component.apply_emotion(
            Emotion.HAPPY.value,
            intensity=1.0,
            base_profile=base_profile
        )
        
        assert abs(low["pitch_shift"]) < abs(high["pitch_shift"])
    
    def test_emotion_without_base_profile(self, component):
        """TC405: Apply emotion without base profile"""
        mods = component.apply_emotion(Emotion.CALM.value, intensity=0.8)
        
        assert mods is not None
        assert "pitch_shift" in mods
        assert "final_pitch" not in mods  # Only present with base_profile
    
    def test_list_emotions(self, component):
        """TC406: List available emotions"""
        emotions = component.list_emotions()
        
        assert isinstance(emotions, list)
        assert len(emotions) > 0
        assert Emotion.HAPPY.value in emotions
        assert Emotion.SAD.value in emotions
    
    # NEGATIVE TESTS
    
    def test_invalid_emotion(self, component):
        """TC407: Reject invalid emotion type"""
        with pytest.raises(VoiceTextException, match="Invalid emotion"):
            component.apply_emotion("invalid_emotion", intensity=0.5)
    
    def test_invalid_intensity(self, component):
        """TC408: Reject out-of-range intensity"""
        with pytest.raises(VoiceTextException, match="Intensity"):
            component.apply_emotion(Emotion.HAPPY.value, intensity=2.0)

# ============================================================================
# TEST SUITE: VoiceProfileStorageComponent
# ============================================================================

class TestVoiceProfileStorageComponent:
    """Test profile persistence"""
    
    @pytest.fixture
    def temp_storage(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def component(self, temp_storage):
        return VoiceProfileStorageComponent(storage_path=temp_storage)
    
    @pytest.fixture
    def sample_profile(self):
        return VoiceProfile(
            name="Test Profile",
            pitch=1.5,
            speed=0.9
        )
    
    # POSITIVE TESTS
    
    def test_save_profile(self, component, sample_profile):
        """TC501: Save profile to storage"""
        result = component.save_profile(sample_profile)
        
        assert result["success"] == True
        assert result["profile_id"] == sample_profile.profile_id
        assert Path(result["file_path"]).exists()
    
    def test_load_profile(self, component, sample_profile):
        """TC502: Load profile from storage"""
        # Save first
        component.save_profile(sample_profile)
        
        # Load
        loaded = component.load_profile(sample_profile.profile_id)
        
        assert loaded.name == sample_profile.name
        assert loaded.pitch == sample_profile.pitch
        assert loaded.profile_id == sample_profile.profile_id
    
    def test_list_profiles(self, component):
        """TC503: List all saved profiles"""
        # Save multiple profiles
        profiles = [
            VoiceProfile(name="Voice1", gender=Gender.MALE.value),
            VoiceProfile(name="Voice2", gender=Gender.FEMALE.value)
        ]
        
        for profile in profiles:
            component.save_profile(profile)
        
        # List
        listed = component.list_profiles()
        
        assert len(listed) == 2
        assert any(p["name"] == "Voice1" for p in listed)
        assert any(p["name"] == "Voice2" for p in listed)
    
    def test_delete_profile(self, component, sample_profile):
        """TC504: Delete profile from storage"""
        # Save first
        component.save_profile(sample_profile)
        
        # Delete
        result = component.delete_profile(sample_profile.profile_id)
        
        assert result["success"] == True
        
        # Verify deleted
        with pytest.raises(VoiceTextException):
            component.load_profile(sample_profile.profile_id)
    
    # NEGATIVE TESTS
    
    def test_save_invalid_profile(self, component):
        """TC505: Reject invalid profile"""
        invalid = VoiceProfile(pitch=50.0)  # Out of range
        
        with pytest.raises(VoiceTextException):
            component.save_profile(invalid)
    
    def test_load_nonexistent_profile(self, component):
        """TC506: Error loading nonexistent profile"""
        with pytest.raises(VoiceTextException, match="Profile not found"):
            component.load_profile("nonexistent_id")
    
    def test_delete_nonexistent_profile(self, component):
        """TC507: Error deleting nonexistent profile"""
        with pytest.raises(VoiceTextException):
            component.delete_profile("nonexistent_id")

# ============================================================================
# TEST SUITE: VoiceCustomizationEngine (Integration)
# ============================================================================

class TestVoiceCustomizationEngine:
    """Test high-level voice customization API"""
    
    @pytest.fixture
    def temp_storage(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def engine(self, temp_storage):
        return VoiceCustomizationEngine(storage_path=temp_storage)
    
    @pytest.fixture
    def sample_audio(self):
        return AudioData(b"SAMPLE", "wav", 16000, 2.0)
    
    # INTEGRATION TESTS
    
    def test_create_custom_voice_from_preset(self, engine):
        """TC601: Create custom voice from preset"""
        voice = engine.create_custom_voice(
            name="My Voice",
            base_preset="professional_male",
            pitch=-0.5
        )
        
        assert voice.name == "My Voice"
        assert voice.pitch == -0.5
        assert voice.gender == Gender.MALE.value
    
    def test_create_custom_voice_from_scratch(self, engine):
        """TC602: Create custom voice without preset"""
        voice = engine.create_custom_voice(
            name="Custom",
            gender=Gender.FEMALE.value,
            pitch=2.0,
            speed=1.1
        )
        
        assert voice.name == "Custom"
        assert voice.gender == Gender.FEMALE.value
        assert voice.pitch == 2.0
    
    def test_apply_complete_voice_profile(self, engine, sample_audio):
        """TC603: Apply full voice profile with emotion and effects"""
        voice = engine.create_custom_voice(
            name="Test",
            pitch=1.0
        )
        
        effects = [
            engine.effects.create_reverb(room_size=0.5)
        ]
        
        result = engine.apply_voice_profile(
            audio=sample_audio,
            profile=voice,
            emotion=Emotion.HAPPY.value,
            emotion_intensity=0.8,
            effects=effects
        )
        
        assert isinstance(result, AudioData)
    
    def test_get_preset_list(self, engine):
        """TC604: Get available presets"""
        presets = engine.get_preset_list()
        
        assert len(presets) > 0
        assert "professional_male" in presets
    
    def test_save_and_load_custom_profile(self, engine):
        """TC605: Save custom profile and reload it"""
        # Create and save
        voice = engine.create_custom_voice(
            name="Saved Voice",
            pitch=1.5
        )
        
        # Load
        loaded = engine.load_saved_profile(voice.profile_id)
        
        assert loaded.name == voice.name
        assert loaded.pitch == voice.pitch

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--cov=enhanced_voice_profiles"])
