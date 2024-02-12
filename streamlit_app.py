import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from googletrans import Translator
from gtts import gTTS
from tempfile import NamedTemporaryFile

def extract_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([t['text'] for t in transcript_list])
        return transcript
    except Exception as e:
        st.error("Failed to extract transcript. Please check the video link.")
        st.error(f"Error: {e}")
        return None

def enhance_transcript(transcript):
    summarizer = pipeline("summarization")
    enhanced_transcript = summarizer(transcript)[0]['summary_text']
    return enhanced_transcript

def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi')
    return translated_text.text

def convert_to_audio(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    temp_file = NamedTemporaryFile(delete=False)
    tts.save(temp_file.name)
    return temp_file.name

def main():
    st.markdown(
        """
        <style>
            body {
                background-image: url("https://mcdn.wallpapersafari.com/medium/29/56/ymaAeU.jpg");
                background-size: cover;
                font-family: Arial, sans-serif;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                color: #ff4500; /* Orange color */
                text-align: center;
                padding-top: 50px;
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #ff4500; /* Orange color */
                text-align: center;
                padding-top: 20px;
                padding-bottom: 20px;
            }
            .input {
                font-size: 18px;
                color: #ffffff;
                margin-bottom: 20px;
            }
            .button-container {
                display: flex;
                justify-content: center;
            }
            .button {
                font-size: 18px;
                color: #ffffff;
                background-color: #008080;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #005555;
            }
            .success {
                font-size: 18px;
                color: #00ff00;
            }
            .error {
                font-size: 18px;
                color: #ff0000;
            }
            .markdown-text {
                font-size: 16px;
                color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='title'>Avainishi</div>", unsafe_allow_html=True)
    st.subheader("Your Study App")

    youtube_link = st.text_input("Enter YouTube Video ID:", value='', key='youtube_link')

    if st.button("Process"):
        st.image(f"http://img.youtube.com/vi/{youtube_link}/0.jpg", use_column_width=True)
        if youtube_link:
            with st.spinner("Processing your request..."):
                # Call function to extract transcript
                transcript_text = extract_transcript(youtube_link)
                if transcript_text:
                    st.success("Transcript extracted successfully!")

                    # Add tabs
                    tabs = st.tabs(["Summary", "Hindi"])

                    # First tab - Summary
                    with tabs[0]:
                        st.markdown("<div class='header'>Summary Notes:</div>", unsafe_allow_html=True)
                        # Generate summary
                        transcript = enhance_transcript(transcript_text)
                        st.markdown(f"<div class='markdown-text'>{transcript}</div>", unsafe_allow_html=True)
                        # Convert to audio and play
                        st.audio(convert_to_audio(transcript), format='audio/mp3')

                    # Second tab - Hindi translation
                    with tabs[1]:
                        st.markdown("<div class='header'>Detailed Notes (in Hindi):</div>", unsafe_allow_html=True)
                        # Translate to Hindi
                        transcript_hindi = translate_to_hindi(transcript_text)
                        st.markdown(f"<div class='markdown-text'>{transcript_hindi}</div>", unsafe_allow_html=True)
                        # Convert to audio and play
                        st.audio(convert_to_audio(transcript_hindi, lang='hi'), format='audio/mp3')
                else:
                    st.error("Failed to extract transcript. Please check the video link.")

if __name__ == "__main__":
    main()
