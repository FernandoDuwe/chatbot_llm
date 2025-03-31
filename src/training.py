import os
import utils.consts as consts
import utils.assets_import as imports

fileListSpc = [f for f in os.listdir(consts.DIRECTORY_ASSETS) if ((f.lower().endswith(".pdf")) or (f.lower().endswith(".docx")) or (f.lower().endswith(".mp4t"))) ]
fileListDev = [f for f in os.listdir(consts.DIRECTORY_ASSETS) if ((f.lower().endswith(".ytb")) or (f.lower().endswith(".wbt")) ) ]

imports.config_retriever(fileListSpc, consts.PROFILE_SPECIALIST)

imports.config_retriever(fileListDev, consts.PROFILE_DEVELOPER)