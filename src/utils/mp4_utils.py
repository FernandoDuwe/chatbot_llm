import os
import utils.consts as consts

import moviepy as mp
import speech_recognition as sr
import sys
from pydub import AudioSegment

def transcript_mp4(prFilePath, prModel):
    vrNome, vrExtensao = os.path.splitext(prFilePath)

    vrFileMp3  = consts.DIRECTORY_TEMP + vrNome + ".mp3"
    vrFilemp4t = consts.DIRECTORY_ASSETS + vrNome + ".mp4t"

    #converter de mp4 para mp3
    clip = mp.VideoFileClip(consts.DIRECTORY_TEMP + prFilePath)

    clip.audio.write_audiofile(vrFileMp3, codec="libmp3lame", bitrate="192k")

    result = prModel.transcribe(vrFileMp3)

    with open(vrFilemp4t, "w", encoding="utf-8") as file: 
        file.write(result["text"])