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

#TODO: Update the wav file player to an object
#TODO: initialize player with wav file state items using wf.getparams()
#frames
frames = wf.getnframes()
# Framerate
rate = wf.getframerate()

duration = frames/rate
print(frames)
print(duration)

#TODO: Looks like doing one light call per read of the buffer will give us ~40 calls
#TODO: Realisticly we should only be doing 30 calls in the course of 3 seconds (10 calls per light per second)



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
    for point in data:
        data_list.append(point)

    stream.write(data)
    data = wf.readframes(chunk_size)


# Plotting frequencies of the sound clip
plt.plot(range(0, len(data_list)), data_list)
plt.show()

# Stop stream.
stream.stop_stream()
stream.close()

# Close PyAudio.
p.terminate()