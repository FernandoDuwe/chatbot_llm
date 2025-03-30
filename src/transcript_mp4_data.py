import os

import utils.consts as consts
import utils.mp4_utils as mp4
import whisper


model = whisper.load_model("small")  

mp4_files = [f for f in os.listdir(consts.DIRECTORY_TEMP) if f.lower().endswith(".mp4")]

for item in mp4_files:
    mp4.transcript_mp4(item, model)