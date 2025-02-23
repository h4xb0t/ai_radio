# Fallout Terminal Developer Documentation - v1.4

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Architecture](#2-architecture)
- [3. Components](#3-components)
  - [Theme System](#theme-system)
  - [Audio Processing](#audio-processing)
  - [Key Event Handling](#key-event-handling)
  - [Error Handling](#error-handling)
- [4. Configurations](#4-configurations)
  - [Theme Configuration](#theme-configuration)
  - [Environment Variables](#environment-variables)
- [5. Installation and Setup](#5-installation-and-setup)
  - [Dependencies](#dependencies)
  - [Hardware Configuration](#hardware-configuration)
  - [Generating `silence.wav`](#generating-silencewav)
- [6. Usage](#6-usage)
  - [Running the Script](#running-the-script)
  - [Interacting with the Terminal](#interacting-with-the-terminal)
- [7. Development Guidelines](#7-development-guidelines)
  - [Adding New Themes](#adding-new-themes)
  - [Customizing Audio Settings](#customizing-audio-settings)
  - [Debugging Tips](#debugging-tips)
- [8. Troubleshooting](#8-troubleshooting)
- [9. Future Enhancements](#9-future-enhancements)

---

## 1. Project Overview

The **Fallout Terminal** is an interactive, voice-controlled AI assistant inspired by themed experiences (e.g., *Fallout*, *Barbie*, *Terminator*). Built in [Python](https://www.python.org/), it runs on a [Raspberry Pi](https://www.raspberrypi.org/) and leverages [OpenAI APIs](https://openai.com/api/) for **speech-to-text (STT)**, **text-to-text AI (ChatGPT)**, and **text-to-speech (TTS)**. The project supports a dynamic theme system, allowing developers to customize the AI's personality, voice, and behavior via JSON files.

This documentation equips developers with the knowledge to maintain, extend, and debug the application, serving as a comprehensive resource for both current and future contributors.

---

## 2. Architecture

The Fallout Terminal follows a modular design:

- **Theme System**: Loads configurations from JSON files in the `themes/` directory to define the AI’s personality and settings.
- **Audio Input**: Captures voice via [sounddevice](https://python-sounddevice.readthedocs.io/), transcribed using [Whisper](https://github.com/openai/whisper).
- **AI Interaction**: Processes transcriptions with [ChatGPT](https://openai.com/research/chatgpt) for themed responses.
- **Audio Output**: Converts responses to speech with OpenAI TTS, played via `paplay`.
- **Key Event Handling**: Uses the [keyboard](https://github.com/boppreh/keyboard) library to manage user interactions.

---

## 3. Components

### Theme System

- **Purpose**: Defines the AI’s personality, TTS voice, and STT model.
- **Implementation**: Each theme is a JSON file in `themes/` with the following structure:
  ```json
  {
      "theme_name": "Fallout",
      "system_message": "You are a gritty Fallout terminal AI.",
      "voice": "onyx",
      "intro_user_prompt": "Introduce yourself as a Fallout terminal.",
      "whisper_model": "tiny"
  }
  ```
- **Key Fields**:
  - `theme_name`: Unique identifier.
  - `system_message`: ChatGPT behavior prompt.
  - `voice`: TTS voice (e.g., "onyx", "nova").
  - `intro_user_prompt`: Generates the AI’s intro.
  - `whisper_model`: STT model (e.g., "tiny", "base").

### Audio Processing

- **Input**:
  - Captured using `sounddevice` (16,000 Hz sample rate, 512 block size).
  - Optimized with pre-allocated NumPy arrays.
- **Transcription**:
  - Processed by Whisper with configurable model sizes.
- **Output**:
  - Generated via OpenAI TTS and played with `paplay`, prefixed with `silence.wav` to minimize latency.

### Key Event Handling

- **Library**: `keyboard` (requires `sudo` for root privileges).
- **Controls**:
  - **Left Shift**: Start/stop recording.
  - `'q'`: Exit the application.

### Error Handling

- **Theme Validation**: Ensures JSON files include required fields and valid syntax.
- **API Resilience**: Handles OpenAI API failures with user-friendly feedback.

---

## 4. Configurations

### Theme Configuration

- **Location**: `themes/` directory.
- **Example**:
  ```json
  {
      "theme_name": "Terminator",
      "system_message": "You are a cold, calculating Terminator AI.",
      "voice": "alloy",
      "intro_user_prompt": "State your designation and purpose.",
      "whisper_model": "base"
  }
  ```

### Environment Variables

- **OpenAI API Key**:
  ```bash
  export OPENAI_API_KEY='your-api-key-here'
  ```

---

## 5. Installation and Setup

### Dependencies

- **Python Libraries**:
  ```bash
  pip install openai sounddevice numpy whisper keyboard
  ```
- **System Packages**:
  - Install `sox` for silence file generation:
    ```bash
    sudo apt install sox
    ```

### Hardware Configuration

- **Platform**: Raspberry Pi (configured for user `h4xb0t`).
- **Audio**: Requires [PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) for `paplay`.

### Generating `silence.wav`

- Create a 0.5-second silence file:
  ```bash
  sox -n -t wav silence.wav trim 0.0 0.5
  ```
- Place it in the script’s working directory.

---

## 6. Usage

### Running the Script

- Run with `sudo` to preserve environment variables:
  ```bash
  sudo -E /path/to/venv/bin/python terminal_v1.4.py
  ```
- Select a theme from the displayed menu.

### Interacting with the Terminal

- **Record**: Hold **Left Shift** (max 10 seconds).
- **Response**: Release to hear the AI’s themed reply.
- **Exit**: Press `'q'`.

---

## 7. Development Guidelines

### Adding New Themes

1. Create a new JSON file in `themes/` (e.g., `my_theme.json`).
2. Define the required fields:
   ```json
   {
       "theme_name": "my_theme",
       "system_message": "Your custom AI behavior.",
       "voice": "nova",
       "intro_user_prompt": "Your intro here.",
       "whisper_model": "tiny"
   }
   ```
3. The theme will automatically appear in the menu.

### Customizing Audio Settings

- Adjust `BLOCK_SIZE` (default: 512) or `SAMPLE_RATE` (default: 16,000 Hz) in the script:
  ```python
  BLOCK_SIZE = 256  # Example adjustment
  SAMPLE_RATE = 8000  # Example adjustment
  ```
- Ensure Whisper compatibility with the sample rate (16,000 Hz preferred).

### Debugging Tips

- **Audio Failures**: Verify microphone setup and PulseAudio functionality with:
  ```bash
  pactl info
  ```
- **API Issues**: Check API key validity and network status:
  ```bash
  echo $OPENAI_API_KEY
  ping api.openai.com
  ```
- **Transcription Errors**: Test alternative Whisper models by editing the theme JSON:
  ```json
  "whisper_model": "base"
  ```

---

## 8. Troubleshooting

- **"No audio captured"**: 
  - Ensure microphone is connected and Left Shift is held long enough.
  - Test with:
    ```bash
    arecord -f cd test.wav
    ```
- **"Invalid theme file"**: Validate JSON syntax and required fields with a linter (e.g., [JSONLint](https://jsonlint.com/)).
- **"API connection failed"**: Confirm API key and internet connectivity.

---

## 9. Future Enhancements

- **UI Feedback**: Add visual cues using ANSI escape codes for recording/processing states:
  ```python
  print("\033[31mRecording...\033[0m")  # Red text example
  ```
- **Dynamic Data**: Integrate external APIs (e.g., [OpenWeatherMap](https://openweathermap.org/api)) for real-time data.
- **Voice Flexibility**: Enable runtime voice selection via a config option.
- **Profiles**: Support per-user configurations with a JSON-based user database.

---
