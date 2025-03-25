import consts

import os
import io
import getpass
from langchain_community.document_loaders import YoutubeLoader
import yt_dlp

def transcript_youtube_video(videoId):
    video_loader = YoutubeLoader.from_youtube_url(consts.YOUTUBE_READ_VIDEO + videoId, language = ["pt", "pt-BR", "en"],)

    infos = video_loader.load()

    with open(consts.DIRECTORY_ASSETS + videoId + ".txt", "w", encoding="utf-8") as file: 
        file.write(str(infos))

def youtube_get_title(videoId):
    video_title = videoId

    url = consts.YOUTUBE_READ_VIDEO + videoId

    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)

    return video_title