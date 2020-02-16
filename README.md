# OpenDAP
An open source digital audio player designed for the Raspberry Pi and based on the venerable [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player). Local storage means your music is accessable even when you're without internet, which should be ideal for users who find themselves stuck in the 1970s. OpenDAP is not tested on animals.

## Roadmap

- [x] Play .mp3 and .flac audio files

- [x] UI with current song and playback progress

- [x] Menu navigation

- [x] .m3u playlist support

- [ ] Browse library by artist, album, genre, and year

- [ ] Queue functionality

- [ ] Compatibility with the AdaFruit PiTFT touch display and/or hardware buttons

- [ ] Investigate suitable batteries

- [ ] Investigate suitable cases

- [ ] Shuffling and looping

- [ ] Quick scrolling

- [ ] Ability to view/edit ID3 tags

- [ ] Ability to edit .m3u playlists

- [ ] Display album art

- [ ] Sync songs via WiFi and/or Bluetooth (with other openDAPs?)

## Recommended Hardware
While running OpenDAP on the Raspberry Pi hardware is the long-term goal, note that openDAP *should* run on any terminal emulator.

[Raspberry Pi 3 A+](https://www.adafruit.com/product/4027)

[2.8 inch PiTFT touchscreen display](https://www.adafruit.com/product/1601)

## Development Setup
1. Install [VLC](https://www.videolan.org/vlc/) if you don't have it already.
1. Install [Python 3+](https://www.python.org/), and then install dependencies:
`pip3 install -r requirements.txt`
1. If on MacOS, you'll need to allow your terminal emulator permissions for the [pynput keyboard listener](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx). This is under System Preferences ▶ Security and Privacy ▶ Accessibility. You may also need to run the process as root; I've had better luck with 3rd party emulators than the native Terminal.app.
1. Optionally add some files to `./music` `./playlists`.
1. Run `python3 src/main.py`.
