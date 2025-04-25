import json
import random

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"{self.title} by {self.artist}"

    def to_dict(self):
        return {"title": self.title, "artist": self.artist}

    @staticmethod
    def from_dict(data):
        return Song(data["title"], data["artist"])


class MoodPlaylist:
    def __init__(self, mood):
        self.mood = mood
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def get_random_song(self):
        return random.choice(self.songs) if self.songs else None

    def to_dict(self):
        return {
            "mood": self.mood,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        playlist = MoodPlaylist(data["mood"])
        playlist.songs = [Song.from_dict(s) for s in data["songs"]]
        return playlist


class MoodTunes:
    def __init__(self):
        self.playlists = {}
        self.load_data()

    def load_data(self, filename="moods.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    playlist = MoodPlaylist.from_dict(item)
                    self.playlists[playlist.mood] = playlist
        except FileNotFoundError:
            self.playlists = {}

    def save_data(self, filename="moods.json"):
        with open(filename, "w") as f:
            json.dump([p.to_dict() for p in self.playlists.values()], f, indent=4)

    def get_playlist(self, mood):
        return self.playlists.get(mood)

    def add_song_to_mood(self, mood, song):
        if mood not in self.playlists:
            self.playlists[mood] = MoodPlaylist(mood)
        self.playlists[mood].add_song(song)

    def recommend_song(self, mood):
        playlist = self.get_playlist(mood)
        if playlist:
            return playlist.get_random_song()
        return None

    def run(self):
        print("🎵 Welcome to MoodTunes — your mood-based music buddy!")
        while True:
            print("\n1. Recommend Song\n2. Add Song\n3. Show Moods\n4. Save & Exit")
            choice = input("Choose: ")

            if choice == "1":
                mood = input("Enter your mood: ").lower()
                song = self.recommend_song(mood)
                if song:
                    print(f"\n🎶 Try this: {song}")
                else:
                    print("😕 No songs found for that mood. Add some first!")

            elif choice == "2":
                mood = input("Enter mood to add to: ").lower()
                title = input("Song title: ")
                artist = input("Artist: ")
                self.add_song_to_mood(mood, Song(title, artist))
                print("✅ Song added!")

            elif choice == "3":
                if not self.playlists:
                    print("No moods yet.")
                for mood in self.playlists:
                    print(f"- {mood.capitalize()} ({len(self.playlists[mood].songs)} songs)")

            elif choice == "4":
                self.save_data()
                print("🎉 Saved! See you later.")
                break

            else:
                print("Invalid option. Try again.")

if __name__ == "__main__":
    app = MoodTunes()
    app.run()
