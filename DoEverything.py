import wave
import pyaudio
import sys
import numpy
import requests
from json import dumps
from collections import deque
from Helpers.Colors import ColorHelper
import matplotlib.pyplot as plt

lights = [2,4,5]
queue = deque(lights)

#wav_filename = 'onclassical_demo_ensemble-la-tempesta_porpora_iii-notturno_iii-lezione_live_small-version.wav'
wav_filename = 'woop.wav'
chunk_size = 1024


try:
    print
    'Trying to play file ' + wav_filename
    wf = wave.open(wav_filename, 'rb')
except IOError as ioe:
    sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
                     str(ioe) + '. Skipping.\n')
except EOFError as eofe:
    sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
                     str(eofe) + '. Skipping.\n')


# Instantiate PyAudio.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data_list = []

data = wf.readframes(chunk_size)
while len(data) > 0:

    avg = 0
    abs_list = []
    plot_list = []

    for point in data:
        abs_list.append(point)
        data_list.append(point)

    avg = sum(abs_list)/len(abs_list)
    for point in abs_list:
        plot_list.append(avg-point)


    plt.scatter(range(0, len(plot_list)), plot_list)
    plt.show()

    stream.write(data)
    data = wf.readframes(chunk_size)


    # TODO: Let's consider assigning each light to a function
    # TODO: So one light will be the max in a chunk, one the min, and one the average
    # Further note, this doesnt work very well, we encounter the max of 255 VERY quickly, like every 7th sample or so

# Plotting frequencies of the sound clip
plt.scatter(range(0, len(data_list)), data_list)
plt.show()

# Stop stream.
stream.stop_stream()
stream.close()

# Close PyAudio.
p.terminate()

#for point in decoded:
#    print(point)