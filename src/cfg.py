"""User settings. Change only text between quotes."""

# in seconds
refresh_rate = 0.02

# should be able to handle any format VLC can
music_dir = "music"
music_formats = ('.mp3', '.flac')
playlist_dir = "playlists"
playlist_formats = ('.m3u')

# text strings
no_media_str = "Nothing playing."
no_load_str = "..."
play_error_str = "Couldn't play file."
not_implemented_str = "Not yet implemented!"
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
media_option_items = [
    "play",
    "view",
    "queue next",
    "queue last",
    "delete"
]

# symbols
prog_fill = u'▒'
home_icon = u'☯'
dir_icon = u'ᗕ '
menu_icon = u'➤ '
track_icon = u'♬ '
playlist_icon = u'✎ '
