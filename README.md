# RizzWave v1.1 AI HAM RADIO

The **RizzWave v1.1 AI HAM RADIO** is an interactive, voice-controlled AI assistant inspired by ham radio vibes and Gen Z/Alpha culture. Built in Python for a Raspberry Pi, it uses OpenAI’s APIs for speech-to-text (Whisper), text-to-text (ChatGPT), and text-to-speech (TTS), with spaCy for intent recognition. Customize the AI’s personality with dynamic themes loaded from JSON files.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Theme Configuration](#theme-configuration)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

---

## Project Overview

The RizzWave v1.1 AI HAM RADIO turns your Raspberry Pi into a voice-activated AI terminal with a twist—retro ham radio flair meets modern AI. Pick a theme like a Fallout survivor or Skibidi Toilet AI, and chat using push-to-talk. It’s a wild, fun experiment for tinkerers and AI enthusiasts.

---

## Features

- **Dynamic Theme Selection**: Switch between personalities (e.g., Fallout, Skibidi, Terminator) via JSON configs.
- **Voice Interaction**: Hold Left Shift to record (max 10s), transcribed by Whisper, with AI responses via ChatGPT.
- **Text-to-Speech**: Hear themed replies with OpenAI’s TTS voices (e.g., "onyx", "nova").
- **Intent Recognition**: Uses spaCy to route weather queries to OpenWeatherMap and general queries to OpenAI.
- **Weather Integration**: 
  - Real-time weather updates powered by the OpenWeatherMap API.
  - Ask naturally (e.g., "What’s the weather in 90210?")—spaCy detects the intent and extracts ZIP codes for precise, location-based data.
  - No ZIP provided? Falls back to a default ZIP code set via the `WEATHER_ZIP` environment variable.
  - Temperature reported in Fahrenheit for that classic American radio vibe.
- **Customizable**: Add your own themes with ease.
- **Lightweight**: Runs on a Raspberry Pi with minimal setup.

---

## Installation

### Prerequisites

- Raspberry Pi (configured for user `h4xb0t`)
- Python 3.9+
- PulseAudio for audio playback
- OpenAI API Key
- OpenWeatherMap API Key

### Setup

1. **Download the Latest Release**:
   - Head to the [releases page](/releases) on GitHub and grab the latest zip file.
   - Extract it to a directory of your choice (e.g., `/home/h4xb0t/rizzwave`).
   - Navigate to the extracted directory:
     ```bash
     cd /home/h4xb0t/rizzwave
     ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install openai sounddevice numpy openai-whisper keyboard requests spacy==3.7.2
   python -m spacy download en_core_web_sm
   ```

4. **Set Your API Keys and Default ZIP Code**:
   ```bash
   export OPENAI_API_KEY='your-openai-key'
   export OPENWEATHERMAP_API_KEY='your-openweathermap-key'
   export WEATHER_ZIP='your-zip-code'  # e.g., '10001' for NYC—sets default weather location
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
   sudo -E /path/to/venv/bin/python rizzwave_v1.1.py
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

## Troubleshooting

- **"No audio captured"**: Check your mic and hold Left Shift long enough.
- **"Invalid theme file"**: Verify JSON syntax and required fields.
- **"API connection failed"**: Confirm your API keys and internet connection.
- **No audio output**: Confirm PulseAudio is running and HDMI sink is active:
  ```bash
  pactl info
  pactl list sinks short
  pactl set-sink-mute alsa_output.platform-107c706400.hdmi.hdmi-stereo 0
  pactl set-sink-volume alsa_output.platform-107c706400.hdmi.hdmi-stereo 100%
  ```

See [PulseAudio docs](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/) for more.

---

## Future Enhancements

Here are some cool ideas to take RizzWave to the next level:

- **Multi-Language Support**: Add support for multiple languages to reach a global audience.
- **Voice Customization**: Let users pick or tweak the AI’s voice—think pitch sliders or custom voice synthesis.
- **Hardware Integration**: Design a retro ham radio-inspired case with physical knobs for volume, theme switching, or frequency vibes.
- **Advanced Intent Recognition**: Upgrade to cutting-edge NLP models for better intent handling and conversational depth.
- **User Profiles**: Save preferences, chat history, and settings per user for a personalized experience.
- **API Expansion**: Hook into APIs for news, sports scores, stock updates, or even ham radio frequency data.
- **Voice Commands for System Control**: Say "Switch to Fallout" or "Turn up the volume" to control the system hands-free.
- **Interactive Storytelling**: Build voice-driven games or stories—like a post-apocalyptic radio drama where users make choices.
- **Community Themes**: Let users upload and share themes on a public repo, growing a RizzWave creator community.
- **AI DJ Mode**: Have the AI curate and narrate a playlist based on weather, mood, or theme, with radio-style transitions.
- **Ham Radio Bridge**: Connect to real ham radio networks, blending vintage comms with AI responses.

---

## Contributing

Fork the repo, add themes, or tweak features—pull requests are welcome! For big changes, open an issue to chat about it first.

---

## Disclaimer

This is a fun, experimental project—not for production use. It relies on third-party APIs and may need tweaks for different hardware.
