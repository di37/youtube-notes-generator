import os
import streamlit as st

from custom_logger import logger
from yt_notes_generator import generate_notes_audio
from utils import TUTORIAL_ONLY, CLASS_LECTURE

st.set_page_config(page_title="▶️ YouTube Audio Notes Generator", page_icon="🎵📝")

st.title("▶️ YouTube Notes Generator 📝")
st.markdown("Transform your YouTube videos into detailed notes with AI! 🚀")

# Initialize session state
if "generated_notes" not in st.session_state:
    st.session_state.generated_notes = ""
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# Sidebar inputs
with st.sidebar:
    st.header("📊 Input Parameters")
    youtube_url = st.text_input(
        "🔗 YouTube URL", placeholder="Paste your YouTube URL here..."
    )
    model_name = st.selectbox(
        "🤖 Model Name", ["gemini-1.5-pro", "gemini-1.5-flash"]
    )

    system_prompt = st.selectbox(
        "💬 System Prompt", ["tutorial-only", "class-lecture", "custom"]
    )
    if system_prompt == "tutorial-only":
        system_prompt = TUTORIAL_ONLY
    elif system_prompt == "class-lecture":
        system_prompt = CLASS_LECTURE
    elif system_prompt == "custom":
        system_prompt = st.text_area(
            "✏️ Custom System Prompt", "You are a helpful assistant."
        )

    user_prompt = st.text_area(
        "🗨️ User Prompt", "Please generate notes for this audio."
    )

    generate_button = st.button("🚀 Generate Notes", use_container_width=True)

    if st.session_state.show_download:
        st.download_button(
            label="📥 Download Notes as MD",
            data=st.session_state.generated_notes,
            file_name="notes.md",
            mime="text/markdown",
            use_container_width=True,
        )

# Main content area
st.header("📄 Generated Notes")
if generate_button:
    if youtube_url and model_name and system_prompt and user_prompt:
        with st.spinner("🔄 Generating notes... Please wait."):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in generate_notes_audio(
                youtube_url=youtube_url,
                model_name=model_name,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            ):
                full_response += chunk.text
                response_placeholder.markdown(full_response)

        logger.info("Response successfully generated.")


        # Store generated notes in session state and show download button
        st.session_state.generated_notes = full_response
        st.session_state.show_download = True
        st.rerun()  # Rerun the app to update the sidebar

# Always display the generated notes if they exist
if st.session_state.generated_notes:
    st.markdown(st.session_state.generated_notes)
else:
    st.info("👆 Click 'Generate Notes' in the sidebar to start the process!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Isham Rashik | [GitHub](https://github.com/di37)")
