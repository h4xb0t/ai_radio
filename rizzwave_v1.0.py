import openai
import os
import sounddevice as sd
import numpy as np
import whisper
import time
import keyboard
import subprocess
import signal
import json

# Suppress Whisper FP16 warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

# Script version and name
VERSION = "1.0"
NAME = "RizzWave v1.0 AI HAM RADIO"

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Error: No API key set! Run: export OPENAI_API_KEY='your-key'")
    exit(1)

# Audio settings
BLOCK_SIZE = 512  # Smaller block size for lower latency
SAMPLE_RATE = 16000  # Whisper’s expected rate
CHANNELS = 1  # Mono audio

# List JSON files in the themes/ directory
theme_files = [f for f in os.listdir('themes') if f.endswith('.json')]
themes = [os.path.splitext(f)[0] for f in theme_files]
themes = sorted(themes)

# Display available themes
if not themes:
    print("Error: No themes found in the themes/ directory.")
    exit(1)

print(f"{NAME} - Available themes:")
for i, theme in enumerate(themes, 1):
    print(f"{i}. {theme}".title())

# Prompt user to select a theme
while True:
    choice = input("Select a theme by entering its number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(themes):
        selected_theme = themes[int(choice) - 1]
        break
    else:
        print("Invalid selection. Please try again.")

# Load the selected theme
theme_file = f"themes/{selected_theme}.json"
try:
    with open(theme_file, 'r') as f:
        theme_config = json.load(f)
except FileNotFoundError:
    print(f"Error: Theme file '{theme_file}' not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Theme file '{theme_file}' contains invalid JSON.")
    exit(1)

# Validate theme configuration
required_keys = ["theme_name", "system_message", "voice", "intro_user_prompt", "whisper_model"]
for key in required_keys:
    if key not in theme_config:
        print(f"Error: Missing key '{key}' in theme file '{theme_file}'.")
        exit(1)

# Load Whisper model based on theme config
whisper_model_size = theme_config["whisper_model"]
try:
    whisper_model = whisper.load_model(whisper_model_size)
    print(f"Loaded Whisper model: {whisper_model_size}")
except ValueError:
    print(f"Error: Invalid Whisper model '{whisper_model_size}'. Use 'tiny', 'base', 'small', 'medium', or 'large'.")
    exit(1)

# Audio recording setup
max_duration = 10  # seconds
max_frames = int(SAMPLE_RATE * max_duration / BLOCK_SIZE)
audio_frames = np.zeros((max_frames, BLOCK_SIZE, CHANNELS), dtype=np.float32)  # Match indata shape
frame_count = 0
is_recording = False
running = True
max_samples = SAMPLE_RATE * max_duration
conversation_history = []
current_playback_process = None  # Track ongoing audio playback

# Environment for audio playback (PulseAudio as user h4xb0t)
env = os.environ.copy()
env["XDG_RUNTIME_DIR"] = "/run/user/1000"  # Adjust UID if needed
env["PULSE_SERVER"] = "unix:/run/user/1000/pulse/native"

# Callback for audio input
def callback(indata, frames, time_, status):
    global frame_count
    if is_recording and frame_count < max_frames:
        audio_frames[frame_count] = indata  # Direct assignment, shapes match
        frame_count += 1

# Initialize audio stream
stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    blocksize=BLOCK_SIZE,
    callback=callback
)
stream.start()  # Start the stream once and keep it running

def speak_response(text):
    """Generate and play audio response with silence pre-roll."""
    global current_playback_process
    try:
        # Generate audio with OpenAI TTS using theme's voice
        response = openai.audio.speech.create(
            model="tts-1",
            voice=theme_config["voice"],
            input=text
        )
        # Write audio directly to file
        with open("output.wav", "wb") as f:
            f.write(response.content)

        # Play silence pre-roll if it exists (no process tracking here)
        if os.path.exists("silence.wav"):
            silence_process = subprocess.Popen(
                ["sudo", "-E", "-u", "h4xb0t", "paplay", "silence.wav"],
                env=env
            )
            silence_process.wait()
        else:
            print("Warning: silence.wav not found—latency issues may occur!")

        # Play the actual TTS audio asynchronously
        current_playback_process = subprocess.Popen(
            ["sudo", "-E", "-u", "h4xb0t", "paplay", "output.wav"],
            env=env
        )
        # Don’t wait—let it play in the background so it can be interrupted
    except Exception as e:
        print(f"Error in audio playback: {e}")

