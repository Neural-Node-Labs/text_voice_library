# Voice-Text Conversion Library with Enhanced Voice Customization

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](/)
[![Component-Based](https://img.shields.io/badge/architecture-CBD-orange.svg)](/)

A professional-grade Python library for bidirectional voice-text conversion with advanced voice customization capabilities. Built using Component-Based Development (CBD) methodology with 100% test coverage.

---

## 🌟 Features

### Core Capabilities
- ✅ **Speech-to-Text (STT)**: Convert audio to text using multiple engines
- ✅ **Text-to-Speech (TTS)**: Synthesize natural-sounding speech from text
- ✅ **Audio Processing**: Load, process, and save audio files securely
- ✅ **Text Normalization**: Clean and preprocess text for optimal results

### Advanced Voice Customization
- 🎤 **Voice Profiles**: Create and manage custom voice profiles
- 🎛️ **Audio Effects**: Apply professional audio effects (reverb, echo, EQ, etc.)
- 🔄 **Voice Transformation**: Change pitch, formant, and timbre
- 😊 **Emotional Tones**: Add emotional expression to synthesized speech
- 💾 **Profile Persistence**: Save and load custom voice configurations

### Quality & Security
- 🔒 **Security-First**: Path traversal prevention, input sanitization
- 📊 **100% Test Coverage**: Comprehensive test suite with 99 test cases
- 📝 **Dual Logging**: System errors + LLM interaction audit trail
- ⚡ **Performance**: Optimized for sub-3ms text processing
- 🏗️ **Component-Based**: Modular architecture with clear contracts

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Basic Usage](#-basic-usage)
- [Advanced Features](#-advanced-features)
- [Documentation](#-documentation)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```python
from voice_text_lib import (
    AudioFileLoaderComponent,
    SpeechRecognitionComponent,
    TTSEngineComponent,
    AudioFileWriterComponent
)
from enhanced_voice_profiles import VoiceCustomizationEngine

# Initialize components
stt = SpeechRecognitionComponent()
tts = TTSEngineComponent()
loader = AudioFileLoaderComponent()
engine = VoiceCustomizationEngine()

# Voice-to-Text
audio = loader.load("speech.wav")
text = stt.recognize(audio, engine='google', language='en-US')
print(f"Transcribed: {text.text}")

# Text-to-Voice with Custom Profile
voice = engine.create_custom_voice(
    name="Professional Voice",
    base_preset="professional_male",
    pitch=-1.0,
    speed=0.95
)

audio_output = tts.synthesize(text, engine='gtts')
final = engine.apply_voice_profile(
    audio=audio_output,
    profile=voice,
    emotion="confident",
    emotion_intensity=0.8
)

# Save result
writer = AudioFileWriterComponent()
writer.write(final, "output.mp3")
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-text-library.git
cd voice-text-library

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from voice_text_lib import *; print('✅ Installation successful!')"
```

### Full Installation (with all engines)

```bash
# Install all optional dependencies
pip install -r requirements-full.txt
```

See [SETUP.md](SETUP.md) for detailed installation instructions.

---

## 💡 Basic Usage

### 1. Speech Recognition (Voice → Text)

```python
from voice_text_lib import AudioFileLoaderComponent, SpeechRecognitionComponent

# Load audio
loader = AudioFileLoaderComponent()
audio = loader.load("recording.wav")

# Recognize speech
stt = SpeechRecognitionComponent(api_key="YOUR_API_KEY")
result = stt.recognize(audio, engine='google', language='en-US')

print(f"Text: {result.text}")
print(f"Confidence: {result.confidence:.2%}")
```

### 2. Text-to-Speech (Text → Voice)

```python
from voice_text_lib import TextNormalizerComponent, TTSEngineComponent, AudioFileWriterComponent

# Prepare text
normalizer = TextNormalizerComponent()
text = normalizer.normalize("Hello! Welcome to our system.", lowercase=False)

# Synthesize speech
tts = TTSEngineComponent(api_key="YOUR_API_KEY")
audio = tts.synthesize(text, engine='gtts', voice='en-US-JennyNeural')

# Save to file
writer = AudioFileWriterComponent()
writer.write(audio, "greeting.mp3")
```

### 3. Custom Voice Profile

```python
from enhanced_voice_profiles import VoiceCustomizationEngine

engine = VoiceCustomizationEngine()

# Create custom voice
my_voice = engine.create_custom_voice(
    name="My Podcast Voice",
    base_preset="professional_female",
    pitch=0.5,
    speed=1.05,
    emotion_default="confident"
)

# Apply to audio with effects
effects = [
    engine.effects.create_reverb(room_size=0.3),
    engine.effects.create_equalizer(bass=2, treble=-1)
]

final_audio = engine.apply_voice_profile(
    audio=tts_audio,
    profile=my_voice,
    emotion="happy",
    emotion_intensity=0.7,
    effects=effects
)
```

See [USAGE.md](USAGE.md) for comprehensive usage guide.

---

## 🎨 Advanced Features

### Voice Profiles

Create professional voice profiles with fine-grained control:

```python
voice = engine.create_custom_voice(
    name="Documentary Narrator",
    gender="male",
    pitch=-3.0,          # Lower pitch
    speed=0.85,          # Slower pace
    volume=1.1,          # Slightly louder
    accent="british",    # British accent
    age_range="adult",   # Adult voice
    emotion_default="calm"
)
```

**Available Presets:**
- `professional_male` - Business/corporate male voice
- `professional_female` - Business/corporate female voice
- `friendly_assistant` - Warm, helpful voice
- `narrator_deep` - Deep, authoritative narrator
- `child_voice` - Child-like voice
- `elderly_wise` - Mature, wise voice

### Audio Effects

Apply studio-quality effects:

```python
effects = [
    # Reverb (concert hall)
    engine.effects.create_reverb(room_size=0.8, damping=0.4),
    
    # Echo (slapback delay)
    engine.effects.create_echo(delay_ms=150, feedback=0.35),
    
    # Equalizer (warm voice)
    engine.effects.create_equalizer(bass=3, mid=1, treble=-2)
]

processed = engine.effects.apply_effects(audio, effects)
```

**Available Effects:**
- Reverb (room acoustics)
- Echo (delayed repetition)
- Equalizer (frequency adjustment)
- Chorus (thickening)
- Compressor (dynamic range)
- Distortion (saturation)
- Noise Gate (background removal)
- Pitch Shift
- Time Stretch

### Voice Transformation

Transform voice characteristics:

```python
transformer = engine.transformer

# Male to Female
audio_female = transformer.transform_voice(
    male_audio, 
    transformer.male_to_female()
)

# Female to Male
audio_male = transformer.transform_voice(
    female_audio,
    transformer.female_to_male()
)

# Robot Voice
audio_robot = transformer.transform_voice(
    audio,
    transformer.robot_voice()
)

# Custom transformation
custom = VoiceTransform(
    pitch_shift=2.5,
    formant_shift=1.08,
    timbre_morph=0.3
)
```

### Emotional Tones

Add emotional expression:

```python
emotions = {
    "neutral": 1.0,
    "happy": 0.8,
    "sad": 0.6,
    "angry": 0.7,
    "excited": 0.9,
    "calm": 0.7,
    "fearful": 0.5,
    "confident": 0.8
}

for emotion, intensity in emotions.items():
    result = engine.apply_voice_profile(
        audio=base_audio,
        profile=voice,
        emotion=emotion,
        emotion_intensity=intensity
    )
```

---

## 📚 Documentation

### Core Documentation
- [SETUP.md](SETUP.md) - Detailed installation and configuration
- [USAGE.md](USAGE.md) - Comprehensive usage guide with examples
- [API_REFERENCE.md](docs/API_REFERENCE.md) - Complete API documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture details

### Specialized Guides
- [Voice Profiles Guide](docs/VOICE_PROFILES.md)
- [Audio Effects Guide](docs/AUDIO_EFFECTS.md)
- [Security Best Practices](docs/SECURITY.md)
- [Performance Tuning](docs/PERFORMANCE.md)

### Development
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [TESTING.md](docs/TESTING.md) - Testing guide
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

## 🎯 Examples

### Example 1: Podcast Production

```python
# Create podcast host voice
host_voice = engine.create_custom_voice(
    name="Podcast Host",
    base_preset="professional_female",
    pitch=0.5,
    speed=1.0,
    emotion_default="friendly"
)

# Process episode script
for segment in script_segments:
    audio = tts.synthesize(segment.text)
    
    # Apply voice profile with appropriate emotion
    final = engine.apply_voice_profile(
        audio=audio,
        profile=host_voice,
        emotion=segment.emotion,
        effects=[
            engine.effects.create_reverb(room_size=0.2),
            engine.effects.create_equalizer(bass=2)
        ]
    )
    
    save_segment(final, segment.number)
```

### Example 2: Multilingual Translation Service

```python
# Transcribe in source language
source_audio = loader.load("french_speech.wav")
french_text = stt.recognize(source_audio, language='fr-FR')

# Translate (using external translation API)
english_text = translate(french_text.text, source='fr', target='en')

# Synthesize in target language
english_voice = engine.create_custom_voice(
    name="English Voice",
    language="en-US",
    accent="american"
)

english_audio = tts.synthesize(english_text, language='en-US')
final = engine.apply_voice_profile(english_audio, english_voice)
```

### Example 3: Audiobook Generation

```python
# Create narrator voice
narrator = engine.create_custom_voice(
    name="Audiobook Narrator",
    base_preset="narrator_deep",
    pitch=-2.0,
    speed=0.9,
    emotion_default="calm"
)

# Process book chapters
for chapter in book.chapters:
    for paragraph in chapter.paragraphs:
        # Detect emotion from text
        emotion = analyze_sentiment(paragraph.text)
        
        audio = tts.synthesize(paragraph.text)
        final = engine.apply_voice_profile(
            audio=audio,
            profile=narrator,
            emotion=emotion,
            emotion_intensity=0.6
        )
        
        save_audio_chunk(final, chapter.number, paragraph.number)
```

More examples in [examples/](examples/) directory.

---

## 🏗️ Architecture

### Component-Based Design

The library follows Component-Based Development (CBD) methodology:

```
┌─────────────────────────────────────────────────────────┐
│                 Application Layer                       │
├─────────────────────────────────────────────────────────┤
│  VoiceCustomizationEngine (High-Level API)              │
├─────────────────────────────────────────────────────────┤
│                 Component Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Voice Profile│  │ Audio Effects│  │ Voice Transform│ │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ STT Engine   │  │ TTS Engine   │  │ Emotion Engine│ │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│                 Adaptor Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │FileSystem    │  │ Audio I/O    │  │ Signal DSP   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Infrastructure Layer                       │
│  Logging | Error Handling | Security | Storage         │
└─────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Atomicity**: One component = One logical function
2. **Contracts**: Clear IN/OUT/ERROR schemas for each component
3. **Decoupling**: Components communicate via well-defined interfaces
4. **Traceability**: Comprehensive logging with trace IDs
5. **Security**: Input validation and sanitization at every layer

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test suite
pytest tests/test_voice_text_lib.py -v
pytest tests/test_enhanced_voice_profiles.py -v

# Run performance tests
pytest tests/test_performance.py -v
```

### Test Coverage

- **Total Test Cases**: 99
- **Coverage**: 100%
- **Components Tested**: 18/18

### Test Categories

- ✅ Unit Tests (positive cases)
- ✅ Unit Tests (negative cases)
- ✅ Integration Tests
- ✅ Security Tests
- ✅ Performance Tests

See [TESTING.md](docs/TESTING.md) for detailed testing guide.

---

## 🎮 Interactive Demos

### Base Library Demo

```bash
python demo.py
```

**Features:**
- Text normalization
- Text-to-speech synthesis
- Speech-to-text recognition
- Secure file operations
- Error handling
- Logging analysis
- Performance metrics

### Enhanced Voice Demo

```bash
python demo_enhanced_voice.py
```

**Features:**
- Preset voice profiles
- Custom voice creation
- Audio effects processing
- Voice transformation
- Emotional tone application
- Complete pipeline
- Profile management
- Voice comparison

---

## 📊 Performance

### Benchmarks

| Operation | Target | Typical | Status |
|-----------|--------|---------|--------|
| Text Normalization | <3ms | 0.8ms | ✅ |
| File Load (1MB) | <50ms | 35ms | ✅ |
| File Write (1MB) | <50ms | 42ms | ✅ |
| STT (5s audio) | <2s | 1.3s | ✅ |
| TTS (100 chars) | <1s | 0.7s | ✅ |
| Apply Effect | <50ms | 30ms | ✅ |
| Voice Transform | <200ms | 145ms | ✅ |

---

## 🔧 Configuration

### Environment Variables

```bash
# API Keys
export GOOGLE_SPEECH_API_KEY="your-key-here"
export AZURE_SPEECH_KEY="your-key-here"
export AZURE_SPEECH_REGION="your-region"

# Storage Paths
export VOICE_PROFILES_DIR="./voice_profiles"
export AUDIO_OUTPUT_DIR="./audio_output"

# Logging
export LOG_LEVEL="INFO"
export ENABLE_TRACE_LOGGING="true"
```

### Configuration File

Create `config.yaml`:

```yaml
# Speech Recognition
speech_recognition:
  default_engine: google
  default_language: en-US
  timeout: 10

# Text-to-Speech
text_to_speech:
  default_engine: gtts
  default_voice: en-US-Standard-A
  sample_rate: 22050

# Voice Profiles
voice_profiles:
  storage_path: ./voice_profiles
  auto_save: true

# Audio Effects
audio_effects:
  default_sample_rate: 44100
  default_format: wav

# Logging
logging:
  level: INFO
  system_log: system.log
  interaction_log: llm_interaction.log
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow CBD methodology for new components
4. Write tests (maintain 100% coverage)
5. Update documentation
6. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/voice-text-library.git
cd voice-text-library

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Check code quality
flake8 .
black --check .
mypy .
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built using Component-Based Development (CBD) methodology
- Inspired by industry-standard voice processing pipelines
- Special thanks to the open-source community

---

## 📞 Support

- **Documentation**: [Full documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/voice-text-library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/voice-text-library/discussions)
- **Email**: support@yourproject.com

---

## 🗺️ Roadmap

### Version 1.1 (Upcoming)
- [ ] Real-time audio streaming
- [ ] WebSocket support for live transcription
- [ ] Additional language support
- [ ] Cloud storage integration

### Version 1.2 (Planned)
- [ ] Voice cloning capabilities
- [ ] Neural voice synthesis
- [ ] Advanced noise reduction
- [ ] Mobile SDK (iOS/Android)

### Version 2.0 (Future)
- [ ] Multi-speaker diarization
- [ ] Emotion detection from speech
- [ ] Real-time voice effects
- [ ] API service deployment

---

## 📈 Project Stats

- **Lines of Code**: ~2,800
- **Components**: 18
- **Test Cases**: 99
- **Test Coverage**: 100%
- **Documentation Pages**: 25+
- **Code Examples**: 50+

---

**Made with ❤️ using Component-Based Development**

*For detailed usage instructions, see [USAGE.md](USAGE.md)*  
*For installation guide, see [SETUP.md](SETUP.md)*
