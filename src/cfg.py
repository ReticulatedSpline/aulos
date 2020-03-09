"""user settings"""

# in seconds, lower should be more responsive
refresh_rate = 0.01

# in seconds, after this is reached 'skip back' resets to track start instead
# of skipping to the last played track.
skip_back_threshold = 5.0

# should be able to handle any format VLC can
music_dir = "music"
music_formats = ('.mp3', '.flac')
playlist_dir = "playlists"
playlist_formats = ('.m3u')

# text strings
no_load_str = "..."
time_sep_str = " of "
track_sep_str = " by "
paused_str = "Paused."
playing_str = "Now playing:"
play_next_str = "Queued next."
play_last_str = "Queued last."
no_media_str = "Nothing playing."
play_error_str = "Couldn't play file."
load_error_str = "Unable to complete request."
not_implemented_str = "Not yet implemented!"
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
home_icon = u'☯'
dir_icon = u'ᗕ '
menu_icon = u'➤ '
track_icon = u'♬ '
playlist_icon = u'✎ '
progress_bar_fill_char = u'█'
progress_bar_empty_char = u'▒'
