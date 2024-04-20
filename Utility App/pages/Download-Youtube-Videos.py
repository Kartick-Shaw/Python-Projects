from pytube import YouTube
import streamlit as st

st.title(":red[Download Youtube Videos]")

link = st.text_input("Paste video link: ")
resolution = st.selectbox('Select Resolutions: ',
                          ('720p', '480p', '360p', '240p', '144p'))
get_button = st.button('Get Video')
st.subheader('',divider='red')

if get_button and link and resolution:
    youtubeObj = YouTube(link)
    st.write('Searching the Video...')
    video_stream = youtubeObj.streams.get_by_resolution(resolution=resolution)
    if video_stream:
        try:
            thumb = youtubeObj.thumbnail_url
            st.image(thumb, width=400)
            st.markdown(f'<h3 style="color:red;">{youtubeObj.title}</h3>', unsafe_allow_html=True)
            
            video_stream.download(filename='NewVideo.mp4')
            with open('NewVideo.mp4', 'rb') as video:
                video_bytes = video.read() 

            st.download_button(
                label='Download video',
                data=video_bytes,
                file_name=f'{youtubeObj.title}.mp4',
                mime='application/mp4'
            )    
        except:
            st.warning("An error has occurred during download")
    else:
        st.warning(f"No {resolution} stream available for download.")