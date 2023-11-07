import streamlit as st
from pathlib import Path
import openai
import os
import base64

# Streamlit app
def main():
    st.title("Text-to-Speech App")

    # Prompt user for OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key", type="password")

    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        st.stop()

    # Initialize OpenAI client
    openai.api_key = api_key

    # Text input and voice selection
    text_input = st.text_area("Enter text to convert to speech")
    voice = st.selectbox("Select Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

    # Placeholder for displaying audio player and download link
    audio_placeholder = st.empty()

    if st.button("Convert to Speech"):
        if text_input:
            # Make a request to the OpenAI Audio API
            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text_input
            )

            # Save the response audio file
            #current_directory = os.getcwd()
            #speech_file_path = Path(current_directory) / "speech.mp3"
            #with open(speech_file_path, "wb") as audio_file:
                #audio_file.write(response.content)

            # Display the audio file in the app with HTML audio tag
            audio_html = f'<audio controls controlsList="nodownload"><source src="data:audio/mp3;base64,{base64.b64encode(response.content).decode()}" type="audio/mp3"></audio>'
            audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

            # Allow the user to download the audio file using a separate link
            st.markdown(get_binary_file_downloader_html("speech.mp3", 'Download Audio'), unsafe_allow_html=True)
        else:
            st.warning("Please enter text to convert.")

    # Check if audio file exists, then display the audio player
    if os.path.exists("speech.mp3"):
        audio_html = f'<audio controls controlsList="nodownload"><source src="data:audio/mp3;base64,{base64.b64encode(open("speech.mp3", "rb").read()).decode()}" type="audio/mp3"></audio>'
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

# Function to create a download link for a file
def get_binary_file_downloader_html(file_path, file_label='File'):
    with open(file_path, 'rb') as file:
        data = file.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_path}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
