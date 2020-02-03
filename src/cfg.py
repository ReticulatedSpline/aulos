import os

# controls: [P]lay, P[a]use, [N]ext, [L]ast

# directories
music_dir = os.path.realpath("music")
playlist_dir = os.path.realpath("playlists")

# text strings
title_str = 'OpenDAP v0.0.0.1'
no_media_str = "Nothing playing."
no_load_str = "..."
song_sep_str = " by "
time_sep_str = " of "
home_menu_items = ["playlists", "albums", "artists", "genres", "tracks", "queue", "settings", "quit"]

# file types to scan for
file_types = {'.mp3', '.flac'}

# progress bar filler
prog_fill = '▒'
