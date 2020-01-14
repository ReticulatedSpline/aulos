# openDAP
An open source digital audio player program designed for the Raspberry Pi and a PiTFT display. Uses [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player) for media playback and the [curses library](https://en.wikipedia.org/wiki/Curses_%28programming_library%29) for a text-based user interface.

![screen capture of openDAP's textual interface](https://i.imgur.com/6k4LK09.png)

## Roadmap
### v1: Basic DAP functionality

- [x] Play .mp3 and .flac files

- [x] UI with current song and playback progress

- [ ] Support for .m3u playlists

- [ ] Browse library by artist, album, genre, year, and .m3u playlists

- [ ] Queue functionality

- [ ] Compatibility with the AdaFruit PiTFT touch display and/or hardware buttons

- [ ] Battery integration & runtime testing

### v2: Metadata handling

- [ ] CRUD operations for ID3 tags

- [ ] CRUD operations for .m3u playlists

- [ ] Tracking of ID3 and .m3u CRUD operations to support syncing to library copy

### v3: Extras

- [ ] Display album art

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
