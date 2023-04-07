import os
import requests

# Configuration options
API_KEY = os.environ["MUSIXMATCH_API_KEY"]
ARTIST = "Parcels"  # Replace with your desired artist
TITLE = "Tieduprightnow"  # Replace with your desired song title

BASE_URL = "https://api.musixmatch.com/ws/1.1/"



def get_lyrics(artist: str, title: str) -> str:
    search_url = f"{BASE_URL}track.search?format=json&callback=callback&q_artist={artist}&q_track={title}&quorum_factor=1&apikey={API_KEY}"
    response = requests.get(search_url)
    track_data = response.json()
    print(track_data)

    if track_data["message"]["header"]["execute_time"] > 0:
        try:
            track_id = track_data["message"]["body"]["track_list"][0]["track"]["track_id"]
        except (IndexError, KeyError, TypeError) as e:
            return f"Error occurred while parsing track data: {e}"

        lyrics_url = f"{BASE_URL}track.lyrics.get?format=json&callback=callback&track_id={track_id}&apikey={API_KEY}"
        response = requests.get(lyrics_url)
        lyrics_data = response.json()

        if lyrics_data["message"]["header"]["status_code"] == 200:
            return lyrics_data["message"]["body"]["lyrics"]["lyrics_body"]
        else:
            return "Lyrics not found"
    else:
        return "Track not found"

def main():
    # Use the configured artist and title
    artist = ARTIST
    title = TITLE
    print("The API Key is " + API_KEY)

    lyrics = get_lyrics(artist, title)
    print("\nLyrics:\n")
    print(lyrics)

if __name__ == "__main__":
    main()

