#!/usr/bin/env python3
import sys
import numpy as np
import random
import itertools
import librosa
import soundfile as sf
from os import listdir, mkdir
from os.path import isfile, join, exists

def load_audio_sec(file_path, sr=16000, num_pieces=-1):
    data, _ = librosa.core.load(file_path, sr)
    if num_pieces != -1 and len(data) > num_pieces:
        data = data[:num_pieces]
    else:
        cur_len = len(data)
        data = np.pad(data, pad_width=(0, max(0, num_pieces - len(data))),mode="symmetric")
    return data

path = sys.argv[1]
if path[-1] != '/':
	path = path + '/'

noise_path = path[:-1] + "_noisy/"
if not exists(noise_path):
	mkdir(noise_path)

files = [f for f in listdir(path) if isfile(join(path, f))]
for file in files:
    form = file[-4:]
    if form == ".wav" or form == "flac":
        data = load_audio_sec(join(path, file))
        noise_1 = load_audio_sec('noises/noise-free-sound-0842.wav', 16000, len(data))
        noise_2 = load_audio_sec('noises/254098_4616297-lq.wav', 16000, len(data))
        data_wn = data + 0.05*noise_1 + 0.05*noise_2
        if form == 'flac':
            sf.write(noise_path + file, data_wn, 1600, format='flac', subtype='PCM_24')
        else:
            librosa.output.write_wav(noise_path + file, data_wn, 16000)
