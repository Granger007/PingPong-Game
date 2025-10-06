"""
Generate simple sound effects for the Ping Pong game.
Run this script once to create the sound files in the assets folder.
"""

import numpy as np
import wave
import os

def generate_beep(filename, frequency=440, duration=0.1, sample_rate=44100):
    """Generate a simple beep sound"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate tone with envelope to prevent clicks
    tone = np.sin(2 * np.pi * frequency * t)
    envelope = np.exp(-t * 10)  # Decay envelope
    audio = tone * envelope
    
    # Normalize to 16-bit range
    audio = np.int16(audio * 32767 * 0.5)
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    print(f"Created {filename}")

def generate_noise(filename, duration=0.05, sample_rate=44100):
    """Generate a short noise burst for wall bounce"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # White noise with envelope
    noise = np.random.uniform(-1, 1, len(t))
    envelope = np.exp(-t * 50)
    audio = noise * envelope
    
    # Normalize
    audio = np.int16(audio * 32767 * 0.3)
    
    os.makedirs('assets', exist_ok=True)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    print(f"Created {filename}")

def generate_score_sound(filename, duration=0.3, sample_rate=44100):
    """Generate a rising tone for scoring"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Rising frequency
    freq = 400 + 400 * t / duration
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    tone = np.sin(phase)
    
    # Envelope
    envelope = np.exp(-t * 5)
    audio = tone * envelope
    
    # Normalize
    audio = np.int16(audio * 32767 * 0.5)
    
    os.makedirs('assets', exist_ok=True)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    print(f"Created {filename}")

if __name__ == "__main__":
    print("Generating sound effects...")
    
    # Generate paddle hit sound (mid frequency beep)
    generate_beep('assets/paddle.wav', frequency=600, duration=0.08)
    
    # Generate wall bounce sound (short noise burst)
    generate_noise('assets/wall.wav', duration=0.04)
    
    # Generate score sound (rising tone)
    generate_score_sound('assets/score.wav', duration=0.25)
    
    print("\nAll sound effects created successfully!")
    print("Sound files are in the 'assets' folder.")