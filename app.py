import streamlit as st
import os
import tempfile
import edge_tts
import asyncio
from groq import Groq
from dotenv import load_dotenv
import time
import json
from audio_recorder_streamlit import audio_recorder
import requests


load_dotenv()

knowledge_base = """
I am Abhyudya Bhatnagar. I'm a final year student at IIIT Nagpur, majoring in Computer Science with a focus on AI and Machine Learning. 

MY LIFE STORY:
I grew up with a passion for technology and problem-solving. At IIIT Nagpur, I've actively explored AI/ML through research, internships, and hackathons. I'm currently interning at Friska.AI where I built a fully duplex Conversational AI pipeline (sub-200ms latency), fine-tuned LLMs for personalized meal plans, and engineered a dual LLM pipeline for data generation. My love for music began early—I've been playing piano for [X years], blending technical precision with emotional expression. My aviation interest began when [add your story]. I've completed hands-on projects like RAG-based QA systems, document summarization tools, and model distillation experiments. I've also interned at Procohat, working with PowerBI and SAP ABAP to virtualize 7+ years of data.

MY #1 SUPERPOWER:
My biggest strength is breaking down complex problems into structured, manageable parts. I also have a knack for building end-to-end systems that fuse research-level ideas with practical deployment, and I quickly learn unfamiliar tools and frameworks.

TOP 3 AREAS I'D LIKE TO GROW IN:
1. Advanced machine learning research and contributing to impactful, open-source AI projects.
2. Leadership skills and managing cross-functional AI/ML teams.
3. Advanced piano techniques and music composition for digital platforms.

COMMON MISCONCEPTIONS ABOUT ME:
People often assume that because I'm into AI and hardcore tech, I'm not creative. But I actually thrive on artistic expression—whether it's through music or designing intuitive UIs (like the Gradio front-end I developed for a question generation app). Some think I'm all about code, but I enjoy collaborative ideation, hackathons, and spending time understanding human behavior.

HOW I PUSH MY BOUNDARIES:
I constantly challenge myself with real-world, time-bound projects—like building a personalized meal planning engine or fine-tuning DistilBERT to extract keywords from news articles. I push limits through hackathons (top 5 at IISc OpenHack'24, winner at TantraFiesta'24), intense learning curves (like distilling BERT to DistilBERT with custom loss functions), and exploring new fields (like virtual datalake architecture or real-time disease detection with ESP32-CAM). I believe that growth comes from combining curiosity with execution.

ADDITIONAL PERSONAL INFO:
- Favorite programming languages: Python, C++
- Current projects I'm working on: Building a VTON (Virtual Try-On) model for Indian traditional wear.
- Dream job/career goal: To work on AI/ML projects that directly improve lives through personalization, accessibility, and automation.
- Interesting fact: I learn new tools and concepts incredibly fast—my projects span ASR pipelines, Qdrant vector stores, and Azure-based dashboards.
- Approach to problem-solving: Deconstruct, analyze, prototype, test, and optimize. I thrive on iterative design.
- What excites me most about AI/ML: Its power to understand, generate, and interact with humans in meaningful ways.
- My musical influences/favorite pieces: Eclectic taste—classical, electronic, Indian folk, and cinematic scores.
- My aviation interests: Fascinated by how large aircraft are designed and engineered, especially control systems and structural optimization.

HACKATHON WINS:
-  **Analytica '24 Winner**: Built an LLM app that generates & validates questions from PDFs using Mistral 7B + Gradio UI.
-  **MarketWise '24 Winner**: Created a recommendation engine with Gemma-2B, data generation, and predictive analytics (SciKitLearn).
-  **OpenHack '24 Finalist** (Top 5 of 1800+ teams): Summify News App using fine-tuned BERT and DistilBERT.
-  **TantraFiesta '23 Runner-Up**: Plant Disease Detection using ResNet50 and ESP32-CAM (97% accuracy).

SELECTED PROJECTS:
- **DocuMind** (Feb 2025): AI-powered document QA using RAG + Gemma2 27B + Qdrant. Reduced manual search time by 50%.
- **Knowledge Distillation Implementation** (Jan 2025): BERT → DistilBERT, 40% size reduction, 94.4% accuracy in 10 epochs.
- **Resume Scoring App**: Evaluates resumes based on job description matching and keyword extraction.
- **Summify Browser Extension**: Summarizes news articles with keyword suggestions and fast load times (Chrome/Firefox).

TECH STACK:
- Languages: Python, C++, Java, C, ABAP, HTML/CSS, JavaScript, SQL, PL-SQL, NoSQL
- Tools/Platforms: Jupyter, PowerBI, VS Code, Eclipse, GCP, Android Studio, MongoDB
- Frameworks/Tech: AWS, Azure, Transformers, Docker, Kubernetes, WordPress, Git, Jenkins

WORK EXPERIENCE:

🔹 **Gen AI Intern – Friska.AI** (March 2025 – Present) | Kochi, Kerala
- Engineered a **fully duplex Conversational AI pipeline** with STT, ASR, and TTS modules achieving **<200ms latency**.
- Fine-tuned **multiple LLMs** to generate **personalized meal plans** using user input + medical metadata.
- Built a **dual-model QA pipeline** (question generator + answer model) which **5× data throughput** and reduced manual intervention by **80%**.
- Conducted **web scraping** to create datasets from multiple sources for internal model training.

🔹 **Developer Intern – Procohat** (June 2024 – August 2024) | Nagpur, Maharashtra
- Developed **interactive PowerBI dashboards** for real-time insights, boosting decision-making efficiency and user engagement.
- Utilized **SAP ABAP** to migrate 7+ years of physical data into a **virtual datalake**, increasing accessibility by 25% and improving scalability.
"""



