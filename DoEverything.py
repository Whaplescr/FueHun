import pyaudio
import matplotlib.pyplot as plt
from WavElements.WavFile import WaveFile
import math
import numpy as np
from time import sleep



#wav_filename = 'onclassical_demo_ensemble-la-tempesta_porpora_iii-notturno_iii-lezione_live_small-version.wav'
#wav_filename = 'SongSparrow].wav'
wav_filename = 'woop.wav'

wave =  WaveFile(wav_filename)
framerate = wave.framerate
fft_size = 1024

data_chunks = wave.chop_chunks(1024)

bass_d = []
mid_d = []
high_d = []

# This looks like awesome results sofar, still wondering why rfft gives me 513
# TODO: Try this same code with np.fft[0:len/2] and see what the results give
# TODO: Other todo is to figure out how we're gonna map these bass,mid and high powers to light changes

for chunk in data_chunks:

    # I dont know why getting the the rfft gives us 513 instead of 512
    rfft = np.fft.rfft(chunk)
    #print(len(rfft))

    bass_vals = rfft[0:20]
    mids = rfft[20:300]
    highs = rfft[300:]

    bass_power = 0
    for val in bass_vals:
        bass_power += val
    bass_power = int(np.real(bass_power))

    mid_power = 0
    for val in mids:
        mid_power += val
    mid_power = int(np.real(mid_power))

    high_power = 0
    for val in highs:
        high_power += val
    high_power = int(np.real(high_power))


    bass_d.append(bass_power)
    mid_d.append(mid_power)
    high_d.append(int(high_power))

    #print(np.real(bass_power))
    #print(np.real(mid_power))
    #print(np.real(high_power))

    #plt.plot(rfft)
    #plt.show()

print(bass_d)
print(mid_d)
print(high_d)

# Instantiate PyAudio.
# p = pyaudio.PyAudio()

#for chunk in data_chunks:
    #stream.write(chunk)

# stream.stop_stream()
# stream.close()

# Close PyAudio.
# p.terminate()
