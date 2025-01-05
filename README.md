# FlightAI - Intelligent Airline Assistant 🛫

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)](https://gradio.app/)

FlightAI is a cutting-edge airline customer support assistant that leverages artificial intelligence to provide an immersive and helpful travel experience. By combining natural language processing, image generation, and text-to-speech capabilities, it offers a multimodal interaction platform for airline customers.

## ✨ Features

- **🗣️ Natural Language Interface**: Engage in human-like conversations with the AI assistant for travel inquiries
- **💰 Real-time Pricing**: Get instant access to ticket prices for popular destinations
- **🎨 AI-Generated Visuals**: Experience destinations through AI-generated preview images
- **🔊 Voice Responses**: Receive information through natural text-to-speech audio responses
- **🌐 Multi-Modal Experience**: Seamlessly switch between text, image, and audio interactions

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg (required for audio processing)
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/flightai.git
cd flightai
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your environment:

- Copy the `.env.example` file to `.env`
- Add your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

4. Install FFmpeg:

- **macOS**:
  ```bash
  brew install ffmpeg
  ```
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Linux**:
  ```bash
  sudo apt-get install ffmpeg
  ```

## 🎯 Usage

Launch the application:

```bash
python app.py
```

The Gradio interface will automatically open in your default web browser, providing access to all features.

## 🛠️ Technical Stack

- **Frontend**: Gradio (Web Interface)
- **Backend**: Python
- **AI Services**: OpenAI GPT & DALL-E
- **Audio**: FFmpeg for speech synthesis
- **Environment**: Python dotenv for configuration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
