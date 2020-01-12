# openDAP
An open source digital audio player program designed for the Raspberry Pi and a PiTFT display. Uses [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player) for media playback and the [curses library](https://en.wikipedia.org/wiki/Curses_%28programming_library%29) for a text-based user interface.

## Roadmap
### v1

- [x] Play .mp3 and .flac files

- [x] UI with current song and playback progress

- [ ] Support for m3u playlists

- [ ] Browse local library by artist, album, and m3u playlist

### v2

- [ ] View all ID3 tags and other song metadata

- [ ] Ability to ID3 tags

- [ ] Ability to edit m3u playlists

- [ ] Queue functionality

- [ ] Log ID3 and m3u CRUD operations to support syncing back to a master library

- [ ] Compatibility with the AdaFruit PiTFT touch display or hardware buttons

### v3

- [ ] Display album art

- [ ] Battery integration

- [ ] Sync songs via WiFi and/or Bluetooth (with other openDAPs?)

## Recommended Hardware
[Raspberry Pi 3 A+](https://www.adafruit.com/product/4027)

[2.8 inch touchscreen display](https://www.adafruit.com/product/1601)

## Development Setup
1. Install [VLC](https://www.videolan.org/vlc/) if you don't have it already.
1. Install [Python 3+](https://www.python.org/), and then install dependencies:
`pip3 install -r requirements.txt`
1. If on MacOS, you'll need to allow your terminal permissions for the [pynput keyboard listener](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx). This is under System Preferences ▶ Security and Privacy ▶ Accessibility.
1. Optionally add some files to `./music` `./playlists`.
1. Run `python3 src/main.py`
