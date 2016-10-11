import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from HueElements.Light import Light
from WavElements.WavFile import WaveFile


def do_fft_stuff(file_name,sample_size=1024):#2048):

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


    all_bass = []
    all_mid = []
    all_high = []

    # Parse the sampled signal
    for chunk in data_chunks:
        # In case one of the samples size is less than expected, pad it with 0's
        if len(chunk) < sample_size:
            remainder = sample_size - len(chunk)
            zeroes = [0] * remainder
            chunk = chunk + zeroes

        # Get the real portion of the fft of the sample
        fft = np.fft.fft(chunk)
        rfft = np.real(fft[0:round(len(fft)/2)])

        # Seperate the bands of the sample

        bass_bands = rfft[0:b_i]
        mid_bands = rfft[b_i:m_i]
        high_bands = rfft[m_i:len(rfft)]

        all_bass.append(bass_bands)
        all_mid.append(mid_bands)
        all_high.append(high_bands)

    bass_coeffs = []

    for band in all_bass:
        for band_2 in all_bass:
            if np.array_equal(band,band_2):
                #pass
                bass_coeffs.append(1)
            else:
                ccorr = np.corrcoef(band,band_2)
                bass_coeffs.append(ccorr[0][1])

    axes = plt.gca()
    axes.set_ylim([-2,2])
    plt.plot(bass_coeffs)

    mid_coeffs = []
    for band in all_mid:
        for band_2 in all_mid:
            if np.array_equal(band,band_2):
                # pass
                mid_coeffs.append(1)
            else:
                ccorr = np.corrcoef(band,band_2)
                mid_coeffs.append(ccorr[0,1])

    plt.plot(mid_coeffs)

    high_coeffs = []
    for band in all_high:
        for band_2 in all_high:
            if np.array_equal(band,band_2):
                # pass
                high_coeffs.append(1)
            else:
                ccorr = np.corrcoef(band,band_2)
                high_coeffs.append(ccorr[0,1])

    plt.plot(high_coeffs)
    plt.show()

    # stream.stop_stream()
    # stream.close()
    #
    # #Close PyAudio.
    # p.terminate()

do_fft_stuff('woop.wav',1024)

#do_fft_stuff('SongSparrow].wav',2048)

#do_fft_stuff('onclassical_demo_ensemble-la-tempesta_porpora_iii-notturno_iii-lezione_live_small-version.wav',8192)
