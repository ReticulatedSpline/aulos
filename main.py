import os
import time
import vlc
import mutagen

music_path = 'music'
song_list = []
song_idx = 0
player = None

def get_input():
    global player
    global song_idx
    choice = input('[P]lay, P[a]use, [N]ext, [L]ast\n▶ ')
    if choice.lower() == 'p':
        print("Playing...")
        player.play()
        return
    elif choice.lower() == 'a':
        print("Pausing...")
        player.pause()
        get_input()
    elif choice.lower() == 'n':
        print("Skipping...")
        song_idx += 1
        player.set_media(song_list[song_idx])
        return
    elif choice.lower() == 'l':
        print("Skipping back...")
        if (song_idx):
            song_idx -= 1
            player.set_media(song_list[song_idx])
        else:
            player.stop()
            player.play()
        return
    else:
        get_input()

for dirpath, dirnames, files in os.walk(music_path):
    for file in files:
        song_list.append(os.path.join(dirpath, file))

player = vlc.MediaPlayer(song_list[song_idx])

while (True):
    get_input()
    metadata = mutagen.File(song_list[song_idx], easy=True)
    print('Now playing \"' + str(metadata['title']).strip('[\']') 
            + '\" by \"' + str(metadata['artist']).strip('[\']') + '\"...')
    continue
