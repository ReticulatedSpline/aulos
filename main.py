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
        player.play()
        return
    elif choice.lower() == 'a':
        player.pause()
        get_input()
    elif choice.lower() == 'n':
        player.stop()
        song_idx += 1
        return
    elif choice.lower() == 'l':
        if (song_idx):
            player.stop()
            song_idx -= 1
        else:
            player.stop()
            player.play()
        return
    else:
        get_input()

for dirpath, dirnames, files in os.walk(music_path):
    for file in files:
        song_list.append(os.path.join(dirpath, file))

while (True):
    player = vlc.MediaPlayer(song_list[song_idx])
    get_input()
    metadata = mutagen.File(song_list[song_idx], easy=True)
    print('Now playing \"' + str(metadata['title']).strip('[\']') 
            + '\" by \"' + str(metadata['artist']).strip('[\']') + '\"...')
    continue
