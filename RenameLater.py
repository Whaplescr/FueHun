import pyaudio
import numpy as np

from HueElements.Light import Light
from WavElements.WavFile import WaveFile


def do_fft_stuff(file_name,sample_size=2048):

    wave = WaveFile(file_name)
    framerate = wave.framerate

    # Get the size of the bands, i.e. what does each bin of the sample represent in terms of hz
    band_size = wave.get_hz_per_bin(sample_size/2)

    # Calculate the inded
    b_i = wave.get_bass_bands(band_size)
    m_i = wave.get_mid_bands(band_size)

    # Pre break up the samples of damage
    # TODO: Convert the reading + analysis to real time
    data_chunks = wave.chop_chunks(sample_size)

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open audio stream for writing
    stream = p.open(format=p.get_format_from_width(wave.amp_width),
                channels = wave.nChannels,
                rate = framerate,
                output = True)

    bass_light = Light(2)
    mid_light = Light(4)
    high_light = Light(5)

    bass_light.turn_on()
    mid_light.turn_on()
    high_light.turn_on()

    bass_light.change_color_by_name(color = 'Blue')
    mid_light.change_color_by_name(color = 'Yellow')
    high_light.change_color_by_name(color = 'Red')

    high_low = wave.get_low_highs(data_chunks,b_i,m_i)

    # Parse the sampled signal
    for chunk in data_chunks:
        # In case one of the samples size is less than expected, pad it with 0's
        if len(chunk) < sample_size:
            remainder = sample_size - len(chunk)
            zeroes = [0] * remainder
            chunk = chunk + zeroes

        # Get the real portion of the fft of the sample
        rfft = np.fft.rfft(chunk)

        # Seperate the bands of the sample
        bass_bands = rfft[0:b_i]
        mid_bands = rfft[b_i:m_i]
        high_bands = rfft[m_i:len(rfft)]

        # Get the power of each band
        bass_power = 0
        for val in bass_bands:
            bass_power += val
        bass_power = int(np.real(bass_power))

        mid_power = 0
        for val in mid_bands:
            mid_power += val
        mid_power = int(np.real(mid_power))

        high_power = 0
        for val in high_bands:
            high_power += val
        high_power = int(np.real(high_power))

        # Change the brightness to the power of that band
        bass_light.change_brightness(int(np.interp(bass_power, high_low[0], [1, 254])))
        mid_light.change_brightness(int(np.interp(mid_power, high_low[1], [1, 254])))
        high_light.change_brightness(int(np.interp(high_power, high_low[2], [1, 254])))

        stream.write(bytes(chunk))

    stream.stop_stream()
    stream.close()

    #Close PyAudio.
    p.terminate()

do_fft_stuff('woop.wav',2048)
do_fft_stuff('SongSparrow].wav',2048)
do_fft_stuff('onclassical_demo_ensemble-la-tempesta_porpora_iii-notturno_iii-lezione_live_small-version.wav',8192)
#print("")
