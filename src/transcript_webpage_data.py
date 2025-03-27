import json
import utils.webpage_utils as webpg

with (open("./config/web_import_list.json")) as file:
    data = json.load(file)

increment = 0

for item in data["pages"]:
    webpg.transcript_webpage(item, increment)

    increment += 1