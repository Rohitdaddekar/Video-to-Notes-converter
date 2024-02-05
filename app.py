import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # load all the environment variables
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure Google Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 250 words. Please provide the summary of the text given here:  """

prompt = """
You are a sophisticated YouTube video summarizer powered by Gemini Pro. Your task is to analyze the provided transcript text 
and generate a concise summary of the entire video, highlighting key points and insights. Your summary should capture the essence 
of the content within 250 words. Please provide a well-structured and informative summary based on the given transcript:

[Insert Transcript Here]
"""

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join(i["text"] for i in transcript_text)
        return transcript

    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App Design
st.set_page_config(
    page_title="YouTube Transcript Summarizer",
    page_icon=":clapper:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Video to Notes Converter")
youtube_link = st.sidebar.text_input("Enter YouTube Video Link:")
if st.sidebar.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.sidebar.success("Summary Generated!")

# Main Content
st.title("YouTube Transcript to Detailed Notes Converter")
st.markdown(
    """
    <style>
        .title {
            color: #3498db;  /* Blue color */
        }
    </style>
""",
    unsafe_allow_html=True,
)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(
        f"http://img.youtube.com/vi/{video_id}/0.jpg",
        use_column_width=True,
        caption="YouTube Video Thumbnail",
    )

if 'transcript_text' in locals():
    st.markdown("## Detailed Notes:")
    st.info(summary if 'summary' in locals() else "Please click 'Get Detailed Notes'.")