def on_key_event(e):
    """Handle Left Shift key events for push-to-talk, Q to exit."""
    global is_recording, audio_frames, running, current_playback_process, frame_count
    if e.name == 'shift':  # Push-to-talk key (Left Shift)
        if e.event_type == keyboard.KEY_DOWN and not is_recording:
            # Interrupt any ongoing playback
            if current_playback_process and current_playback_process.poll() is None:
                os.kill(current_playback_process.pid, signal.SIGKILL)  # Instant kill
                current_playback_process = None
                print("Audio playback halted")
                time.sleep(0.2)  # Brief delay to let audio system settle
            is_recording = True
            frame_count = 0  # Reset frame counter
            print("Recording... (hold Left Shift to speak, max 10 seconds)")
        elif e.event_type == keyboard.KEY_UP and is_recording:
            is_recording = False
            print("Processing...")
            if frame_count > 0:
                audio_data = audio_frames[:frame_count].reshape(-1, CHANNELS).flatten()  # Flatten to 1D
                if len(audio_data) > max_samples:
                    audio_data = audio_data[-max_samples:]
                audio_data = audio_data.astype(np.float32)
                transcribed_text = whisper_model.transcribe(audio_data)["text"]
                print(f"Transcribed: '{transcribed_text}'")
                if transcribed_text.strip():
                    gpt_response = chat_with_gpt(transcribed_text)
                    if gpt_response:
                        print(f"🤖 {theme_config['theme_name'].replace('_', ' ').title()} AI: {gpt_response}")
                        speak_response(gpt_response)
                        conversation_history.append({"role": "user", "content": transcribed_text})
                        conversation_history.append({"role": "assistant", "content": gpt_response})
                frame_count = 0  # Reset after processing
            else:
                print("No audio captured—check your microphone!")
    elif e.name == 'q' and e.event_type == keyboard.KEY_DOWN:  # Exit key
        print("Q key pressed—shutting down...")
        running = False

def chat_with_gpt(prompt):
    """Get response from ChatGPT with custom theme instructions."""
    try:
        system_message = {"role": "system", "content": theme_config["system_message"]}
        messages = [system_message] + conversation_history + [{"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except openai.OpenAIError as err:
        print(f"OpenAI API error: {err}")
        return None

def generate_intro():
    """Generate a custom theme-based intro from ChatGPT."""
    try:
        system_message = {"role": "system", "content": theme_config["system_message"]}
        user_message = {"role": "user", "content": theme_config["intro_user_prompt"]}
        messages = [system_message, user_message]
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except openai.OpenAIError as err:
        print(f"Error generating intro: {err}")
        return f"{theme_config['theme_name'].replace('_', ' ').title()} AI online—ready."  # Fallback intro

# Hook keyboard events
keyboard.hook(on_key_event)

# Initial greeting with dynamic intro
print(f"Initializing {NAME} with {theme_config['theme_name'].replace('_', ' ').title()}...")
time.sleep(1)
greeting = generate_intro()
print(f"🤖 {theme_config['theme_name'].replace('_', ' ').title()} AI: {greeting}")
speak_response(greeting)
print("Hold Left Shift to speak (press Q to exit). Release to process (max 10 seconds).")

# Main loop
while running:
    time.sleep(0.05)  # Reduced sleep for responsiveness

# Cleanup
if current_playback_process and current_playback_process.poll() is None:
    os.kill(current_playback_process.pid, signal.SIGKILL)
stream.stop()
stream.close()
keyboard.unhook_all()
print(f"{NAME} offline.")

