from constants import SOUND, MUSIC, SOUND_VOL, MUSIC_VOL, TRACKS
import random
import pyglet

try:
    import pyglet.media.avbin
    have_avbin = True
except:
    pyglet.options['audio'] = ('silent')
    have_avbin = False


# GENERAL
tracks = []
playing_tracks = []

def start_music():
    for t in TRACKS:
        tracks.append(play_music(t, None, 0))
    inc_music()

def inc_music():
    if not len(tracks):
        return

    t = random.choice(tracks)
    tracks.remove(t)
    playing_tracks.append(t)
    t.volume = MUSIC_VOL

def dec_music():
    if not len(playing_tracks):
        return

    t = random.choice(playing_tracks)
    playing_tracks.remove(t)
    tracks.append(t)
    t.volume = 0


# MUSIC
def play_music(name, player, vol = MUSIC_VOL):
    if not MUSIC:
        return

    if not have_avbin:
        return

    if not player:
        player = pyglet.media.Player()

    player.queue(pyglet.resource.media(name, streaming=True))
    player.volume = vol
    player.eos_action = 'loop'
    player.play()

    return player


# SOUND
sounds = {}

def load_sound(name):
    if not SOUND:
        return

    if name not in sounds:
        sounds[name] = pyglet.resource.media(name, streaming=False)

def play_sound(name, vol = SOUND_VOL):
    if not SOUND:
        return

    load_sound(name)
    sounds[name].play().volume = vol
