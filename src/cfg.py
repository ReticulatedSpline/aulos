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
empty_str = "empty!"
time_sep_str = " of "
track_sep_str = " by "
paused_str = "paused."
playing_str = "now playing:"
play_next_str = "queued next."
play_last_str = "queued last."
no_media_str = "nothing playing."
play_error_str = "couldn't play file."
load_error_str = "unable to load."
not_implemented_str = "not yet implemented!"
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
home_icon = '☯'
dir_icon = 'ᗕ '
menu_icon = '➤ '
track_icon = '♬ '
playlist_icon = '✎ '
progress_bar_fill_char = '█'
progress_bar_empty_char = '▒'
