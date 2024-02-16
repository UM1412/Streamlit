import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from googletrans import Translator
from gtts import gTTS
from tempfile import NamedTemporaryFile
from streamlit_option_menu import option_menu
import json
import time

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

def translate_to_hindi(text,dest):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=dest)
    return translated_text.text

def convert_to_audio(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    temp_file = NamedTemporaryFile(delete=False)
    tts.save(temp_file.name)
    return temp_file.name

def cool_title(title_text):
    st.markdown(
        f"""
        <div style="background-color:#f63366;padding:10px;border-radius:10px;font-family: 'Times New Roman', Times, serif;">
        <h1 style="color:white;text-align:center;">{title_text}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

def slider(images, slider_value):
    image_placeholder = st.empty()

    while True:
        if slider_value < len(images)-1:
            slider_value += 1
        else:
            slider_value = 0

        image_placeholder.image(images[slider_value], use_column_width=True)
        time.sleep(2)  # Change image every 2 seconds
        image_placeholder.empty()

def main():
    cool_title("Avinashi")
    st.header("Your Study App")
    selected = option_menu(menu_title = "Menu",
                options = ["English Notes","Hindi Notes","Tribute","Punjabi Notes","Marathi Notes"],
                #icons = ["File text fill","File text fill"],
                menu_icon = "Emoji sunglasses fill",
                default_index = 2,
                                orientation = "horizontal"
                )
    if selected == "Tribute":
        images = [
        "Slider/01.jpg",
        "Slider/02.jpg",
        "Slider/03.jpg",
        "Slider/04.jpg",
        "Slider/05.jpg",
        "Slider/06.jpg",
        "Slider/07.jpg",
    ]   
        st.header("_Education is the best friend. An educated person is respected everywhere.Education beats the beauty and the youth._")
        slider_value = st.slider("||जय माँ सरस्वती||", 0, 6, 0, 1)
        slider(images, slider_value)

        
        

    else:
        youtube_link = st.text_input("Enter YouTube Video ID:", value='', key='youtube_link')

        if st.button("Process"):
            st.image(f"http://img.youtube.com/vi/{youtube_link}/0.jpg", use_column_width=True)
            if youtube_link:
                with st.spinner("Processing your request..."):
                    # Call function to extract transcript
                    transcript = extract_transcript(youtube_link)


                    if transcript:
                        st.success("Transcript extracted successfully!")
                        summary = enhance_transcript(transcript)
                        translate = translate_to_hindi(transcript,"hi")
                        translate_01 = translate_to_hindi(transcript,"pa")
                        translate_02 = translate_to_hindi(transcript,"mr")
                        st.divider()
                        # First tab - Summary
                        if selected == "English Notes":
                            tabs = st.tabs(["Detailed Notes", "Summery Notes",])
                            with tabs[0]:
                                st.markdown("<div class='header'>Detailed Written Notes:</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='markdown-text'>{transcript}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Detailed Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(transcript), format='audio/mp3')
                                st.divider()
                            with tabs[1]:
                                st.markdown("<div class='header'>Summary Written Notes:</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='markdown-text'>{summary}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Summary Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(summary), format='audio/mp3')
                                st.divider()

                        # Second tab - Hindi translation
                        if selected == "Hindi Notes":
                            tabs = st.tabs(["Detailed Notes", "Summery Notes",])
                            with tabs[0]:
                                st.markdown("<div class='header'>Detailed Notes:</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='markdown-text'>{translate}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Detailed Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(translate), format='audio/mp3')
                                st.divider()
                            with tabs[1]:
                                st.markdown("<div class='header'>Summary Written Notes:</div>", unsafe_allow_html=True)
                                transcript_hindi = translate_to_hindi(summary,"hi")
                                st.markdown(f"<div class='markdown-text'>{transcript_hindi}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Summary Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(transcript_hindi, lang='hi'), format='audio/mp3')
                                st.divider()
                        if selected == "Punjabi Notes":
                            tabs = st.tabs(["Detailed Notes", "Summery Notes",])
                            with tabs[0]:
                                st.markdown("<div class='header'>Detailed Notes:</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='markdown-text'>{translate_01}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Detailed Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(translate_01), format='audio/mp3')
                                st.divider()
                            with tabs[1]:
                                st.markdown("<div class='header'>Summary Written Notes:</div>", unsafe_allow_html=True)
                                transcript_panj = translate_to_hindi(summary,"pa")
                                st.markdown(f"<div class='markdown-text'>{transcript_panj}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Summary Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(transcript_panj), format='audio/mp3')
                                st.divider()
                        if selected == "Marathi Notes":
                            tabs = st.tabs(["Detailed Notes", "Summery Notes",])
                            with tabs[0]:
                                st.markdown("<div class='header'>Detailed Notes:</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='markdown-text'>{translate_02}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Detailed Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(translate_02), format='audio/mp3')
                                st.divider()
                            with tabs[1]:
                                st.markdown("<div class='header'>Summary Written Notes:</div>", unsafe_allow_html=True)
                                transcript_mra = translate_to_hindi(summary,"mr")
                                st.markdown(f"<div class='markdown-text'>{transcript_mra}</div>", unsafe_allow_html=True)
                                st.divider()
                                st.markdown("<div class='header'>Summary Audio Notes:</div>", unsafe_allow_html=True)
                                st.audio(convert_to_audio(transcript_mra), format='audio/mp3')
                                st.divider()
                    else:
                        st.error("Failed to extract transcript. Please check the video link.")

if __name__ == "__main__":
    main()
