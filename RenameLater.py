import pyaudio
import numpy as np

from WavElements.WavFile import WaveFile


def do_fft_stuff(file_name,sample_size=1024):

    wave = WaveFile(file_name)
    framerate = wave.framerate
    band_size = wave.get_hz_per_bin(sample_size/2)

    b_i = wave.get_bass_bands(band_size)
    m_i = wave.get_mid_bands(band_size)

    data_chunks = wave.chop_chunks(sample_size)

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    p.open(format=p.get_format_from_width(wave.amp_width),
            channels = wave.nChannels,
            rate = framerate,
            output = True)



    for chunk in data_chunks:

        rfft = np.fft.rfft(chunk)

        bass_bands = rfft[0:b_i]
        mid_bands = rfft[b_i:m_i]
        high_bands = rfft[m_i:]

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

        print(len(bass_bands))
        print(len(mid_bands))
        print(len(high_bands))

        print(bass_power)
        print(mid_power)
        print(high_power)

do_fft_stuff('woop.wav')