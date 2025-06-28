import streamlit as st
import os
import time
from lyrics_fetcher import LyricsFetcher
from wordcloud_generator import WordCloudGenerator

# Configure Streamlit page
st.set_page_config(
    page_title="Taylor Swift Lyrics Word Cloud Generator",
    page_icon="🎵",
    layout="wide"
)

@st.cache_resource
def get_lyrics_fetcher():
    return LyricsFetcher()

@st.cache_resource
def get_wordcloud_generator():
    return WordCloudGenerator()

def main():
    # ✅ Get API key from Streamlit Cloud secrets
    try:
        api_key = st.secrets["GENIUS_API_KEY"]
    except KeyError:
        st.error("❌ Genius API key not found in Streamlit secrets.")
        st.stop()

    st.title("🎵 Taylor Swift Lyrics Word Cloud Generator")
    st.markdown("Enter a Taylor Swift song title to fetch lyrics and generate a beautiful word cloud!")

    # Session state
    if 'lyrics' not in st.session_state:
        st.session_state.lyrics = None
    if 'song_title' not in st.session_state:
        st.session_state.song_title = ""
    if 'last_searched' not in st.session_state:
        st.session_state.last_searched = ""

    lyrics_fetcher = get_lyrics_fetcher()
    wordcloud_generator = get_wordcloud_generator()

    # Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🔍 Song Search")
        song_input = st.text_input(
            "Enter Taylor Swift song title:",
            value=st.session_state.song_title,
            placeholder="e.g., Shake It Off, Love Story"
        )
        search_clicked = st.button("🎵 Fetch Lyrics", type="primary")

        if search_clicked and song_input.strip():
            st.session_state.song_title = song_input.strip()

            if st.session_state.song_title != st.session_state.last_searched:
                with st.spinner(f"Searching for '{st.session_state.song_title}'..."):
                    try:
                        lyrics = lyrics_fetcher.fetch_lyrics(st.session_state.song_title)
                        if lyrics:
                            st.session_state.lyrics = lyrics
                            st.session_state.last_searched = st.session_state.song_title
                            st.success("✅ Lyrics found!")
                            st.rerun()
                        else:
                            st.error("❌ No lyrics found.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.session_state.lyrics = None
        elif search_clicked:
            st.warning("⚠️ Please enter a song title.")

    with col2:
        st.subheader("📊 Word Cloud Options")
        max_words = st.slider("Maximum words", 50, 200, 100)
        width = st.slider("Width", 400, 800, 600)
        height = st.slider("Height", 300, 600, 400)
        background_color = st.selectbox("Background color", ["white", "black", "lightpink"])
        colormap = st.selectbox("Color scheme", ["viridis", "plasma", "cool", "spring", "autumn"])

    if st.session_state.lyrics:
        st.markdown("---")
        tab1, tab2 = st.tabs(["📝 Lyrics", "☁️ Word Cloud"])

        with tab1:
            st.text_area("Lyrics", value=st.session_state.lyrics, height=400, disabled=True)

        with tab2:
            if st.button("🎨 Generate Word Cloud", type="primary"):
                with st.spinner("Generating..."):
                    try:
                        fig = wordcloud_generator.generate_wordcloud(
                            st.session_state.lyrics,
                            max_words=max_words,
                            width=width,
                            height=height,
                            background_color=background_color,
                            colormap=colormap
                        )
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Word cloud error: {str(e)}")

if __name__ == "__main__":
    main()
