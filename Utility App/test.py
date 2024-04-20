from pytube import YouTube
import streamlit as st

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    # youtubeObject.default_filename('video')
    try:
        youtubeObject.download(filename='newVideo.mp4')
    except:
        print("An error has occurred")
    print("Download is completed successfully")


# link = input("Enter the YouTube video URL: ")

Download("https://youtu.be/0KGP9f3duEg?feature=shared")