# AI Voice Assistant

A voice-enabled AI assistant built with Streamlit, Groq, and Edge TTS. This app lets you record your voice, transcribes it to text, generates AI responses, and speaks them back to you—all in a beautiful, interactive UI.

## Features

- Voice recording with audio-recorder-streamlit
- Speech-to-text using Groq's Whisper model
- AI chat responses using Groq LLM
- Text-to-speech with Edge TTS
- Chat history display
- Responsive, modern UI

## Getting Started

### Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your API key:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```


## Dependencies

- streamlit
- groq
- edge-tts
- python-dotenv
- audio-recorder-streamlit
- requests

## Project Structure

```
voice-bot/
├── app.py            # Main Streamlit app
├── requirements.txt  # Python dependencies
├── .env              # Local environment variables (not tracked)
└── README.md         # Project documentation
```

## Usage

1. Click the microphone button to start recording
2. Speak your question
3. Click again to stop recording
4. Wait for the AI to process and respond
5. Listen to the AI's voice reply

## License

MIT License