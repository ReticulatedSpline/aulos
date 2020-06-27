# Aulos
Digital audio player designed for local media files, intended for the Raspberry Pi, and based on the venerable [VLC media player](https://en.wikipedia.org/wiki/VLC_media_player). The goal is to recreate the [Rockbox](https://www.rockbox.org/) experience on cheap, modern hardware in a portable installation.

## Roadmap
- [x] Play .mp3 and .flac audio files

- [x] UI with current track and playback progress

- [x] Resizable [curses](https://docs.python.org/3/howto/curses.html) UI

- [x] Browse library by track

- [x] Browse library by playlist

- [x] Browse library by artist, album, genre, and year

- [x] Queue functionality

- [ ] Cache library for faster startup

- [ ] View recently played tracks

- [ ] Reorderable queue

- [ ] Shuffling and looping

- [ ] Quick scrolling

- [ ] Monochrome, [dithered](https://en.wikipedia.org/wiki/Dither) album art

### Nice-to-haves

- [ ] Ability to edit .m3u playlists

- [ ] Ability to view and edit ID3 tags

## Recommended Hardware
While running OpenDAP on the Raspberry Pi hardware is the long-term goal, note that openDAP *should* run on any terminal emulator.

[Raspberry Pi 3 A+](https://www.adafruit.com/product/4027)

[2.8 inch PiTFT touchscreen display](https://www.adafruit.com/product/1601)

## Development
Help in the form of bug reports or pull requests is appreciated. I am new to Python and the Raspberry Pi platform.

### Unit Tests
Uses the [unittest](https://docs.python.org/3/library/unittest.html) framework. To run the tests just run `python3 -m unittest discover` from the project root directory.

### Setup
1. Install [VLC](https://www.videolan.org/vlc/)
1. Install [Python 3+](https://www.python.org/), and then install pip dependencies:
`pip3 install -r requirements.txt`
1. If you're on MacOS, you'll need to grant your terminal emulator [permissions](https://support.apple.com/guide/mac-help/allow-accessibility-apps-to-access-your-mac-mh43185/mac) for the [pynput keyboard listener](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx) to work. This setting can be found under System Preferences → Security and Privacy → Accessibility. You may also need to run the process as root; I've had better luck with 3rd party emulators than the native Terminal.app
1. Optionally add some files to `./music` `./playlists`
1. Run `python3 src/main.py`
