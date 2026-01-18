# Setup & Installation Guide

Complete guide for installing and configuring the Voice-Text Conversion Library.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Dependency Installation](#dependency-installation)
4. [Configuration](#configuration)
5. [API Keys Setup](#api-keys-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for library + dependencies
- **Internet**: Required for cloud STT/TTS services

### Recommended Requirements

- **Python**: 3.10+
- **RAM**: 16GB (for processing large audio files)
- **CPU**: Multi-core processor for faster processing
- **GPU**: Optional, for neural voice synthesis

### Check Python Version

```bash
python --version
# Should output: Python 3.8.x or higher

# Or
python3 --version
```

---

## 📦 Installation Methods

### Method 1: Basic Installation (Recommended for Testing)

Quick setup with core functionality and mock implementations:

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-text-library.git
cd voice-text-library

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install core dependencies
pip install -r requirements-basic.txt
```

**What you get:**
- ✅ All component contracts
- ✅ Mock STT/TTS implementations
- ✅ Voice profile management
- ✅ Audio effects (mock DSP)
- ✅ File I/O operations
- ✅ Complete test suite
- ✅ Interactive demos

### Method 2: Standard Installation (For Production)

Full installation with real STT/TTS engines:

```bash
# After cloning and creating venv...

# Install standard dependencies
pip install -r requirements.txt
```

**What you get:**
- ✅ Everything from Basic +
- ✅ Google Speech Recognition
- ✅ gTTS (Google Text-to-Speech)
- ✅ pyttsx3 (Offline TTS)
- ✅ Basic audio processing (pydub)

### Method 3: Full Installation (All Features)

Complete installation with advanced features:

```bash
# After cloning and creating venv...

# Install all dependencies
pip install -r requirements-full.txt
```

**What you get:**
- ✅ Everything from Standard +
- ✅ Azure Cognitive Services
- ✅ OpenAI Whisper
- ✅ Advanced audio effects (pedalboard)
- ✅ Voice transformation (librosa)
- ✅ Formant analysis (praat-parselmouth)

### Method 4: Development Installation

For contributing to the project:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

**What you get:**
- ✅ Everything from Full +
- ✅ Testing tools (pytest, coverage)
- ✅ Code quality tools (flake8, black, mypy)
- ✅ Documentation tools (sphinx)

---

## 📚 Dependency Installation

### Core Dependencies (requirements-basic.txt)

```txt
# Core Python libraries
pathlib>=1.0.1
dataclasses>=0.6; python_version < '3.7'
typing-extensions>=4.0.0

# JSON/YAML handling
pyyaml>=6.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
```

### Standard Dependencies (requirements.txt)

```txt
# Include all from requirements-basic.txt
-r requirements-basic.txt

# Audio I/O
pyaudio>=0.2.11
pydub>=0.25.1
soundfile>=0.11.0

# Speech Recognition
SpeechRecognition>=3.10.0

# Text-to-Speech
gTTS>=2.3.0
pyttsx3>=2.90

# Audio playback
pygame>=2.1.0

# Signal processing
numpy>=1.21.0
scipy>=1.7.0
```

### Full Dependencies (requirements-full.txt)

```txt
# Include all from requirements.txt
-r requirements.txt

# Cloud Speech Services
azure-cognitiveservices-speech>=1.24.0
google-cloud-speech>=2.16.0

# Advanced STT
openai-whisper>=20230314

# Advanced Audio Processing
librosa>=0.10.0
pedalboard>=0.7.0
pyrubberband>=0.3.0
noisereduce>=2.0.0

# Voice Analysis
praat-parselmouth>=0.4.3
resemblyzer>=0.1.1.dev0

# Advanced TTS
TTS>=0.10.0  # Coqui TTS

# File format support
ffmpeg-python>=0.2.0
```

### Development Dependencies (requirements-dev.txt)

```txt
# Include all from requirements-full.txt
-r requirements-full.txt

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-asyncio>=0.20.0

# Code Quality
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
pylint>=2.16.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.2.0
sphinx-autodoc-typehints>=1.22.0

# Development Tools
ipython>=8.0.0
jupyter>=1.0.0
```

---

## ⚙️ Configuration

### 1. Directory Structure Setup

```bash
# Create required directories
mkdir -p voice_profiles
mkdir -p audio_output
mkdir -p logs
mkdir -p cache
mkdir -p config

# Set permissions (Linux/macOS)
chmod 755 voice_profiles audio_output logs
```

### 2. Environment Variables

Create a `.env` file in the project root:

```bash
# .env file

# API Keys
GOOGLE_SPEECH_API_KEY=your_google_api_key_here
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus
OPENAI_API_KEY=your_openai_key_here

# Storage Paths
VOICE_PROFILES_DIR=./voice_profiles
AUDIO_OUTPUT_DIR=./audio_output
CACHE_DIR=./cache

# Logging
LOG_LEVEL=INFO
ENABLE_TRACE_LOGGING=true
SYSTEM_LOG_PATH=./logs/system.log
INTERACTION_LOG_PATH=./logs/llm_interaction.log

# Audio Settings
DEFAULT_SAMPLE_RATE=44100
DEFAULT_AUDIO_FORMAT=wav

# Performance
MAX_WORKERS=4
CACHE_ENABLED=true
CACHE_SIZE_MB=100
```

### 3. Configuration File

Create `config/settings.yaml`:

```yaml
# Voice-Text Library Configuration

# Speech Recognition Settings
speech_recognition:
  default_engine: google  # google, azure, whisper, sphinx
  default_language: en-US
  timeout_seconds: 10
  retry_attempts: 3
  
  # Engine-specific settings
  google:
    use_enhanced: true
    model: latest_long
  
  azure:
    endpoint: https://{region}.api.cognitive.microsoft.com
    profanity_filter: masked
  
  whisper:
    model_size: base  # tiny, base, small, medium, large
    device: cpu       # cpu or cuda

# Text-to-Speech Settings
text_to_speech:
  default_engine: gtts  # gtts, pyttsx3, azure, elevenlabs
  default_voice: en-US-Standard-A
  default_speed: 1.0
  default_pitch: 0.0
  sample_rate: 22050
  
  # Engine-specific settings
  gtts:
    slow: false
    lang: en
  
  pyttsx3:
    rate: 150
    volume: 1.0
  
  azure:
    voice_name: en-US-JennyNeural
    style: default  # default, cheerful, sad, angry, etc.

# Voice Profile Settings
voice_profiles:
  storage_path: ./voice_profiles
  auto_save: true
  compression: false
  max_profiles: 100

# Audio Processing
audio:
  input_formats: [wav, mp3, flac, ogg, m4a]
  output_formats: [wav, mp3]
  default_format: wav
  sample_rate: 44100
  channels: 1  # mono
  bit_depth: 16

# Audio Effects
effects:
  reverb:
    default_room_size: 0.5
    default_damping: 0.5
  
  echo:
    default_delay_ms: 500
    default_feedback: 0.3
  
  equalizer:
    bands: 3  # bass, mid, treble
    range_db: [-12, 12]

# Security Settings
security:
  enable_path_validation: true
  allowed_base_dirs: 
    - ./voice_profiles
    - ./audio_output
    - ./cache
  max_file_size_mb: 100
  allowed_extensions: [wav, mp3, json, yaml]

# Performance Settings
performance:
  max_workers: 4
  cache_enabled: true
  cache_size_mb: 100
  cache_ttl_hours: 24

# Logging Settings
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
  system_log:
    enabled: true
    path: ./logs/system.log
    max_size_mb: 50
    backup_count: 5
  
  interaction_log:
    enabled: true
    path: ./logs/llm_interaction.log
    format: json
    max_size_mb: 50
    backup_count: 5
```

### 4. Load Configuration in Python

```python
import yaml
import os
from pathlib import Path

def load_config():
    """Load configuration from YAML file and environment"""
    
    # Load from YAML
    config_path = Path("config/settings.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Override with environment variables
    if os.getenv("GOOGLE_SPEECH_API_KEY"):
        config['api_keys'] = config.get('api_keys', {})
        config['api_keys']['google'] = os.getenv("GOOGLE_SPEECH_API_KEY")
    
    if os.getenv("AZURE_SPEECH_KEY"):
        config['api_keys']['azure_key'] = os.getenv("AZURE_SPEECH_KEY")
        config['api_keys']['azure_region'] = os.getenv("AZURE_SPEECH_REGION")
    
    return config

# Usage
config = load_config()
```

---

## 🔑 API Keys Setup

### Google Cloud Speech-to-Text

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Cloud Speech-to-Text API"
4. Create credentials (API Key or Service Account)
5. Download credentials JSON

```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export GOOGLE_SPEECH_API_KEY="your-api-key"
```

### Azure Cognitive Services

1. Go to [Azure Portal](https://portal.azure.com)
2. Create "Speech Services" resource
3. Get Key and Region from resource dashboard

```bash
# Set environment variables
export AZURE_SPEECH_KEY="your-subscription-key"
export AZURE_SPEECH_REGION="eastus"  # or your region
```

### OpenAI Whisper (API)

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create API key

```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-api-key"
```

**Note**: Whisper can also run locally without API key using the open-source model.

### ElevenLabs (Optional)

1. Go to [ElevenLabs](https://elevenlabs.io)
2. Sign up and get API key

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

---

## ✅ Verification

### 1. Check Installation

```bash
# Check Python packages
pip list | grep -i speech
pip list | grep -i audio
pip list | grep -i tts

# Verify imports
python -c "from voice_text_lib import *; print('✅ Base library OK')"
python -c "from enhanced_voice_profiles import *; print('✅ Enhanced library OK')"
```

### 2. Run Tests

```bash
# Run all tests
pytest -v

# Check specific components
pytest tests/test_voice_text_lib.py::TestAudioFileLoaderComponent -v
pytest tests/test_enhanced_voice_profiles.py::TestVoiceProfileComponent -v

# Check coverage
pytest --cov=. --cov-report=term-missing
```

### 3. Run Demos

```bash
# Base library demo
python demo.py

# Enhanced voice demo
python demo_enhanced_voice.py
```

### 4. Verify API Connections

```python
# test_api_connections.py

from voice_text_lib import SpeechRecognitionComponent, TTSEngineComponent
import os

def test_google_stt():
    """Test Google Speech Recognition"""
    if not os.getenv("GOOGLE_SPEECH_API_KEY"):
        print("⚠️  Google API key not set")
        return False
    
    try:
        stt = SpeechRecognitionComponent()
        # Test with sample audio
        print("✅ Google STT connection OK")
        return True
    except Exception as e:
        print(f"❌ Google STT error: {e}")
        return False

def test_azure_tts():
    """Test Azure Text-to-Speech"""
    if not os.getenv("AZURE_SPEECH_KEY"):
        print("⚠️  Azure API key not set")
        return False
    
    try:
        tts = TTSEngineComponent(
            api_key=os.getenv("AZURE_SPEECH_KEY")
        )
        print("✅ Azure TTS connection OK")
        return True
    except Exception as e:
        print(f"❌ Azure TTS error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API Connections...\n")
    test_google_stt()
    test_azure_tts()
```

Run verification:

```bash
python test_api_connections.py
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Error: No module named 'pyaudio'

**Problem**: PyAudio installation failed

**Solution (Windows)**:
```bash
# Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl
```

**Solution (macOS)**:
```bash
brew install portaudio
pip install pyaudio
```

**Solution (Linux)**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

#### 2. FFmpeg Not Found

**Problem**: Audio format conversion fails

**Solution (Windows)**:
```bash
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

**Solution (macOS)**:
```bash
brew install ffmpeg
```

**Solution (Linux)**:
```bash
sudo apt-get install ffmpeg
```

#### 3. Permission Denied on File Operations

**Problem**: Cannot write to output directories

**Solution**:
```bash
# Check permissions
ls -la voice_profiles/
ls -la audio_output/

# Fix permissions
chmod 755 voice_profiles audio_output logs

# Or change owner
sudo chown -R $USER:$USER voice_profiles audio_output logs
```

#### 4. API Key Not Working

**Problem**: Authentication fails for cloud services

**Solution**:
```bash
# Verify environment variables are set
echo $GOOGLE_SPEECH_API_KEY
echo $AZURE_SPEECH_KEY

# Check .env file is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_SPEECH_API_KEY'))"

# Verify API key format
# Google: Should be 39 characters
# Azure: Should be 32 hexadecimal characters
```

#### 5. Memory Error with Large Audio Files

**Problem**: Out of memory when processing

**Solution**:
```python
# Process in chunks
from voice_text_lib import AudioFileLoaderComponent

loader = AudioFileLoaderComponent()

# Instead of loading entire file
# audio = loader.load("large_file.wav")

# Load in chunks (implement chunking)
chunk_size = 10  # seconds
for i, chunk in enumerate(load_chunks("large_file.wav", chunk_size)):
    process_chunk(chunk, i)
```

#### 6. Test Failures

**Problem**: Some tests fail after installation

**Solution**:
```bash
# Clear cache
pytest --cache-clear

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for conflicting packages
pip check

# Run tests with verbose output
pytest -vv --tb=long
```

### Platform-Specific Issues

#### Windows

```bash
# If you get SSL errors
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# If you get encoding errors
set PYTHONIOENCODING=utf-8
```

#### macOS

```bash
# If you get compiler errors
xcode-select --install

# If you get library not found errors
export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH
```

#### Linux

```bash
# If you get audio device errors
sudo usermod -a -G audio $USER
# Then logout and login

# If you get dependency errors
sudo apt-get install build-essential python3-dev
```

---

## 📞 Getting Help

If you encounter issues not covered here:

1. **Check Documentation**: See [USAGE.md](USAGE.md) and [README.md](README.md)
2. **Search Issues**: [GitHub Issues](https://github.com/yourusername/voice-text-library/issues)
3. **Ask Community**: [GitHub Discussions](https://github.com/yourusername/voice-text-library/discussions)
4. **Report Bug**: Create new issue with:
   - Python version
   - OS and version
   - Full error traceback
   - Steps to reproduce

---

## 🎯 Next Steps

After successful installation:

1. Read [USAGE.md](USAGE.md) for usage examples
2. Run interactive demos to explore features
3. Review [examples/](examples/) directory
4. Join community discussions

---

**Installation complete! 🎉**

For usage instructions, see [USAGE.md](USAGE.md)
