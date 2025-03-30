import requests
import utils.consts as consts

from bs4 import BeautifulSoup

def transcript_webpage(url, id):
    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and clean text
        text = soup.get_text(separator="\n", strip=True)

        with open(consts.DIRECTORY_ASSETS + str(id) + ".wbt", "w", encoding="utf-8") as file: 
            file.write(str(text))
    else:
        print("Failed to retrieve the page:", response.status_code)