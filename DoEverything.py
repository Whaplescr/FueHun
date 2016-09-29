import pyaudio
import matplotlib.pyplot as plt
from HueElements.Light import Light
from WavElements.WavFile import WaveFile

#wav_filename = 'onclassical_demo_ensemble-la-tempesta_porpora_iii-notturno_iii-lezione_live_small-version.wav'
wav_filename = 'woop.wav'

chunk_size = 1024

new_light = Light(light_number=2)
new_light.turn_off()
assert new_light.on == False
new_light.turn_on()
assert new_light.on == True

# Instantiate PyAudio.
p = pyaudio.PyAudio()

wave =  WaveFile(wav_filename)
wf = wave.wf

# Open stream.
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wave.n_channels,
                rate=wave.framerate,
                output=True)
data_list = []

data_chunks = wave.chop_chunks()

# data = wf.readframes(chunk_size)
# while len(data) > 0:
#     for point in data:
#         data_list.append(point)
#
#     stream.write(data)
#     data = wf.readframes(chunk_size)

for chunk in data_chunks:
    for point in chunk:
        data_list.append(point)
    stream.write(chunk)


# Plotting frequencies of the sound clip
plt.plot(range(0, len(data_list)), data_list)
plt.show()

# Stop stream.
stream.stop_stream()
stream.close()

# Close PyAudio.
p.terminate()