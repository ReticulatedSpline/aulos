# OpenDAP
A digital audio player designed for local media files, intended for the Raspberry Pi, and based on the venerable [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player). OpenDAP is not tested on animals.

## Roadmap

#### v1
- [x] Play .mp3 and .flac audio files

- [x] UI with current song and playback progress

- [x] Curses menu navigation

- [x] Browse library by track

- [x] Browse library by playlist

- [ ] Queue functionality

- [ ] Browse library by artist, album, genre, and year

#### v2
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

## Development
### Architecture
OpenDAP is loosely based on the Model-View-Controller architecture. You'll find code split into one of three files:

**View.py**: Code that uses the Curses library or draws on the display.

**Controller.py**: Logic determining which screen is drawn next and gathering user input.

**Model.py**: Code that handles disk I/O or uses the VLC library.

### Setup
1. Install [VLC](https://www.videolan.org/vlc/) if you don't have it already.
1. Install [Python 3+](https://www.python.org/) if you don't have it already, and then install pip dependencies:
`pip3 install -r requirements.txt`
1. If you're on MacOS, you'll need to grant your terminal emulator [permissions](https://support.apple.com/guide/mac-help/allow-accessibility-apps-to-access-your-mac-mh43185/mac) for the [pynput keyboard listener](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx) to work. This setting can be found under System Preferences ▶ Security and Privacy ▶ Accessibility. You may also need to run the process as root; I've had better luck with 3rd party emulators than the native Terminal.app.
1. Optionally add some files to `./music` `./playlists`.
1. Run `python3 src/main.py`.
