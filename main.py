import os
import webbrowser
import requests
import google.generativeai as genai
import schedule
import time

newsapi = "YOUR_API_KEY"

def show_news(newsapi, country='in'):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': newsapi,
        'country': country,
        'pageSize': 100
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        news_list = [
            {
                'title': article.get('title'),
                'url': article.get('url')
            }
            for article in articles
        ]
        return news_list
    else:
        print(f"Error: {response.status_code}")
        return None

def open_yt():
    webbrowser.open_new_tab("https://www.youtube.com")

def yt(args):
    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={args}")

def open_spotify():
    os.system(r'"PATH_TO_SPOTIFY.EXE"')


# user headers for spotify api
with open('access_token.txt', 'r') as f:
    token_file = (f.read())
token = token_file

user_headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}
# playback controls [play,pause,play previous, play next]
def pause_playback():
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers=user_headers)
    if response.status_code == 200:
        print("Playback paused successfully!")
    else:
        print(f"Error pausing playback: {response.status_code}, {response.text}")

def resume_playback():
    url = "https://api.spotify.com/v1/me/player/play"
    response = requests.put(url, headers=user_headers)
    if response.status_code == 200:
        print("Playback resumed successfully!")
    else:
        print(f"Error resuming playback: {response.status_code}")

def play_next(device_id):
    url = "https://api.spotify.com/v1/me/player/next"
    response = requests.post(url, headers=user_headers, json={"device_id": device_id})
    if response.status_code == 200:
        print("Next playback resumed successfully!")
    else:
        print(f"Error next playback: {response.status_code}")

def play_previous(device_id):
    url = "https://api.spotify.com/v1/me/player/previous"
    response = requests.post(url, headers=user_headers, json={"device_id": device_id})
    if response.status_code == 200:
        print("Previous playback resumed successfully!")
    else:
        print(f"Error previous playback: {response.status_code}")


def main():
    # news = show_news(newsapi)
    # if news:
    #     for article in news:
    #         print(f"Title: {article['title']}")
    #         print(f"URL: {article['url']}")
    #         print("\n")
    #         print('  -  ' * 80)
    #
    # open_spotify()
    # pause_playback()
    # resume_playback()
if __name__ == '__main__':
    main()