client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="centered"
)


st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .chat-message {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)


if 'messages' not in st.session_state:
    st.session_state.messages = []

def save_audio(audio_bytes):
    """Save audio bytes to temporary file"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        return temp_file.name

def transcribe_audio(audio_file):
    """Transcribe audio using Groq Whisper via raw HTTP request"""
    try:
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        }

        with open(audio_file, "rb") as f:
            files = {
                "file": (os.path.basename(audio_file), f, "audio/wav"),
                "model": (None, "whisper-large-v3-turbo"),
                "response_format": (None, "text"),
                "temperature": (None, "0.0"),
                "language": (None, "en")
            }

            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            return response.text.strip()
        else:
            st.error(f"Error from Groq Whisper API: {response.text}")
            return None

    except Exception as e:
        st.error(f"Exception during transcription: {str(e)}")
        return None

async def speak_text(text):
    """Convert text to speech and play it using Edge TTS"""
    try:
        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        await communicate.save("response.mp3")
        st.audio("response.mp3", autoplay=True)
        
        os.remove("response.mp3")
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")

def get_ai_response(prompt):
    """Get response from Groq API"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful and friendly AI assistant. Respond naturally and conversationally. You will only answer from the context of the conversation. You will only answer from your knowledge base which is demarkated by triple backticks : ```{knowledge_base}```"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"


st.title("🎙️ AI Voice Assistant")
st.markdown("Click the microphone button below to start recording your question.")


audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e74c3c",
    neutral_color="#3498db",
    icon_name="microphone",
    icon_size="2x",
)

if audio_bytes:
    
    audio_file = save_audio(audio_bytes)
    
    
    st.audio(audio_bytes, format="audio/wav")
    
    
    with st.spinner("Transcribing your speech..."):
        transcription = transcribe_audio(audio_file)
    
    if transcription:
        st.markdown(f'<div class="chat-message user-message">You said: {transcription}</div>', unsafe_allow_html=True)
        
        with st.spinner("Thinking..."):
            response = get_ai_response(transcription)
            st.session_state.messages.append({"role": "user", "content": transcription})
            st.session_state.messages.append({"role": "assistant", "content": response})
            asyncio.run(speak_text(response))
        
        os.unlink(audio_file)


st.markdown("### Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message">Assistant: {message["content"]}</div>', unsafe_allow_html=True)


st.markdown("""
### How to use:
1. Click the microphone button to start recording
2. Speak your question
3. Click the button again to stop recording
4. Wait for the AI to process and respond
5. Listen to the AI's voice response
""") 