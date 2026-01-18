# Usage Guide

Comprehensive guide for using the Voice-Text Conversion Library with examples and best practices.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Voice Profiles](#voice-profiles)
4. [Audio Effects](#audio-effects)
5. [Voice Transformation](#voice-transformation)
6. [Emotional Tones](#emotional-tones)
7. [Advanced Workflows](#advanced-workflows)
8. [Best Practices](#best-practices)
9. [Error Handling](#error-handling)
10. [Performance Optimization](#performance-optimization)

---

## 🚀 Getting Started

### Quick Start Example

```python
from voice_text_lib import (
    AudioFileLoaderComponent,
    SpeechRecognitionComponent,
    TextNormalizerComponent,
    TTSEngineComponent,
    AudioFileWriterComponent
)
from enhanced_voice_profiles import VoiceCustomizationEngine

# Initialize components
loader = AudioFileLoaderComponent()
stt = SpeechRecognitionComponent()
normalizer = TextNormalizerComponent()
tts = TTSEngineComponent()
writer = AudioFileWriterComponent()
engine = VoiceCustomizationEngine()

# Voice → Text → Voice Pipeline
audio_input = loader.load("speech.wav")
text = stt.recognize(audio_input, engine='google')
normalized = normalizer.normalize(text.text)
audio_output = tts.synthesize(normalized)
writer.write(audio_output, "output.mp3")

print(f"✅ Processed: {normalized.text}")
```

---

## 📖 Basic Operations

### 1. Loading Audio Files

```python
from voice_text_lib import AudioFileLoaderComponent

loader = AudioFileLoaderComponent()

# Load single file
audio = loader.load("recording.wav")
print(f"Format: {audio.format}")
print(f"Sample Rate: {audio.sample_rate} Hz")
print(f"Duration: {audio.duration:.2f} seconds")
print(f"Size: {len(audio.audio_bytes)} bytes")

# Load with format validation
try:
    audio = loader.load("audio.mp3", expected_format="mp3")
except Exception as e:
    print(f"Error: {e}")

# Batch loading
import os
audio_files = []
for filename in os.listdir("audio_folder"):
    if filename.endswith(".wav"):
        audio = loader.load(f"audio_folder/{filename}")
        audio_files.append(audio)
```

### 2. Text Normalization

```python
from voice_text_lib import TextNormalizerComponent

normalizer = TextNormalizerComponent()

# Basic normalization
text = "  HELLO,   WORLD!   How   are   you?  "
result = normalizer.normalize(text)
print(result.text)  # "HELLO, WORLD! How are you?"

# Lowercase conversion
result = normalizer.normalize("SHOUTING TEXT", lowercase=True)
print(result.text)  # "shouting text"

# Remove punctuation
result = normalizer.normalize(
    "Hello, world! How are you?",
    remove_punctuation=True
)
print(result.text)  # "Hello world How are you"

# Combined operations
result = normalizer.normalize(
    "  MESSY,  TEXT!!!  ",
    lowercase=True,
    remove_punctuation=True,
    strip_whitespace=True
)
print(result.text)  # "messy text"

# Check metadata
print(f"Original length: {result.metadata['original_length']}")
print(f"Final length: {result.metadata['final_length']}")
```

### 3. Speech Recognition (Voice → Text)

```python
from voice_text_lib import AudioFileLoaderComponent, SpeechRecognitionComponent

loader = AudioFileLoaderComponent()
stt = SpeechRecognitionComponent(api_key="YOUR_API_KEY")

# Basic recognition
audio = loader.load("speech.wav")
result = stt.recognize(audio, engine='google', language='en-US')

print(f"Transcribed: {result.text}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Language: {result.language}")

# Try different engines
engines = ['google', 'azure', 'whisper', 'sphinx']
for engine in engines:
    try:
        result = stt.recognize(audio, engine=engine)
        print(f"{engine}: {result.text}")
    except Exception as e:
        print(f"{engine} failed: {e}")

# Different languages
languages = ['en-US', 'es-ES', 'fr-FR', 'de-DE']
for lang in languages:
    result = stt.recognize(audio, language=lang)
    print(f"{lang}: {result.text}")

# Handle long audio
def transcribe_long_audio(audio_path, chunk_duration=30):
    """Transcribe long audio by chunking"""
    results = []
    # Implement audio chunking here
    for chunk in audio_chunks:
        result = stt.recognize(chunk)
        results.append(result.text)
    return " ".join(results)
```

### 4. Text-to-Speech (Text → Voice)

```python
from voice_text_lib import TextNormalizerComponent, TTSEngineComponent, AudioFileWriterComponent

normalizer = TextNormalizerComponent()
tts = TTSEngineComponent(api_key="YOUR_API_KEY")
writer = AudioFileWriterComponent()

# Basic synthesis
text = normalizer.normalize("Hello! Welcome to our system.")
audio = tts.synthesize(text, engine='gtts')
writer.write(audio, "greeting.mp3")

# Different engines
engines = {
    'gtts': 'Google TTS (online)',
    'pyttsx3': 'Offline TTS',
    'azure': 'Azure Cognitive Services'
}

for engine, description in engines.items():
    try:
        audio = tts.synthesize(text, engine=engine)
        writer.write(audio, f"output_{engine}.mp3")
        print(f"✅ {description}")
    except Exception as e:
        print(f"❌ {description}: {e}")

# Different voices (Azure example)
voices = [
    'en-US-JennyNeural',  # Female
    'en-US-GuyNeural',    # Male
    'en-GB-SoniaNeural',  # British Female
    'en-AU-NatashaNeural' # Australian Female
]

for voice in voices:
    audio = tts.synthesize(text, engine='azure', voice=voice)
    writer.write(audio, f"output_{voice}.mp3")

# Adjust speed
audio_slow = tts.synthesize(text, speed=0.75)  # 75% speed
audio_fast = tts.synthesize(text, speed=1.5)   # 150% speed
```

### 5. Saving Audio Files

```python
from voice_text_lib import AudioFileWriterComponent, AudioData

writer = AudioFileWriterComponent(base_dir="./my_audio")

# Basic save
audio = AudioData(b"sample_data", "wav", 44100, 3.0)
result = writer.write(audio, "output.wav")
print(f"Saved to: {result['file_path']}")
print(f"Size: {result['file_size']} bytes")

# Save with subdirectories
result = writer.write(audio, "project1/session1/recording.wav")

# Overwrite protection
try:
    writer.write(audio, "output.wav", overwrite=False)
except Exception as e:
    print("File exists!")

# Overwrite allowed
writer.write(audio, "output.wav", overwrite=True)

# Batch save
audios = [audio1, audio2, audio3]
for i, audio in enumerate(audios):
    writer.write(audio, f"batch/audio_{i:03d}.wav")
```

---

## 🎤 Voice Profiles

### Creating Voice Profiles

```python
from enhanced_voice_profiles import VoiceCustomizationEngine, Gender, Emotion

engine = VoiceCustomizationEngine()

# Method 1: From preset
voice1 = engine.create_custom_voice(
    name="My Professional Voice",
    base_preset="professional_male",
    pitch=-1.0,
    speed=0.95
)

# Method 2: From scratch
voice2 = engine.create_custom_voice(
    name="Custom Character",
    gender=Gender.FEMALE.value,
    pitch=2.0,
    speed=1.1,
    volume=1.05,
    language="en-US",
    accent="american",
    age_range="young",
    emotion_default=Emotion.HAPPY.value
)

# Method 3: Fine-tuned control
voice3 = engine.create_custom_voice(
    name="Podcast Host",
    base_preset="friendly_assistant",
    pitch=0.5,
    speed=1.05,
    volume=1.0,
    timbre={"warmth": 0.7, "brightness": 0.6},
    emotion_default=Emotion.CONFIDENT.value,
    custom_params={
        "breathing": 0.2,
        "expressiveness": 0.8
    }
)

print(f"Created voice: {voice3.name}")
print(f"Profile ID: {voice3.profile_id}")
```

### Using Preset Profiles

```python
# List available presets
presets = engine.get_preset_list()
print("Available presets:")
for preset in presets:
    print(f"  - {preset}")

# Load preset
voice = engine.profile_manager.load_preset("professional_female")
print(f"Loaded: {voice.name}")
print(f"Gender: {voice.gender}")
print(f"Pitch: {voice.pitch}")
print(f"Speed: {voice.speed}")

# Customize preset
voice = engine.create_custom_voice(
    name="Customized Preset",
    base_preset="narrator_deep",
    pitch=-2.0,  # Make it slightly higher than default
    speed=0.9    # Slightly faster
)
```

### Voice Profile Parameters

```python
# Complete parameter example
voice = engine.create_custom_voice(
    name="Detailed Voice",
    
    # Basic parameters
    gender=Gender.MALE.value,    # male, female, neutral, custom
    pitch=-1.5,                  # -12 to +12 semitones
    speed=0.95,                  # 0.5 to 2.0 multiplier
    volume=1.0,                  # 0.0 to 2.0 multiplier
    
    # Voice characteristics
    timbre={
        "warmth": 0.8,          # 0.0 to 1.0
        "brightness": 0.5,      # 0.0 to 1.0
        "richness": 0.7         # 0.0 to 1.0
    },
    
    # Localization
    language="en-US",           # Language code
    accent="american",          # Regional accent
    
    # Demographics
    age_range="adult",          # child, young, adult, elderly
    
    # Expression
    emotion_default=Emotion.CALM.value,  # Default emotion
    
    # Advanced
    custom_params={
        "breathing_depth": 0.3,
        "articulation": 0.8,
        "resonance": 0.6
    }
)

# Validate profile
validation = voice.validate()
if validation["valid"]:
    print("✅ Profile is valid")
else:
    print("❌ Validation errors:")
    for error in validation["errors"]:
        print(f"  - {error}")
```

### Saving and Loading Profiles

```python
# Profiles are automatically saved when created
voice = engine.create_custom_voice(name="My Voice", pitch=1.0)
# Saved to: ./voice_profiles/{profile_id}_My_Voice.json

# List saved profiles
saved = engine.get_saved_profiles()
print(f"Saved profiles: {len(saved)}")
for profile in saved:
    print(f"  - {profile['name']} ({profile['gender']})")

# Load saved profile
profile_id = saved[0]['profile_id']
loaded_voice = engine.load_saved_profile(profile_id)
print(f"Loaded: {loaded_voice.name}")

# Manual save/load using storage component
storage = engine.storage

# Save
result = storage.save_profile(voice)
print(f"Saved to: {result['file_path']}")

# Load
loaded = storage.load_profile(voice.profile_id)

# Delete
storage.delete_profile(voice.profile_id)
```

---

## 🎛️ Audio Effects

### Applying Single Effects

```python
from enhanced_voice_profiles import VoiceCustomizationEngine

engine = VoiceCustomizationEngine()
effects = engine.effects

# Load audio
from voice_text_lib import AudioFileLoaderComponent
loader = AudioFileLoaderComponent()
audio = loader.load("voice.wav")

# Reverb (room acoustics)
reverb = effects.create_reverb(
    room_size=0.7,  # 0.0 (small) to 1.0 (large)
    damping=0.5     # High frequency absorption
)
audio_reverb = effects.apply_effects(audio, [reverb])

# Echo (delay effect)
echo = effects.create_echo(
    delay_ms=300,   # Delay time in milliseconds
    feedback=0.4    # Amount of repetition (0.0 to 1.0)
)
audio_echo = effects.apply_effects(audio, [echo])

# Equalizer (frequency adjustment)
eq = effects.create_equalizer(
    bass=3,    # -12 to +12 dB
    mid=0,     # No change
    treble=-2  # -2 dB cut
)
audio_eq = effects.apply_effects(audio, [eq])
```

### Creating Effect Chains

```python
# Professional podcast chain
podcast_chain = [
    effects.create_equalizer(bass=2, mid=1, treble=-1),
    effects.create_compressor(ratio=3.0, threshold=-20),
    effects.create_reverb(room_size=0.2, damping=0.7),
    effects.create_noise_gate(threshold=-40)
]

# Apply chain
processed = effects.apply_effects(audio, podcast_chain)

# Radio broadcast chain
radio_chain = [
    effects.create_equalizer(bass=4, mid=2, treble=-2),
    effects.create_compressor(ratio=6.0, threshold=-15),
    effects.create_distortion(amount=0.2)
]

# Vocal enhancement chain
vocal_chain = [
    effects.create_noise_gate(threshold=-35),
    effects.create_equalizer(bass=-2, mid=3, treble=1),
    effects.create_compressor(ratio=4.0),
    effects.create_reverb(room_size=0.3, damping=0.6)
]

# Creative effects chain
creative_chain = [
    effects.create_pitch_shift(semitones=2),
    effects.create_chorus(depth=0.5, rate=1.5),
    effects.create_reverb(room_size=0.9),
    effects.create_echo(delay_ms=500, feedback=0.3)
]
```

### Effect Presets

```python
def create_preset_chain(preset_name):
    """Get predefined effect chains"""
    
    presets = {
        "podcast": [
            effects.create_equalizer(bass=2, mid=1, treble=-1),
            effects.create_compressor(ratio=3.0),
            effects.create_reverb(room_size=0.2)
        ],
        
        "radio": [
            effects.create_equalizer(bass=4, mid=2, treble=-2),
            effects.create_compressor(ratio=6.0),
            effects.create_distortion(amount=0.2)
        ],
        
        "concert_hall": [
            effects.create_reverb(room_size=0.9, damping=0.3),
            effects.create_echo(delay_ms=500, feedback=0.2)
        ],
        
        "telephone": [
            effects.create_equalizer(bass=-6, mid=0, treble=-4),
            effects.create_compressor(ratio=8.0),
            effects.create_distortion(amount=0.3)
        ],
        
        "underwater": [
            effects.create_equalizer(bass=4, mid=-3, treble=-6),
            effects.create_reverb(room_size=0.7, damping=0.8),
            effects.create_chorus(depth=0.6)
        ]
    }
    
    return presets.get(preset_name, [])

# Use preset
audio_processed = effects.apply_effects(
    audio,
    create_preset_chain("podcast")
)
```

---

## 🔄 Voice Transformation

### Basic Transformations

```python
from enhanced_voice_profiles import VoiceTransformComponent, VoiceTransform

transformer = VoiceTransformComponent()

# Load audio
audio = loader.load("voice.wav")

# Pitch shifting
high_pitch = VoiceTransform(pitch_shift=4.0)  # +4 semitones
low_pitch = VoiceTransform(pitch_shift=-4.0)  # -4 semitones

audio_high = transformer.transform_voice(audio, high_pitch)
audio_low = transformer.transform_voice(audio, low_pitch)

# Formant shifting (changes perceived gender)
feminine = VoiceTransform(formant_shift=1.15)  # Higher formants
masculine = VoiceTransform(formant_shift=0.85)  # Lower formants

# Timbre morphing
bright = VoiceTransform(timbre_morph=0.8)   # Brighter sound
dark = VoiceTransform(timbre_morph=-0.8)    # Darker sound

# Combined transformation
custom = VoiceTransform(
    pitch_shift=2.0,
    formant_shift=1.1,
    timbre_morph=0.3,
    breathiness=0.2,
    roughness=0.1
)
audio_custom = transformer.transform_voice(audio, custom)
```

### Preset Transformations

```python
# Male to Female
m2f_audio = transformer.transform_voice(
    male_audio,
    transformer.male_to_female()
)

# Female to Male
f2m_audio = transformer.transform_voice(
    female_audio,
    transformer.female_to_male()
)

# Robot Voice
robot_audio = transformer.transform_voice(
    audio,
    transformer.robot_voice()
)

# Custom presets
def child_voice():
    return VoiceTransform(
        pitch_shift=6.0,
        formant_shift=1.2,
        timbre_morph=0.5
    )

def elderly_voice():
    return VoiceTransform(
        pitch_shift=-1.0,
        formant_shift=0.95,
        timbre_morph=-0.3,
        breathiness=0.3,
        roughness=0.4
    )

def whisper_voice():
    return VoiceTransform(
        pitch_shift=0.0,
        formant_shift=1.0,
        timbre_morph=-0.5,
        breathiness=0.8,
        roughness=0.2
    )
```

### Gradual Transformations

```python
def morph_voices(audio, start_transform, end_transform, steps=10):
    """Gradually morph from one voice to another"""
    
    morphed_audios = []
    
    for i in range(steps + 1):
        progress = i / steps
        
        # Interpolate between transformations
        current_transform = VoiceTransform(
            pitch_shift=start_transform.pitch_shift + 
                       (end_transform.pitch_shift - start_transform.pitch_shift) * progress,
            formant_shift=start_transform.formant_shift + 
                         (end_transform.formant_shift - start_transform.formant_shift) * progress,
            timbre_morph=start_transform.timbre_morph + 
                        (end_transform.timbre_morph - start_transform.timbre_morph) * progress
        )
        
        morphed = transformer.transform_voice(audio, current_transform)
        morphed_audios.append(morphed)
    
    return morphed_audios

# Create morphing sequence
male_transform = transformer.female_to_male()
female_transform = transformer.male_to_female()

sequence = morph_voices(audio, male_transform, female_transform, steps=20)
```

---

## 😊 Emotional Tones

### Applying Emotions

```python
from enhanced_voice_profiles import EmotionEngineComponent, Emotion

emotion_engine = EmotionEngineComponent()

# List available emotions
emotions = emotion_engine.list_emotions()
print("Available emotions:", emotions)

# Apply basic emotion
mods = emotion_engine.apply_emotion(
    emotion=Emotion.HAPPY.value,
    intensity=0.8
)

print(f"Pitch shift: {mods['pitch_shift']}")
print(f"Speed: {mods['speed_multiplier']}x")
print(f"Volume: {mods['volume_multiplier']}x")

# Apply with voice profile
voice = engine.create_custom_voice(name="Base Voice")

mods = emotion_engine.apply_emotion(
    emotion=Emotion.EXCITED.value,
    intensity=0.9,
    base_profile=voice
)

print(f"Final pitch: {mods['final_pitch']}")
print(f"Final speed: {mods['final_speed']}")
print(f"Final volume: {mods['final_volume']}")
```

### Emotion Intensity Levels

```python
# Test different intensities
emotion = Emotion.HAPPY.value

for intensity in [0.3, 0.5, 0.7, 1.0]:
    mods = emotion_engine.apply_emotion(emotion, intensity)
    print(f"Intensity {intensity:.0%}: Pitch {mods['pitch_shift']:+.2f}")

# Subtle emotion (professional use)
subtle = engine.apply_voice_profile(
    audio,
    profile=voice,
    emotion=Emotion.CONFIDENT.value,
    emotion_intensity=0.5
)

# Strong emotion (dramatic use)
strong = engine.apply_voice_profile(
    audio,
    profile=voice,
    emotion=Emotion.EXCITED.value,
    emotion_intensity=1.0
)
```

### Context-Aware Emotions

```python
def detect_emotion_from_text(text):
    """Simple emotion detection based on keywords"""
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great']):
        return Emotion.HAPPY.value, 0.8
    elif any(word in text_lower for word in ['sad', 'sorry', 'unfortunate']):
        return Emotion.SAD.value, 0.7
    elif any(word in text_lower for word in ['angry', 'furious', 'mad']):
        return Emotion.ANGRY.value, 0.8
    elif any(word in text_lower for word in ['calm', 'peaceful', 'relax']):
        return Emotion.CALM.value, 0.7
    else:
        return Emotion.NEUTRAL.value, 1.0

# Apply emotion based on content
texts = [
    "I'm so excited to share this news!",
    "Unfortunately, we have some sad news today.",
    "This is absolutely unacceptable!",
    "Let's take a moment to breathe and relax."
]

for text in texts:
    emotion, intensity = detect_emotion_from_text(text)
    audio = tts.synthesize(text)
    final = engine.apply_voice_profile(
        audio,
        profile=voice,
        emotion=emotion,
        emotion_intensity=intensity
    )
    print(f"{text[:30]}... → {emotion} ({intensity:.0%})")
```

---

## 🎬 Advanced Workflows

### Complete Production Pipeline

```python
def produce_voiceover(
    script_text,
    voice_profile_name="professional_female",
    emotion="neutral",
    add_effects=True,
    output_file="voiceover.mp3"
):
    """Complete voiceover production pipeline"""
    
    # Step 1: Normalize text
    normalized = normalizer.normalize(
        script_text,
        lowercase=False,
        remove_punctuation=False,
        strip_whitespace=True
    )
    
    # Step 2: Load or create voice profile
    if voice_profile_name in engine.get_preset_list():
        voice = engine.profile_manager.load_preset(voice_profile_name)
    else:
        voice = engine.load_saved_profile(voice_profile_name)
    
    # Step 3: Synthesize speech
    audio = tts.synthesize(normalized, engine='gtts')
    
    # Step 4: Apply voice customization
    if add_effects:
        effects_chain = [
            engine.effects.create_equalizer(bass=2, mid=1, treble=-1),
            engine.effects.create_compressor(ratio=3.0),
            engine.effects.create_reverb(room_size=0.2)
        ]
    else:
        effects_chain = None
    
    final_audio = engine.apply_voice_profile(
        audio=audio,
        profile=voice,
        emotion=emotion,
        emotion_intensity=0.7,
        effects=effects_chain
    )
    
    # Step 5: Save output
    result = writer.write(final_audio, output_file, overwrite=True)
    
    return result

# Use the pipeline
result = produce_voiceover(
    script_text="Welcome to our premium audio service!",
    voice_profile_name="professional_female",
    emotion="confident",
    add_effects=True,
    output_file="welcome_message.mp3"
)

print(f"✅ Voiceover created: {result['file_path']}")
```

### Multi-Speaker Dialogue

```python
def create_dialogue(speakers_config, dialogue_script, output_dir="dialogue"):
    """Create multi-speaker dialogue"""
    
    # Create voice profiles for each speaker
    voices = {}
    for speaker_name, config in speakers_config.items():
        voices[speaker_name] = engine.create_custom_voice(**config)
    
    # Process dialogue
    audio_segments = []
    
    for line in dialogue_script:
        speaker = line['speaker']
        text = line['text']
        emotion = line.get('emotion', 'neutral')
        
        # Synthesize
        audio = tts.synthesize(text)
        
        # Apply speaker's voice
        final = engine.apply_voice_profile(
            audio,
            profile=voices[speaker],
            emotion=emotion,
            emotion_intensity=0.7
        )
        
        audio_segments.append({
            'speaker': speaker,
            'audio': final,
            'text': text
        })
        
        # Save individual segment
        writer.write(
            final,
            f"{output_dir}/{len(audio_segments):03d}_{speaker}.mp3"
        )
    
    return audio_segments

# Configuration
speakers = {
    "narrator": {
        "name": "Narrator",
        "base_preset": "narrator_deep",
        "pitch": -2.0
    },
    "character1": {
        "name": "Hero",
        "gender": "male",
        "pitch": 0.0,
        "emotion_default": "confident"
    },
    "character2": {
        "name": "Sidekick",
        "base_preset": "friendly_assistant",
        "pitch": 2.0,
        "emotion_default": "happy"
    }
}

# Script
script = [
    {"speaker": "narrator", "text": "Once upon a time...", "emotion": "calm"},
    {"speaker": "character1", "text": "We must save the kingdom!", "emotion": "confident"},
    {"speaker": "character2", "text": "I'm right behind you!", "emotion": "excited"}
]

# Create dialogue
segments = create_dialogue(speakers, script)
```

### Batch Processing

```python
def batch_process_files(
    input_dir,
    output_dir,
    operation="transcribe",  # or "synthesize"
    voice_profile=None
):
    """Batch process multiple audio files"""
    
    import os
    from pathlib import Path
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    results = []
    
    for audio_file in input_path.glob("*.wav"):
        print(f"Processing: {audio_file.name}")
        
        try:
            if operation == "transcribe":
                # Load and transcribe
                audio = loader.load(str(audio_file))
                text_result = stt.recognize(audio)
                
                # Save transcript
                transcript_file = output_path / f"{audio_file.stem}.txt"
                with open(transcript_file, 'w') as f:
                    f.write(text_result.text)
                
                results.append({
                    "file": audio_file.name,
                    "status": "success",
                    "text": text_result.text
                })
            
            elif operation == "apply_voice":
                # Load audio
                audio = loader.load(str(audio_file))
                
                # Apply voice profile
                processed = engine.apply_voice_profile(
                    audio,
                    profile=voice_profile
                )
                
                # Save
                output_file = output_path / audio_file.name
                writer.write(processed, str(output_file))
                
                results.append({
                    "file": audio_file.name,
                    "status": "success"
                })
        
        except Exception as e:
            results.append({
                "file": audio_file.name,
                "status": "error",
                "error": str(e)
            })
    
    return results

# Batch transcribe
results = batch_process_files(
    input_dir="recordings",
    output_dir="transcripts",
    operation="transcribe"
)

# Batch voice processing
voice = engine.create_custom_voice(name="Batch Voice", pitch=1.0)
results = batch_process_files(
    input_dir="raw_audio",
    output_dir="processed_audio",
    operation="apply_voice",
    voice_profile=voice
)
```

---

## ✨ Best Practices

### 1. Resource Management

```python
# Use context managers when available
class AudioProcessor:
    def __init__(self):
        self.loader = AudioFileLoaderComponent()
        self.writer = AudioFileWriterComponent()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup resources
        pass

# Usage
with AudioProcessor() as processor:
    audio = processor.loader.load("file.wav")
    # Process audio
    processor.writer.write(audio, "output.wav")
```

### 2. Error Handling

```python
from voice_text_lib import VoiceTextException

def safe_transcribe(audio_file, max_retries=3):
    """

<function_calls>
<invoke name="artifacts">
<parameter name="command">update</parameter>
<parameter name="id">usage_guide</parameter>
<parameter name="old_str">def safe_transcribe(audio_file, max_retries=3):
    """</parameter>
<parameter name="new_str">def safe_transcribe(audio_file, max_retries=3):
    """Transcribe with error handling and retries"""
    
    for attempt in range(max_retries):
        try:
            audio = loader.load(audio_file)
            result = stt.recognize(audio)
            return result
        
        except FileNotFoundError:
            print(f"❌ File not found: {audio_file}")
            return None
        
        except VoiceTextException as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Attempt {attempt + 1} failed, retrying...")
                continue
            else:
                print(f"❌ Failed after {max_retries} attempts: {e}")
                return None
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

# Usage
result = safe_transcribe("audio.wav")
if result:
    print(f"Success: {result.text}")
```

### 3. Performance Optimization

```python
# Cache frequently used profiles
class VoiceProfileCache:
    def __init__(self, engine):
        self.engine = engine
        self.cache = {}
    
    def get_profile(self, profile_name):
        if profile_name not in self.cache:
            if profile_name in self.engine.get_preset_list():
                self.cache[profile_name] = self.engine.profile_manager.load_preset(profile_name)
            else:
                self.cache[profile_name] = self.engine.load_saved_profile(profile_name)
        
        return self.cache[profile_name]

# Usage
cache = VoiceProfileCache(engine)
voice1 = cache.get_profile("professional_male")  # Loaded from disk
voice2 = cache.get_profile("professional_male")  # Retrieved from cache
```

### 4. Logging Best Practices

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_with_logging(audio_file):
    logger.info(f"Starting processing: {audio_file}")
    
    try:
        audio = loader.load(audio_file)
        logger.info(f"Loaded audio: {audio.duration:.2f}s")
        
        result = stt.recognize(audio)
        logger.info(f"Transcribed: {len(result.text)} characters")
        
        return result
    
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        raise

# Check trace logs
def analyze_trace_logs():
    """Analyze LLM interaction logs"""
    import json
    
    with open('llm_interaction.log', 'r') as f:
        for line in f:
            trace = json.loads(line)
            print(f"{trace['component']} - {trace['event']}: {trace['duration_ms']:.2f}ms")
```

---

## 🔧 Error Handling

### Common Error Scenarios

```python
# 1. File not found
try:
    audio = loader.load("nonexistent.wav")
except VoiceTextException as e:
    print(f"File error: {e}")

# 2. Invalid format
try:
    audio = loader.load("image.jpg")
except VoiceTextException as e:
    print(f"Format error: {e}")

# 3. Invalid voice parameters
try:
    voice = engine.create_custom_voice(
        name="Invalid",
        pitch=50.0  # Out of range
    )
except VoiceTextException as e:
    print(f"Validation error: {e}")

# 4. API errors
try:
    result = stt.recognize(audio, engine='google')
except Exception as e:
    print(f"API error: {e}")

# 5. Permission errors
try:
    writer.write(audio, "/root/protected.wav")
except PermissionError as e:
    print(f"Permission denied: {e}")
```

### Comprehensive Error Handler

```python
def robust_voice_pipeline(
    input_file,
    output_file,
    voice_profile_name,
    fallback_engine='pyttsx3'
):
    """Production-ready pipeline with comprehensive error handling"""
    
    try:
        # Load audio
        try:
            audio = loader.load(input_file)
        except FileNotFoundError:
            logger.error(f"Input file not found: {input_file}")
            return {"status": "error", "message": "File not found"}
        except VoiceTextException as e:
            logger.error(f"Invalid audio file: {e}")
            return {"status": "error", "message": str(e)}
        
        # Transcribe
        try:
            text = stt.recognize(audio, engine='google')
        except Exception as e:
            logger.warning(f"Primary STT failed, trying {fallback_engine}: {e}")
            try:
                text = stt.recognize(audio, engine=fallback_engine)
            except Exception as e2:
                logger.error(f"All STT engines failed: {e2}")
                return {"status": "error", "message": "Transcription failed"}
        
        # Load voice profile
        try:
            if voice_profile_name in engine.get_preset_list():
                voice = engine.profile_manager.load_preset(voice_profile_name)
            else:
                voice = engine.load_saved_profile(voice_profile_name)
        except VoiceTextException as e:
            logger.warning(f"Profile load failed, using default: {e}")
            voice = engine.profile_manager.load_preset("professional_male")
        
        # Synthesize
        try:
            audio_out = tts.synthesize(text, engine='gtts')
        except Exception as e:
            logger.warning(f"Primary TTS failed, trying {fallback_engine}: {e}")
            try:
                audio_out = tts.synthesize(text, engine=fallback_engine)
            except Exception as e2:
                logger.error(f"All TTS engines failed: {e2}")
                return {"status": "error", "message": "Synthesis failed"}
        
        # Apply profile
        try:
            final = engine.apply_voice_profile(audio_out, profile=voice)
        except Exception as e:
            logger.warning(f"Voice profile application failed, using original: {e}")
            final = audio_out
        
        # Save
        try:
            result = writer.write(final, output_file, overwrite=True)
            logger.info(f"Success: {result['file_path']}")
            return {"status": "success", "file": result['file_path']}
        except Exception as e:
            logger.error(f"Failed to save output: {e}")
            return {"status": "error", "message": "Save failed"}
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
```

---

## ⚡ Performance Optimization

### Async Processing

```python
import asyncio

async def process_audio_async(audio_file):
    """Async audio processing"""
    loop = asyncio.get_event_loop()
    
    # Run blocking operations in thread pool
    audio = await loop.run_in_executor(None, loader.load, audio_file)
    result = await loop.run_in_executor(None, stt.recognize, audio)
    
    return result

# Process multiple files concurrently
async def batch_process_async(audio_files):
    tasks = [process_audio_async(f) for f in audio_files]
    results = await asyncio.gather(*tasks)
    return results

# Usage
files = ["file1.wav", "file2.wav", "file3.wav"]
results = asyncio.run(batch_process_async(files))
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib

class CachedVoiceEngine:
    def __init__(self):
        self.engine = VoiceCustomizationEngine()
        self.audio_cache = {}
    
    def get_cache_key(self, text, profile_id, emotion):
        """Generate cache key"""
        data = f"{text}:{profile_id}:{emotion}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def synthesize_cached(self, text, profile, emotion="neutral"):
        """Synthesize with caching"""
        cache_key = self.get_cache_key(text, profile.profile_id, emotion)
        
        if cache_key in self.audio_cache:
            print("✅ Cache hit")
            return self.audio_cache[cache_key]
        
        print("⚠️  Cache miss, synthesizing...")
        audio = tts.synthesize(text)
        final = self.engine.apply_voice_profile(
            audio,
            profile=profile,
            emotion=emotion
        )
        
        self.audio_cache[cache_key] = final
        return final

# Usage
cached_engine = CachedVoiceEngine()
voice = engine.create_custom_voice(name="Test")

audio1 = cached_engine.synthesize_cached("Hello", voice)  # Cache miss
audio2 = cached_engine.synthesize_cached("Hello", voice)  # Cache hit
```

---

For complete API reference, see documentation files.
For installation help, see [SETUP.md](SETUP.md).
For project overview, see [README.md](README.md).

---

**Happy coding! 🎉**</parameter>
