import os
from tinytag import TinyTag


def init_music():
    music_dir = 'C:\\Users\\Lakshmi\\Music\\Trial Music'
    song_list = os.listdir(music_dir)
    song_info = []
    for song in song_list:
        song_path = music_dir + '\\' + song
        tag = TinyTag.get(song_path)
        album = tag.album.lower()
        artist = tag.artist.lower()
        name = tag.title.lower()
        song_detail = {name: 'name', album: 'album', artist: 'artist'}
        song_info.append(song_detail)
    return song_info

