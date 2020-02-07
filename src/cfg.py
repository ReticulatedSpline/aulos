import os

# music controls: [P]lay, P[a]use, [N]ext, [L]ast

# directories
music_dir = "music"
playlist_dir = "playlists"

# text strings
homescreen_title_str = u'☭'
no_media_str = "Nothing playing."
no_load_str = "..."
song_sep_str = " by "
time_sep_str = " of "
home_menu_items = [
    "playlists",
    "albums",
    "artists",
    "genres",
    "tracks",
    "queue",
    "settings",
    "quit"
]

# file types to scan for
file_types = {'.mp3', '.flac'}

# progress bar filler
prog_fill = '▒'
