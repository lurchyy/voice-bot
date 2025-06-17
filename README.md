# AI Voice Assistant

A voice-enabled AI assistant built with Streamlit, Groq, and Edge TTS.

## Features

- Voice recording using audio-recorder-streamlit
- Speech-to-text using Groq's Whisper model
- AI responses using Groq's LLM
- Text-to-speech using Edge TTS
- Chat history display
- Beautiful and responsive UI

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your-groq-api-key-here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (app.py)
6. In the "Secrets" section, add your API keys:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
7. Click "Deploy"

## Environment Variables

- `GROQ_API_KEY`: Your Groq API key for speech-to-text and AI responses

## Dependencies

- streamlit==1.31.1
- groq==0.4.2
- edge-tts==6.1.9
- python-dotenv==1.0.0
- audio-recorder-streamlit==0.0.5
- requests==2.31.0

## Project Structure

```
voice-bot/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Local environment variables
├── .streamlit/        # Streamlit configuration
│   └── secrets.toml   # Streamlit Cloud secrets
└── README.md          # Project documentation
```

## Usage

1. Click the microphone button to start recording
2. Speak your question
3. Click the button again to stop recording
4. Wait for the AI to process and respond
5. Listen to the AI's voice response

## License

MIT License 