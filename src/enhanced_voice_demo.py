"""
Enhanced Voice Customization System - Interactive Demo
Showcase all voice profile and sound customization features
"""

import sys
from pathlib import Path

try:
    from enhanced_voice_profiles import (
        VoiceCustomizationEngine,
        VoiceProfile,
        Gender,
        Emotion,
        AudioEffect,
        VoiceTransform,
        EffectConfig
    )
    from voice_text_lib import AudioData, TextData
except ImportError:
    print("Error: Required modules not found.")
    print("Ensure enhanced_voice_profiles.py and voice_text_lib.py are in the same directory.")
    sys.exit(1)

# ============================================================================
# DEMO CLASS
# ============================================================================

class EnhancedVoiceDemo:
    """Interactive demonstration of voice customization features"""
    
    def __init__(self):
        self.engine = VoiceCustomizationEngine()
        self.current_profile = None
        self.sample_audio = AudioData(b"DEMO_AUDIO_SAMPLE", "wav", 16000, 3.0)
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80 + "\n")
    
    def print_profile_details(self, profile: VoiceProfile):
        """Display profile information"""
        print(f"Profile Name: {profile.name}")
        print(f"Profile ID: {profile.profile_id[:16]}...")
        print(f"Gender: {profile.gender}")
        print(f"Pitch: {profile.pitch:+.1f} semitones")
        print(f"Speed: {profile.speed:.2f}x")
        print(f"Volume: {profile.volume:.2f}x")
        print(f"Language: {profile.language}")
        print(f"Accent: {profile.accent}")
        print(f"Default Emotion: {profile.emotion_default}")
    
    # ========================================================================
    # DEMO 1: Preset Voice Profiles
    # ========================================================================
    
    def demo_preset_profiles(self):
        """Demonstrate preset voice profiles"""
        self.print_header("DEMO 1: Preset Voice Profiles")
        
        print("Available preset profiles:\n")
        
        presets = self.engine.get_preset_list()
        
        for i, preset_name in enumerate(presets, 1):
            print(f"[{i}] {preset_name.replace('_', ' ').title()}")
            
            # Load and show details
            profile = self.engine.profile_manager.load_preset(preset_name)
            print(f"    Gender: {profile.gender}, "
                  f"Pitch: {profile.pitch:+.1f}, "
                  f"Speed: {profile.speed:.2f}x, "
                  f"Age: {profile.age_range}")
            print()
        
        print(f"Total presets available: {len(presets)}")
        
        # Load a preset as current profile
        self.current_profile = self.engine.profile_manager.load_preset("professional_male")
        print(f"\n✓ Loaded 'professional_male' as current profile")
    
    # ========================================================================
    # DEMO 2: Custom Voice Creation
    # ========================================================================
    
    def demo_custom_voices(self):
        """Demonstrate creating custom voices"""
        self.print_header("DEMO 2: Creating Custom Voice Profiles")
        
        # Example 1: From preset
        print("[Example 1] Custom voice from preset:\n")
        
        custom1 = self.engine.create_custom_voice(
            name="Energetic News Anchor",
            base_preset="professional_female",
            pitch=1.5,
            speed=1.15,
            volume=1.05,
            emotion_default=Emotion.CONFIDENT.value
        )
        
        self.print_profile_details(custom1)
        
        # Example 2: From scratch
        print("\n[Example 2] Custom voice from scratch:\n")
        
        custom2 = self.engine.create_custom_voice(
            name="Calm Meditation Guide",
            gender=Gender.NEUTRAL.value,
            pitch=-0.5,
            speed=0.8,
            volume=0.9,
            accent="neutral",
            age_range="adult",
            emotion_default=Emotion.CALM.value
        )
        
        self.print_profile_details(custom2)
        
        # Example 3: Character voice
        print("\n[Example 3] Character voice (child):\n")
        
        custom3 = self.engine.create_custom_voice(
            name="Friendly Robot Companion",
            gender=Gender.NEUTRAL.value,
            pitch=6.0,
            speed=1.2,
            volume=1.0,
            age_range="child",
            emotion_default=Emotion.HAPPY.value,
            custom_params={"robotic_filter": True}
        )
        
        self.print_profile_details(custom3)
        
        self.current_profile = custom1
        print(f"\n✓ Set '{custom1.name}' as current profile")
    
    # ========================================================================
    # DEMO 3: Audio Effects
    # ========================================================================
    
    def demo_audio_effects(self):
        """Demonstrate audio effects"""
        self.print_header("DEMO 3: Audio Effects Processing")
        
        effects_component = self.engine.effects
        
        # Effect 1: Reverb
        print("[Effect 1] Reverb (Concert Hall):\n")
        reverb = effects_component.create_reverb(room_size=0.8, damping=0.4)
        print(f"  Type: {reverb.effect_type}")
        print(f"  Room Size: {reverb.intensity}")
        print(f"  Damping: {reverb.parameters['damping']}")
        
        result1 = effects_component.apply_effects(self.sample_audio, [reverb])
        print(f"  ✓ Applied: {len(result1.audio_bytes)} bytes")
        
        # Effect 2: Echo
        print("\n[Effect 2] Echo (Slapback):\n")
        echo = effects_component.create_echo(delay_ms=150, feedback=0.35)
        print(f"  Type: {echo.effect_type}")
        print(f"  Delay: {echo.parameters['delay_ms']}ms")
        print(f"  Feedback: {echo.intensity}")
        
        result2 = effects_component.apply_effects(self.sample_audio, [echo])
        print(f"  ✓ Applied: {len(result2.audio_bytes)} bytes")
        
        # Effect 3: Equalizer
        print("\n[Effect 3] Equalizer (Warm Voice):\n")
        eq = effects_component.create_equalizer(bass=4, mid=1, treble=-2)
        print(f"  Type: {eq.effect_type}")
        print(f"  Bass: +{eq.parameters['bass']}dB")
        print(f"  Mid: +{eq.parameters['mid']}dB")
        print(f"  Treble: {eq.parameters['treble']}dB")
        
        result3 = effects_component.apply_effects(self.sample_audio, [eq])
        print(f"  ✓ Applied: {len(result3.audio_bytes)} bytes")
        
        # Effect Chain
        print("\n[Effect Chain] Combining multiple effects:\n")
        effects_chain = [
            effects_component.create_reverb(room_size=0.5, damping=0.6),
            effects_component.create_echo(delay_ms=300, feedback=0.25),
            effects_component.create_equalizer(bass=2, mid=0, treble=-1)
        ]
        
        result_chain = effects_component.apply_effects(self.sample_audio, effects_chain)
        print(f"  Effects in chain: {len(effects_chain)}")
        print(f"  ✓ Chain applied: {len(result_chain.audio_bytes)} bytes")
        
        for i, effect in enumerate(effects_chain, 1):
            print(f"    {i}. {effect.effect_type}")
    
    # ========================================================================
    # DEMO 4: Voice Transformation
    # ========================================================================
    
    def demo_voice_transformation(self):
        """Demonstrate voice transformations"""
        self.print_header("DEMO 4: Voice Transformation")
        
        transformer = self.engine.transformer
        
        # Transformation 1: Male to Female
        print("[Transformation 1] Male → Female Voice:\n")
        m2f = transformer.male_to_female()
        print(f"  Pitch Shift: {m2f.pitch_shift:+.1f} semitones")
        print(f"  Formant Shift: {m2f.formant_shift:.2f}")
        print(f"  Timbre Morph: {m2f.timbre_morph:+.2f}")
        
        result1 = transformer.transform_voice(self.sample_audio, m2f)
        print(f"  ✓ Transformed: {len(result1.audio_bytes)} bytes\n")
        
        # Transformation 2: Female to Male
        print("[Transformation 2] Female → Male Voice:\n")
        f2m = transformer.female_to_male()
        print(f"  Pitch Shift: {f2m.pitch_shift:+.1f} semitones")
        print(f"  Formant Shift: {f2m.formant_shift:.2f}")
        print(f"  Timbre Morph: {f2m.timbre_morph:+.2f}")
        
        result2 = transformer.transform_voice(self.sample_audio, f2m)
        print(f"  ✓ Transformed: {len(result2.audio_bytes)} bytes\n")
        
        # Transformation 3: Robot Voice
        print("[Transformation 3] Robot Voice Effect:\n")
        robot = transformer.robot_voice()
        print(f"  Pitch Shift: {robot.pitch_shift:+.1f} semitones")
        print(f"  Formant Shift: {robot.formant_shift:.2f}")
        print(f"  Timbre Morph: {robot.timbre_morph:+.2f}")
        print(f"  Roughness: {robot.roughness:.2f}")
        
        result3 = transformer.transform_voice(self.sample_audio, robot)
        print(f"  ✓ Transformed: {len(result3.audio_bytes)} bytes\n")
        
        # Custom Transformation
        print("[Custom Transformation] Slight Pitch Adjustment:\n")
        custom = VoiceTransform(
            pitch_shift=2.5,
            formant_shift=1.08,
            breathiness=0.2
        )
        print(f"  Pitch Shift: {custom.pitch_shift:+.1f} semitones")
        print(f"  Formant Shift: {custom.formant_shift:.2f}")
        print(f"  Breathiness: {custom.breathiness:.2f}")
        
        result4 = transformer.transform_voice(self.sample_audio, custom)
        print(f"  ✓ Transformed: {len(result4.audio_bytes)} bytes")
    
    # ========================================================================
    # DEMO 5: Emotional Tones
    # ========================================================================
    
    def demo_emotions(self):
        """Demonstrate emotional tone application"""
        self.print_header("DEMO 5: Emotional Tone Application")
        
        emotion_engine = self.engine.emotion_engine
        
        print("Available emotions:")
        emotions = emotion_engine.list_emotions()
        for emotion in emotions:
            print(f"  - {emotion}")
        
        print("\nApplying emotions to voice profile:\n")
        
        # Test different emotions
        test_emotions = [
            (Emotion.HAPPY.value, 0.8, "Cheerful presentation"),
            (Emotion.SAD.value, 0.6, "Somber news delivery"),
            (Emotion.ANGRY.value, 0.7, "Assertive argument"),
            (Emotion.EXCITED.value, 1.0, "Enthusiastic announcement"),
            (Emotion.CALM.value, 0.9, "Meditation guidance"),
            (Emotion.CONFIDENT.value, 0.8, "Professional speech")
        ]
        
        for emotion, intensity, description in test_emotions:
            print(f"[{emotion.upper()}] - {description}")
            
            mods = emotion_engine.apply_emotion(
                emotion,
                intensity,
                self.current_profile
            )
            
            print(f"  Intensity: {intensity:.0%}")
            print(f"  Pitch Modifier: {mods['pitch_shift']:+.2f} semitones")
            print(f"  Speed Multiplier: {mods['speed_multiplier']:.2f}x")
            print(f"  Volume Multiplier: {mods['volume_multiplier']:.2f}x")
            
            if 'final_pitch' in mods:
                print(f"  → Final Pitch: {mods['final_pitch']:+.2f}")
                print(f"  → Final Speed: {mods['final_speed']:.2f}x")
            
            print()
    
    # ========================================================================
    # DEMO 6: Complete Pipeline
    # ========================================================================
    
    def demo_complete_pipeline(self):
        """Demonstrate complete voice customization pipeline"""
        self.print_header("DEMO 6: Complete Voice Customization Pipeline")
        
        print("Building a complete voice pipeline:\n")
        
        # Step 1: Create custom profile
        print("[Step 1] Create Custom Voice Profile")
        profile = self.engine.create_custom_voice(
            name="Dynamic Podcast Host",
            base_preset="professional_female",
            pitch=0.5,
            speed=1.05,
            volume=1.0,
            emotion_default=Emotion.CONFIDENT.value
        )
        print(f"  ✓ Created: {profile.name}")
        print(f"    Pitch: {profile.pitch:+.1f}, Speed: {profile.speed:.2f}x\n")
        
        # Step 2: Prepare effects
        print("[Step 2] Configure Audio Effects")
        effects = [
            self.engine.effects.create_reverb(room_size=0.4, damping=0.65),
            self.engine.effects.create_equalizer(bass=2, mid=1, treble=0),
            self.engine.effects.create_echo(delay_ms=200, feedback=0.2)
        ]
        print(f"  ✓ Configured {len(effects)} effects:")
        for effect in effects:
            print(f"    - {effect.effect_type}")
        print()
        
        # Step 3: Select emotion
        print("[Step 3] Select Emotional Tone")
        emotion = Emotion.EXCITED.value
        emotion_intensity = 0.75
        print(f"  ✓ Emotion: {emotion} ({emotion_intensity:.0%} intensity)\n")
        
        # Step 4: Apply complete pipeline
        print("[Step 4] Apply Complete Pipeline")
        final_audio = self.engine.apply_voice_profile(
            audio=self.sample_audio,
            profile=profile,
            emotion=emotion,
            emotion_intensity=emotion_intensity,
            effects=effects
        )
        
        print(f"  ✓ Pipeline executed successfully!")
        print(f"  Input:  {len(self.sample_audio.audio_bytes)} bytes")
        print(f"  Output: {len(final_audio.audio_bytes)} bytes")
        print(f"  Duration: {final_audio.duration:.2f}s")
        print(f"  Format: {final_audio.format}")
        print(f"  Sample Rate: {final_audio.sample_rate} Hz")
        
        print("\n[Pipeline Summary]")
        print(f"  Voice: {profile.name}")
        print(f"  Emotion: {emotion} @ {emotion_intensity:.0%}")
        print(f"  Effects: {len(effects)} applied")
        print(f"  Total Processing: Multi-stage transformation")
    
    # ========================================================================
    # DEMO 7: Profile Management
    # ========================================================================
    
    def demo_profile_management(self):
        """Demonstrate profile storage and management"""
        self.print_header("DEMO 7: Voice Profile Storage & Management")
        
        print("[Operation 1] Saving Custom Profiles\n")
        
        # Create and save profiles
        profiles = [
            self.engine.create_custom_voice(
                name="Morning Show Host",
                base_preset="friendly_assistant",
                pitch=1.0,
                speed=1.1
            ),
            self.engine.create_custom_voice(
                name="Documentary Narrator",
                base_preset="narrator_deep",
                pitch=-3.0,
                speed=0.85
            ),
            self.engine.create_custom_voice(
                name="Customer Service Agent",
                base_preset="professional_female",
                pitch=0.5,
                speed=1.0,
                emotion_default=Emotion.CALM.value
            )
        ]
        
        for profile in profiles:
            print(f"  ✓ Saved: {profile.name}")
            print(f"    ID: {profile.profile_id[:16]}...")
        
        print(f"\n[Operation 2] Listing Saved Profiles\n")
        
        saved_profiles = self.engine.get_saved_profiles()
        print(f"  Total saved profiles: {len(saved_profiles)}\n")
        
        for i, info in enumerate(saved_profiles, 1):
            print(f"  [{i}] {info['name']}")
            print(f"      Gender: {info['gender']}, Language: {info['language']}")
        
        print(f"\n[Operation 3] Loading Saved Profile\n")
        
        if saved_profiles:
            loaded = self.engine.load_saved_profile(saved_profiles[0]['profile_id'])
            print(f"  ✓ Loaded: {loaded.name}")
            self.print_profile_details(loaded)
    
    # ========================================================================
    # DEMO 8: Comparison Showcase
    # ========================================================================
    
    def demo_comparison(self):
        """Demonstrate voice variations on same text"""
        self.print_header("DEMO 8: Voice Comparison Showcase")
        
        print("Applying different voices to the same content:\n")
        print("Text: 'Welcome to our advanced voice customization system!'\n")
        
        test_configs = [
            {
                "name": "Professional Male",
                "preset": "professional_male",
                "emotion": Emotion.CONFIDENT.value,
                "intensity": 0.7
            },
            {
                "name": "Friendly Female",
                "preset": "professional_female",
                "emotion": Emotion.HAPPY.value,
                "intensity": 0.8
            },
            {
                "name": "Deep Narrator",
                "preset": "narrator_deep",
                "emotion": Emotion.CALM.value,
                "intensity": 0.6
            },
            {
                "name": "Excited Child",
                "preset": "child_voice",
                "emotion": Emotion.EXCITED.value,
                "intensity": 1.0
            }
        ]
        
        for i, config in enumerate(test_configs, 1):
            print(f"[Voice {i}] {config['name']}")
            
            profile = self.engine.profile_manager.load_preset(config['preset'])
            emotion_mods = self.engine.emotion_engine.apply_emotion(
                config['emotion'],
                config['intensity'],
                profile
            )
            
            print(f"  Base: Pitch {profile.pitch:+.1f}, Speed {profile.speed:.2f}x")
            print(f"  Emotion: {config['emotion']} @ {config['intensity']:.0%}")
            print(f"  Final: Pitch {emotion_mods.get('final_pitch', 'N/A'):+.1f}, "
                  f"Speed {emotion_mods.get('final_speed', 'N/A'):.2f}x")
            print()
    
    # ========================================================================
    # MAIN MENU
    # ========================================================================
    
    def show_menu(self):
        """Display interactive menu"""
        print("\n" + "=" * 80)
        print("  Enhanced Voice Customization System - Demo Menu")
        print("=" * 80)
        print("\n1. Preset Voice Profiles")
        print("2. Custom Voice Creation")
        print("3. Audio Effects Processing")
        print("4. Voice Transformation")
        print("5. Emotional Tone Application")
        print("6. Complete Pipeline Demo")
        print("7. Profile Storage & Management")
        print("8. Voice Comparison Showcase")
        print("9. Run All Demos")
        print("0. Exit")
        print()
    
    def run(self):
        """Main demo loop"""
        print("\n" + "=" * 80)
        print("  Enhanced Voice Profile & Sound Customization")
        print("  Interactive Demonstration System")
        print("=" * 80)
        
        demos = {
            '1': ("Preset Voice Profiles", self.demo_preset_profiles),
            '2': ("Custom Voice Creation", self.demo_custom_voices),
            '3': ("Audio Effects Processing", self.demo_audio_effects),
            '4': ("Voice Transformation", self.demo_voice_transformation),
            '5': ("Emotional Tone Application", self.demo_emotions),
            '6': ("Complete Pipeline Demo", self.demo_complete_pipeline),
            '7': ("Profile Storage & Management", self.demo_profile_management),
            '8': ("Voice Comparison Showcase", self.demo_comparison)
        }
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Select option (0-9): ").strip()
                
                if choice == '0':
                    print("\nExiting demo. Thank you!")
                    break
                elif choice == '9':
                    # Run all demos
                    for name, demo_func in demos.values():
                        demo_func()
                        input("\nPress Enter to continue...")
                elif choice in demos:
                    demos[choice][1]()
                else:
                    print("\n✗ Invalid option. Please select 0-9.")
                
            except KeyboardInterrupt:
                print("\n\nDemo interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    demo = EnhancedVoiceDemo()
    demo.run()
