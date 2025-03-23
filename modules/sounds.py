# modules/sounds.py

"""
Play typing sounds as you type. 
Requires a library like pygame (pip install pygame) or playsound.
Here is a minimal pygame example.
"""

import pygame
import random
import os

_sound_files = []
_sound_on = False

def init_sounds(sound_folder):
    """
    Initialize pygame mixer and load all sound files from the given folder.
    """
    global _sound_files
    pygame.mixer.init()
    for file in os.listdir(sound_folder):
        if file.lower().endswith(('.wav', '.mp3', '.ogg')):
            _sound_files.append(os.path.join(sound_folder, file))

def play_key_sound():
    """
    Play a random typing sound from the loaded list (if enabled).
    """
    global _sound_files, _sound_on
    if _sound_on and _sound_files:
        sound_file = random.choice(_sound_files)
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

def set_sound_on(on_off):
    """
    Enable or disable typing sounds globally.
    """
    global _sound_on
    _sound_on = on_off

def stop_all_sounds():
    """
    Stop all sounds currently playing.
    """
    pygame.mixer.stop()
