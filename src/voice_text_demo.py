"""
Voice-Text Conversion Library - Interactive Demo
Demonstrates all components with real-world scenarios
"""

import os
import sys
from pathlib import Path
import json

# Import library components
try:
    from voice_text_lib import (
        AudioFileLoaderComponent,
        TextNormalizerComponent,
        AudioFileWriterComponent,
        SpeechRecognitionComponent,
        TTSEngineComponent,
        AudioData,
        TextData,
        VoiceTextException,
        logger
    )
except ImportError:
    print("Error: voice_text_lib.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

# ============================================================================
# DEMO CONFIGURATION
# ============================================================================

class DemoConfig:
    """Configuration for demo scenarios"""
    
    # Directories
    INPUT_DIR = Path("./demo_audio_input")
    OUTPUT_DIR = Path("./demo_audio_output")
    
    # Sample texts for TTS
    SAMPLE_TEXTS = [
        "Hello! This is a demonstration of the voice text conversion library.",
        "The system supports multiple languages and speech engines.",
        "Component-based development ensures modularity and reliability."
    ]
    
    # Test engines
    STT_ENGINES = ['google', 'azure', 'whisper']
    TTS_ENGINES = ['gtts', 'pyttsx3', 'azure']
    
    @classmethod
    def setup(cls):
        """Create demo directories"""
        cls.INPUT_DIR.mkdir(exist_ok=True, parents=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================================
# DEMO SCENARIOS
# ============================================================================

class VoiceTextDemo:
    """Interactive demo application"""
    
    def __init__(self):
        self.config = DemoConfig()
        self.config.setup()
        
        # Initialize components
        self.loader = AudioFileLoaderComponent()
        self.normalizer = TextNormalizerComponent()
        self.writer = AudioFileWriterComponent(base_dir=str(self.config.OUTPUT_DIR))
        self.stt = SpeechRecognitionComponent()
        self.tts = TTSEngineComponent()
    
    def print_header(self, title):
        """Print formatted section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def demo_text_normalization(self):
        """Demonstrate text normalization features"""
        self.print_header("DEMO 1: Text Normalization")
        
        test_cases = [
            {
                "input": "  HELLO,   WORLD!   How   are   YOU?  ",
                "options": {"lowercase": True, "remove_punctuation": True, "strip_whitespace": True},
                "description": "Lowercase + Remove Punctuation + Strip Whitespace"
            },
            {
                "input": "The Quick Brown Fox Jumps Over The Lazy Dog!",
                "options": {"lowercase": True, "remove_punctuation": False, "strip_whitespace": True},
                "description": "Lowercase Only"
            },
            {
                "input": "Email: user@example.com, Phone: (555) 123-4567",
                "options": {"lowercase": False, "remove_punctuation": True, "strip_whitespace": True},
                "description": "Remove Punctuation (preserves text)"
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"Test Case {i}: {test['description']}")
            print(f"Input:  '{test['input']}'")
            
            result = self.normalizer.normalize(test['input'], **test['options'])
            
            print(f"Output: '{result.text}'")
            print(f"Stats:  Original: {result.metadata['original_length']} chars → "
                  f"Final: {result.metadata['final_length']} chars "
                  f"({round((1 - result.metadata['final_length']/result.metadata['original_length']) * 100, 1)}% reduction)")
            print()
    
    def demo_text_to_speech(self):
        """Demonstrate TTS synthesis"""
        self.print_header("DEMO 2: Text-to-Speech Synthesis")
        
        for i, text in enumerate(self.config.SAMPLE_TEXTS, 1):
            print(f"\n[{i}] Text: \"{text}\"")
            
            # Normalize
            normalized = self.normalizer.normalize(text, strip_whitespace=True)
            
            # Synthesize with different engines
            for engine in ['gtts', 'pyttsx3']:
                try:
                    print(f"    Engine: {engine.upper()}")
                    
                    audio = self.tts.synthesize(
                        normalized,
                        engine=engine,
                        speed=1.0
                    )
                    
                    # Save to file
                    filename = f"tts_demo_{i}_{engine}.mp3"
                    result = self.writer.write(audio, filename, overwrite=True)
                    
                    print(f"    ✓ Generated: {result['file_size']} bytes, "
                          f"{audio.duration:.2f}s duration")
                    print(f"    ✓ Saved to: {result['file_path']}")
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}")
    
    def demo_speech_to_text(self):
        """Demonstrate STT recognition"""
        self.print_header("DEMO 3: Speech-to-Text Recognition")
        
        # Create mock audio files for demo
        mock_audios = [
            ("sample_meeting.wav", "Meeting transcript example"),
            ("sample_dictation.wav", "Dictation example"),
            ("sample_interview.wav", "Interview recording")
        ]
        
        print("Note: Using mock audio data for demonstration\n")
        
        for filename, description in mock_audios:
            print(f"Processing: {filename}")
            print(f"Description: {description}")
            
            # Create mock audio
            mock_audio = AudioData(
                audio_bytes=b"MOCK_AUDIO_" + description.encode(),
                format='wav',
                sample_rate=16000,
                duration=5.0
            )
            
            # Recognize with different engines
            for engine in ['google', 'whisper']:
                try:
                    print(f"  Engine: {engine.upper()}")
                    
                    text = self.stt.recognize(
                        mock_audio,
                        engine=engine,
                        language='en-US'
                    )
                    
                    print(f"  ✓ Transcription: \"{text.text}\"")
                    print(f"  ✓ Confidence: {text.confidence:.2%}")
                    print(f"  ✓ Language: {text.language}")
                    
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            
            print()
    
    def demo_file_operations(self):
        """Demonstrate secure file operations"""
        self.print_header("DEMO 4: Secure File Operations")
        
        # Test valid operations
        print("Testing valid file operations:")
        
        test_audio = AudioData(
            audio_bytes=b"TEST_AUDIO_DATA_12345",
            format='wav',
            sample_rate=44100,
            duration=1.0
        )
        
        valid_paths = [
            "test_output.wav",
            "subdirectory/nested_file.wav",
            "voices/user_recordings/session_001.wav"
        ]
        
        for path in valid_paths:
            try:
                result = self.writer.write(test_audio, path, overwrite=True)
                print(f"  ✓ Wrote: {result['file_path']} ({result['file_size']} bytes)")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        # Test security features
        print("\nTesting security features (should be blocked):")
        
        malicious_paths = [
            ("../../etc/passwd", "Path traversal attempt"),
            ("../outside_directory.wav", "Directory escape"),
            ("malware.exe", "Invalid extension"),
            ("/absolute/path/hack.wav", "Absolute path")
        ]
        
        for path, description in malicious_paths:
            try:
                self.writer.write(test_audio, path, overwrite=True)
                print(f"  ✗ SECURITY ISSUE: {path} was not blocked!")
            except VoiceTextException as e:
                print(f"  ✓ Blocked: {path} - {description}")
            except Exception as e:
                print(f"  ✓ Blocked: {path} - {type(e).__name__}")
    
    def demo_error_handling(self):
        """Demonstrate error handling and recovery"""
        self.print_header("DEMO 5: Error Handling & Recovery")
        
        error_scenarios = [
            {
                "name": "Empty Text Normalization",
                "func": lambda: self.normalizer.normalize(""),
                "expected": "Empty text error"
            },
            {
                "name": "Nonexistent File Load",
                "func": lambda: self.loader.load("/fake/path/audio.wav"),
                "expected": "File not found error"
            },
            {
                "name": "Unsupported STT Engine",
                "func": lambda: self.stt.recognize(
                    AudioData(b"test", "wav", 16000, 1.0),
                    engine='invalid_engine'
                ),
                "expected": "Unsupported engine error"
            },
            {
                "name": "Text Exceeds TTS Limit",
                "func": lambda: self.tts.synthesize(
                    TextData("A" * 10000),
                    engine='gtts'
                ),
                "expected": "Text too long error"
            }
        ]
        
        for scenario in error_scenarios:
            print(f"Testing: {scenario['name']}")
            print(f"Expected: {scenario['expected']}")
            
            try:
                scenario['func']()
                print(f"  ✗ No error raised (unexpected!)")
            except VoiceTextException as e:
                print(f"  ✓ Caught: {type(e).__name__} - {str(e)[:60]}")
            except Exception as e:
                print(f"  ✓ Caught: {type(e).__name__} - {str(e)[:60]}")
            
            print()
    
    def demo_logging_analysis(self):
        """Demonstrate logging and trace analysis"""
        self.print_header("DEMO 6: Logging & Trace Analysis")
        
        print("Running operations to generate logs...\n")
        
        # Generate some trace logs
        text = self.normalizer.normalize("Sample text for logging demo")
        mock_audio = AudioData(b"sample", "wav", 16000, 2.0)
        self.stt.recognize(mock_audio, engine='google')
        
        # Read and analyze logs
        print("Recent trace events from llm_interaction.log:")
        print("-" * 70)
        
        if os.path.exists("llm_interaction.log"):
            with open("llm_interaction.log", "r") as f:
                lines = f.readlines()
                
                # Show last 10 trace events
                for line in lines[-10:]:
                    try:
                        trace = json.loads(line.strip())
                        print(f"[{trace['component']}] {trace['event']}")
                        print(f"  Time: {trace['timestamp']}")
                        print(f"  Duration: {trace['duration_ms']:.2f}ms")
                        if trace.get('data'):
                            print(f"  Data: {trace['data']}")
                        print()
                    except json.JSONDecodeError:
                        pass
        else:
            print("(No log file found - run some operations first)")
        
        print("\nSystem errors from system.log:")
        print("-" * 70)
        
        if os.path.exists("system.log"):
            with open("system.log", "r") as f:
                lines = f.readlines()
                
                # Show last 5 error entries
                error_lines = [l for l in lines if "ERROR" in l]
                for line in error_lines[-5:]:
                    print(line.strip())
        else:
            print("(No system errors logged)")
    
    def demo_performance_metrics(self):
        """Demonstrate performance monitoring"""
        self.print_header("DEMO 7: Performance Metrics")
        
        import time
        
        benchmarks = []
        
        # Benchmark 1: Text normalization
        text = "A" * 1000
        start = time.perf_counter()
        for _ in range(100):
            self.normalizer.normalize(text, lowercase=True)
        duration = time.perf_counter() - start
        avg_ms = (duration / 100) * 1000
        benchmarks.append(("Text Normalization (1000 chars)", avg_ms, 3.0))
        
        # Benchmark 2: File write
        audio = AudioData(b"X" * 10000, 'wav', 44100, 1.0)
        start = time.perf_counter()
        for i in range(10):
            self.writer.write(audio, f"perf_test_{i}.wav", overwrite=True)
        duration = time.perf_counter() - start
        avg_ms = (duration / 10) * 1000
        benchmarks.append(("File Write (10KB)", avg_ms, 50.0))
        
        # Benchmark 3: Mock STT
        mock_audio = AudioData(b"test" * 100, 'wav', 16000, 3.0)
        start = time.perf_counter()
        for _ in range(10):
            self.stt.recognize(mock_audio, engine='google')
        duration = time.perf_counter() - start
        avg_ms = (duration / 10) * 1000
        benchmarks.append(("STT Recognition (mock)", avg_ms, 100.0))
        
        # Display results
        print(f"{'Operation':<40} {'Avg Time':<15} {'Target':<15} {'Status'}")
        print("-" * 80)
        
        for operation, measured, target in benchmarks:
            status = "✓ PASS" if measured <= target else "✗ SLOW"
            print(f"{operation:<40} {measured:>8.2f}ms      {target:>8.2f}ms      {status}")
    
    def run_all_demos(self):
        """Run all demonstration scenarios"""
        self.print_header("Voice-Text Conversion Library - Complete Demo")
        
        demos = [
            ("Text Normalization", self.demo_text_normalization),
            ("Text-to-Speech Synthesis", self.demo_text_to_speech),
            ("Speech-to-Text Recognition", self.demo_speech_to_text),
            ("Secure File Operations", self.demo_file_operations),
            ("Error Handling & Recovery", self.demo_error_handling),
            ("Logging & Trace Analysis", self.demo_logging_analysis),
            ("Performance Metrics", self.demo_performance_metrics)
        ]
        
        for i, (name, demo_func) in enumerate(demos, 1):
            try:
                demo_func()
                input(f"\nPress Enter to continue to next demo ({i}/{len(demos)})...")
            except KeyboardInterrupt:
                print("\n\nDemo interrupted by user.")
                break
            except Exception as e:
                print(f"\n✗ Demo error: {e}")
                import traceback
                traceback.print_exc()
        
        self.print_header("Demo Complete")
        print("Check the following for outputs:")
        print(f"  - Audio files: {self.config.OUTPUT_DIR}")
        print(f"  - Trace logs: llm_interaction.log")
        print(f"  - Error logs: system.log")
        print()

# ============================================================================
# INTERACTIVE MENU
# ============================================================================

def show_menu():
    """Display interactive menu"""
    print("\n" + "=" * 70)
    print("  Voice-Text Conversion Library - Interactive Demo")
    print("=" * 70)
    print("\n1. Text Normalization Demo")
    print("2. Text-to-Speech Demo")
    print("3. Speech-to-Text Demo")
    print("4. Secure File Operations Demo")
    print("5. Error Handling Demo")
    print("6. Logging Analysis Demo")
    print("7. Performance Metrics Demo")
    print("8. Run All Demos")
    print("9. Exit")
    print()

def main():
    """Main entry point"""
    demo = VoiceTextDemo()
    
    while True:
        show_menu()
        
        try:
            choice = input("Select option (1-9): ").strip()
            
            if choice == '1':
                demo.demo_text_normalization()
            elif choice == '2':
                demo.demo_text_to_speech()
            elif choice == '3':
                demo.demo_speech_to_text()
            elif choice == '4':
                demo.demo_file_operations()
            elif choice == '5':
                demo.demo_error_handling()
            elif choice == '6':
                demo.demo_logging_analysis()
            elif choice == '7':
                demo.demo_performance_metrics()
            elif choice == '8':
                demo.run_all_demos()
            elif choice == '9':
                print("\nExiting demo. Thank you!")
                break
            else:
                print("\n✗ Invalid option. Please select 1-9.")
            
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
