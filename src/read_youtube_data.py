import json
import youtube_utils
import consts

from pytube import Playlist

with (open("./config/youtube_import_list.json")) as file:
    data = json.load(file)

# Lendo os vídeos cadastrados no arquivo
for item in data["videos"]:
    youtube_utils.transcript_youtube_video(item)

    print("Video transcrito: ", item)


# Buscando as playlists cadastradas no arquivo
for playlist_item in data["playlists"]:
    playlist = Playlist(consts.YOUTUBE_READ_PLAYLIST + playlist_item)

    print("Lendo playlist: ", playlist_item)

    video_urls = playlist.video_urls

    print(" Total de videos: ", len(video_urls))

    for video in video_urls:
        youtube_utils.transcript_youtube_video(video.replace(consts.YOUTUBE_READ_VIDEO, ""))

        print("     Video transcrito: ", video)