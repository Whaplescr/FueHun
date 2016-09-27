import wave
from time import sleep
import pyaudio
import sys
import os.path
import numpy
import requests
from json import dumps
from collections import deque
import random

request_url = 'http://192.168.0.3/api/4cywpZuSJ2RpTx0-MXBgKKTQWIP8HI5pQhqAh0eU/lights/2/state'
put_on = {"on":True}
put_off = {"on":False}
bri_max = {"bri":255}
bri_half = {"bri":127}
bri_min = {"bri":0}

on = dumps(put_on)
off = dumps(put_off)
b_max = dumps(bri_max)
b_half = dumps(bri_half)
b_min = dumps(bri_min)

top_color_list = [[0.3088,0.3212],[0.3548,0.3489],[0.17,0.3403],[0.2138,0.4051],[0.3059,0.3303],[0.3402,0.356],[0.3806,0.3576],[0.139,0.081],
                [0.3695,0.3584],[0.139,0.081],[0.245,0.1214],[0.6399,0.3041],[0.4236,0.3811],[0.2211,0.3328],[0.2682,0.6632],[0.6009,0.3684],
                [0.5763,0.3486],[0.1905,0.1945],[0.3511,0.3574],[0.6531,0.2834],[0.17,0.3403],[0.139,0.081],[0.17,0.3403],[0.5265,0.4428],
                [0.3227,0.329],[0.214,0.709],[0.4004,0.4331],[0.3787,0.1724],[0.3475,0.5047],[0.5951,0.3872],[0.296,0.1409],[0.7,0.2986],
                [0.4837,0.3479],[0.2924,0.4134],[0.2206,0.1484],[0.2239,0.3368],[0.1693,0.3347],[0.2742,0.1326],[0.5454,0.2359],[0.1576,0.2368],
                [0.3227,0.329],[0.1484,0.1599],[0.6621,0.3023],[0.3361,0.3388],[0.2097,0.6732],[0.3787,0.1724],[0.3227,0.329],[0.3174,0.3207],
                [0.4947,0.472],[0.5136,0.4444],[0.3227,0.329],[0.3227,0.329],[0.214,0.709],[0.214,0.709],[0.3298,0.5959],[0.316,0.3477],
                [0.4682,0.2452],[0.5488,0.3112],[0.2332,0.1169],[0.3334,0.3455],[0.4019,0.4261],[0.3085,0.3071],[0.3369,0.3225],[0.2663,0.6649],
                [0.3608,0.3756],[0.2621,0.3157],[0.5075,0.3145],[0.2901,0.3316],[0.3504,0.3717],[0.3227,0.329],[0.2648,0.4901],[0.4112,0.3091],
                [0.5016,0.3531],[0.1721,0.358],[0.214,0.2749],[0.2738,0.297],[0.276,0.2975],[0.3436,0.3612],[0.214,0.709],[0.2101,0.6765],
                [0.3411,0.3387],[0.3787,0.1724],[0.5383,0.2566],[0.7,0.2986],[0.215,0.4014],[0.139,0.081],[0.3365,0.1735],[0.263,0.1773],
                [0.1979,0.5005],[0.2179,0.1424],[0.1919,0.524],[0.176,0.3496],[0.504,0.2201],[0.1585,0.0884],[0.315,0.3363],[0.3581,0.3284],
                [0.3927,0.3732],[0.4027,0.3757],[0.139,0.081],[0.3421,0.344],[0.4432,0.5154],[0.354,0.5561],[0.5614,0.4156],
                [0.6726,0.3217],[0.3688,0.2095],[0.3751,0.3983],[0.2675,0.4826],[0.2539,0.3344],[0.4658,0.2773],[0.3591,0.3536],[0.3953,0.3564],
                [0.5305,0.3911],[0.3944,0.3093],[0.3495,0.2545],[0.262,0.3269],[0.2651,0.1291],[0.3787,0.1724],[0.2703,0.1398],[0.7,0.2986],
                [0.4026,0.3227],[0.1649,0.1338],[0.5993,0.369],[0.5346,0.3247],[0.5104,0.3826],[0.1968,0.5047],[0.3397,0.3353],[0.5714,0.3559],
                [0.3227,0.329],[0.2206,0.2948],[0.2218,0.1444],[0.2762,0.3009],[0.3292,0.3285],[0.1994,0.5864],[0.183,0.2325],[0.4035,0.3772],
                [0.17,0.3403],[0.3342,0.2971],[0.6112,0.3261],[0.1732,0.3672],[0.3644,0.2133],[0.3852,0.3737],[0.3227,0.329],[0.3227,0.329],
                [0.4432,0.5154],[0.3517,0.5618]]

lights = [2,4,5]


tmp_colors = top_color_list
c = 0
while len(top_color_list) <256:
    c += 1
    top_color_list.append(top_color_list[c])

random.shuffle(top_color_list)

queue = deque(lights)
for light in lights:
    off_url = 'http://192.168.0.3/api/4cywpZuSJ2RpTx0-MXBgKKTQWIP8HI5pQhqAh0eU/lights/%d/state' % light
    requests.put(off_url,off)

# for hue in top_color_list:
#     light = queue.popleft ()
#     queue.append(light)
#     hue_request_url = 'http://192.168.0.3/api/4cywpZuSJ2RpTx0-MXBgKKTQWIP8HI5pQhqAh0eU/lights/%d/state' %light
#
#     hue_d = {"xy":hue}
#     hue_j = dumps(hue_d)
#
#     requests.put(hue_request_url,hue_j)



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

data_freq = {}

min = 0.0
max = 0.0

data = wf.readframes(chunk_size)
while len(data) > 0:
    for point in numpy.fromstring(data,'uint8'):
        if point < min:
            min = point
        if point > max:
            max = point

        if point in data_freq:
            data_freq[point] = data_freq[point] + 1
        else:
            data_freq[point] = 1

    stream.write(data)
    data = wf.readframes(chunk_size)
    for point in numpy.fromstring(data,'uint8'):
        light = queue.popleft()
        queue.append(light)
        hue_request_url = 'http://192.168.0.3/api/4cywpZuSJ2RpTx0-MXBgKKTQWIP8HI5pQhqAh0eU/lights/%d/state' % light

        hue_d = {"xy": top_color_list[point]}
        hue_j = dumps(hue_d)

        requests.put(hue_request_url, hue_j)


sorted_freq = sorted(data_freq)

for k in sorted_freq:
    print("Intensity %s, frequency %s" %(str(k),str(data_freq[k])))
print("Max: %f" %max)
print("Min: %f" %min)

print(max-min)

# Stop stream.
stream.stop_stream()
stream.close()

# Close PyAudio.
p.terminate()

#for point in decoded:
#    print(point)