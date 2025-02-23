
**Fallout Terminal Developer Documentation - v1.4**

**Table of Contents**

1. Project Overview  
2. Architecture  
3. Components  
    - Theme System  
    - Audio Processing  
    - Key Event Handling  
    - Error Handling  
4. Configurations  
    - Theme Configuration  
    - Environment Variables  
5. Installation and Setup  
    - Dependencies  
    - Hardware Configuration  
    - Generating silence.wav  
6. Usage  
    - Running the Script  
    - Interacting with the Terminal  
7. Development Guidelines  
    - Adding New Themes  
    - Customizing Audio Settings  
    - Debugging Tips  
8. Troubleshooting  
9. Future Enhancements  

---

**1. Project Overview**

The Fallout Terminal is an interactive, voice-controlled AI assistant inspired by themed experiences (e.g., Fallout, Barbie, Terminator). Built in Python, it runs on a Raspberry Pi and leverages OpenAI APIs for speech-to-text (STT), text-to-text AI (ChatGPT), and text-to-speech (TTS). The project supports a dynamic theme system, allowing developers to customize the AI's personality, voice, and behavior via JSON files.

This documentation equips developers with the knowledge to maintain, extend, and debug the application, making it a valuable resource for both current and future contributors.

---

**2. Architecture**

The Fallout Terminal follows a modular design:

- Theme System: Loads configurations from JSON files in the themes/ directory to define the AI’s personality and settings.
- Audio Input: Captures voice via sounddevice, transcribed using Whisper.
- AI Interaction: Processes transcriptions with ChatGPT for themed responses.
- Audio Output: Converts responses to speech with OpenAI TTS, played via paplay.
- Key Event Handling: Uses the keyboard library to manage user interactions.

---

**3. Components**

**Theme System**

- Purpose: Defines the AI’s personality, TTS voice, and STT model.
- Implementation: Each theme is a JSON file in themes/ with the following structure:
  - {
    - "theme_name": "Fallout",
    - "system_message": "You are a gritty Fallout terminal AI.",
    - "voice": "onyx",
    - "intro_user_prompt": "Introduce yourself as a Fallout terminal.",
    - "whisper_model": "tiny"
  - }
- Key Fields:
  - theme_name: Unique identifier.
  - system_message: ChatGPT behavior prompt.
  - voice: TTS voice (e.g., "onyx", "nova").
  - intro_user_prompt: Generates the AI’s intro.
  - whisper_model: STT model (e.g., "tiny", "base").

**Audio Processing**

- Input:
  - Captured using sounddevice (16,000 Hz sample rate, 512 block size).
  - Optimized with pre-allocated NumPy arrays.
- Transcription:
  - Processed by Whisper with configurable model sizes.
- Output:
  - Generated via OpenAI TTS and played with paplay, prefixed with silence.wav to minimize latency.

**Key Event Handling**

- Library: keyboard (requires sudo for root privileges).
- Controls:
  - Left Shift: Start/stop recording.
  - 'q': Exit the application.

**Error Handling**

- Theme Validation: Ensures JSON files include required fields and valid syntax.
- API Resilience: Handles OpenAI API failures with user-friendly feedback.

---

**4. Configurations**

**Theme Configuration**

- Location: themes/ directory.
- Example:
  - {
    - "theme_name": "Terminator",
    - "system_message": "You are a cold, calculating Terminator AI.",
    - "voice": "alloy",
    - "intro_user_prompt": "State your designation and purpose.",
    - "whisper_model": "base"
  - }

**Environment Variables**

- OpenAI API Key:
  - Command: export OPENAI_API_KEY='your-api-key-here'

---

**5. Installation and Setup**

**Dependencies**

- Python Libraries:
  - Command: pip install openai sounddevice numpy whisper keyboard
- System Packages:
  - Install sox for silence file generation:
    - Command: sudo apt install sox

**Hardware Configuration**

- Platform: Raspberry Pi (configured for user h4xb0t).
- Audio: Requires PulseAudio for paplay.

**Generating silence.wav**

- Create a 0.5-second silence file:
  - Command: sox -n -t wav silence.wav trim 0.0 0.5
- Place it in the script’s working directory.

---

**6. Usage**

**Running the Script**

- Run with sudo to preserve environment variables:
  - Command: sudo -E /path/to/venv/bin/python terminal_v1.4.py
- Select a theme from the displayed menu.

**Interacting with the Terminal**

- Record: Hold Left Shift (max 10 seconds).
- Response: Release to hear the AI’s themed reply.
- Exit: Press 'q'.

---

**7. Development Guidelines**

**Adding New Themes**

1. Create a new JSON file in themes/ (e.g., my_theme.json).
2. Define the required fields:
   - {
     - "theme_name": "my_theme",
     - "system_message": "Your custom AI behavior.",
     - "voice": "nova",
     - "intro_user_prompt": "Your intro here.",
     - "whisper_model": "tiny"
   - }
3. The theme will auto-appear in the menu.

**Customizing Audio Settings**

- Adjust BLOCK_SIZE (default: 512) or SAMPLE_RATE (default: 16,000 Hz) in the script.
- Ensure Whisper compatibility with the sample rate.

**Debugging Tips**

- Audio Failures: Verify microphone setup and PulseAudio.
- API Issues: Check API key validity and network status.
- Transcription Errors: Test alternative Whisper models.

---

**8. Troubleshooting**

- "No audio captured": Confirm microphone connectivity and sufficient Left Shift hold time.
- "Invalid theme file": Validate JSON syntax and required fields.
- "API connection failed": Ensure API key is set and internet is active.

---

**9. Future Enhancements**

- UI Feedback: Add visual cues for recording/processing states.
- Dynamic Data: Integrate external APIs (e.g., weather updates).
- Voice Flexibility: Enable runtime voice changes.
- Profiles: Support per-user configurations.

---

This documentation is formatted for easy pasting into Google Docs, using bold headings and simple lists to maintain readability and structure. It provides a detailed, developer-centric view of the Fallout Terminal project at version 1.4, ready for maintenance or extension by any developer.


