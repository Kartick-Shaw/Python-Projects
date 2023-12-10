import streamlit as st
from pytube import YouTube

st.title("Youtube Downloader")

link = st.text_input("Enter your link")
resolution = st.selectbox("Resolution: ", ['1080p', '720p', '480p', '360p', '144p'])

if st.button('Get Video'):
    if link:
        youtubeObject = YouTube(link)
        thumb = youtubeObject.thumbnail_url
        st.image(thumb, width=400)
        st.write("Video Title: ", youtubeObject.title)
        st.session_state['video'] = youtubeObject
        st.session_state['resolution'] = resolution
        st.session_state['show_download_button'] = True

if st.session_state.get('show_download_button', False) and 'video' in st.session_state:
    yt = st.session_state['video']
    resolution = st.session_state['resolution']
    
    video_stream = yt.streams.get_by_itag(22)
    
    if video_stream:
        st.write("Your video is downloading...")
        try:
            video_stream.download()
            st.success("Download is completed successfully")
        except:
            st.warning("An error has occurred during download")
    else:
        st.warning(f"No {resolution} stream available for download.")
