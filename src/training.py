import os
import utils.consts as consts
import utils.assets_import as imports

fileList = [f for f in os.listdir(consts.DIRECTORY_ASSETS) if ((f.lower().endswith(".pdf")) or (f.lower().endswith(".ytb")) or (f.lower().endswith(".docx")) or (f.lower().endswith(".wbt")) or (f.lower().endswith(".mp4t"))) ]

imports.config_retriever(fileList)