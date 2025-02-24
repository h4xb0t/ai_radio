# RizzWave v1.0 AI HAM RADIO

The **RizzWave v1.0 AI HAM RADIO** is an interactive, voice-controlled AI assistant inspired by ham radio vibes and Gen Z/Alpha culture. Built in Python for a Raspberry Pi, it uses OpenAI’s APIs for speech-to-text (Whisper), text-to-text (ChatGPT), and text-to-speech (TTS). Customize the AI’s personality with dynamic themes loaded from JSON files.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Theme Configuration](#theme-configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

---

## Project Overview

The RizzWave v1.0 AI HAM RADIO turns your Raspberry Pi into a voice-activated AI terminal with a twist—retro ham radio flair meets modern AI. Pick a theme like a Fallout survivor or Skibidi Toilet AI, and chat using push-to-talk. It’s a wild, fun experiment for tinkerers and AI enthusiasts.

---

## Features

- **Dynamic Theme Selection**: Switch between personalities (e.g., Fallout, Skibidi, Terminator) via JSON configs.
- **Voice Interaction**: Hold Left Shift to record audio, transcribed by Whisper, with AI responses via ChatGPT.
- **Text-to-Speech**: Hear themed replies with OpenAI’s TTS voices (e.g., "onyx", "nova").
- **Customizable**: Add your own themes with ease.
- **Lightweight**: Runs on a Raspberry Pi with minimal setup.

---

## Installation

### Prerequisites

- Raspberry Pi (configured for user `h4xb0t`)
- Python 3.11+
- PulseAudio for audio playback
- OpenAI API Key

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/rizzwave-ai-ham-radio.git
   cd rizzwave-ai-ham-radio
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

5. **Generate Theme Files**:
   Run the theme generator to populate the `themes/` directory:
   ```bash
   python generate_themes.py
   ```

6. **Generate `silence.wav`** (For latency reduction):
   ```bash
   sudo apt install sox
   sox -n -t wav silence.wav trim 0.0 0.5
   ```

---

## Usage

1. **Run the Script**:
   Use `sudo -E` to preserve environment variables and run as root:
   ```bash
   sudo -E /path/to/venv/bin/python rizzwave_v1.0.py
   ```

2. **Select a Theme**:
   Pick a theme from the list (e.g., `1. Fallout`, `7. Skibidi`).

3. **Interact with the AI**:
   - Hold **Left Shift** to record (max 10 seconds).
   - Release to hear the AI’s themed response.
   - Press `'q'` to quit.

---

## Theme Configuration

Themes live in the `themes/` directory as JSON files. Here’s an example:

```json
{
  "theme_name": "skibidi",
  "system_message": "Yo, you’re the Skibidi Toilet AI, straight outta Ohio, dripping sigma rizz. Spit brain rot answers, max 50 words—keep it sus, lit, and totally goated. No cap, fam, let’s get this bread! Yeet!",
  "voice": "onyx",
  "intro_user_prompt": "Drop a wild intro as the Skibidi Toilet AI, welcome some Gen Z/Alpha zoomers, and flex your sigma readiness to roll.",
  "whisper_model": "tiny"
}
```

- **`theme_name`**: Unique identifier.
- **`system_message`**: Sets the AI’s personality for ChatGPT.
- **`voice`**: TTS voice (e.g., "onyx", "nova").
- **`intro_user_prompt`**: Triggers the AI’s intro message.
- **`whisper_model`**: STT model (e.g., "tiny", "base").

Add a new theme by dropping a JSON file in `themes/` with these fields.

---

## Testing

This project uses GitHub Actions for continuous integration. Tests run automatically on every push and pull request to the `main` branch.

### Run Tests Locally

1. Install testing dependencies:
   ```bash
   pip install pytest
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-key'
   ```

3. Run the tests:
   ```bash
   pytest tests/
   ```

---

## Troubleshooting

- **"No audio captured"**: Check your mic and hold Left Shift long enough.
- **"Invalid theme file"**: Verify JSON syntax and required fields.
- **"API connection failed"**: Confirm your API key and internet connection.
- **Audio issues**: Ensure PulseAudio is running and check sinks:
  ```bash
  pactl info
  pactl list sinks short
  ```

See the [PulseAudio docs](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/) for more.

---

## Future Enhancements

- **Hardware Case**: Build a retro ham radio-inspired enclosure.
- **More Themes**: Expand the theme library or tweak voices on the fly.
- **API Add-ons**: Pull live data (e.g., weather) into responses.
- **User Profiles**: Save settings for multiple users.

---

## Contributing

Fork the repo, add themes, or tweak features—pull requests are welcome! For big changes, open an issue to chat about it first.

---

## Disclaimer

This is a fun, experimental project—not for production use. It relies on third-party APIs and may need tweaks for different hardware.
