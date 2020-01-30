# OpenDAP
An open source digital audio player designed for the Raspberry Pi and a PiTFT display. OpenDAP allows playback of almost any audio file, as it is based on the venerable [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player). Local storage means your music is accessable even when you're without internet, which should be ideal for users who find themselves on the moon, or stuck in the '70s.

![screen capture of OpenDAP's textual interface](https://i.imgur.com/6k4LK09.png)

## Roadmap
### v1: Basic DAP functionality

- [x] Play .mp3 and .flac files

- [x] UI with current song and playback progress

- [x] Menu navigation

- [ ] Browse library by artist, album, genre, year, and .m3u playlists

- [ ] Queue functionality

### v2: Portability 

- [ ] Compatibility with the AdaFruit PiTFT touch display and/or hardware buttons

- [ ] Investigate suitable batteries

- [ ] Investigate suitable cases

### v3: Extras

- [ ] Shuffling and looping

- [ ] Quick scrolling

- [ ] Ability to view/edit all ID3 tags

- [ ] Ability to edit .m3u playlists

- [ ] Display album art

- [ ] Sync songs via WiFi and/or Bluetooth (with other openDAPs?)

## Recommended Hardware
While running on this hardware is the long-term goal, note that openDAP should run on any *nix terminal.

[Raspberry Pi 3 A+](https://www.adafruit.com/product/4027)

[2.8 inch PiTFT touchscreen display](https://www.adafruit.com/product/1601)

## Development Setup
1. Install [VLC](https://www.videolan.org/vlc/) if you don't have it already.
1. Install [Python 3+](https://www.python.org/), and then install dependencies:
`pip3 install -r requirements.txt`
1. If on MacOS, you'll need to allow your terminal permissions for the [pynput keyboard listener](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx). This is under System Preferences ▶ Security and Privacy ▶ Accessibility.
1. Optionally add some files to `./music` `./playlists`.
1. Run `python3 src/main.py`
