import wave
import sys
import numpy as np
import matplotlib.pyplot as plt
import math


class WaveFile:

    def __init__(self,file_path):

        self.file_path = file_path
        self.wf = self.open_file()

        self.sample_rate = self.wf.getframerate()
        self.amp_width = self.wf.getsampwidth()
        self.nChannels = self.wf.getnchannels()
        self.nFrames = self.wf.getnframes()
        self.framerate = self.wf.getframerate()
        self.duration = self.nFrames/self.framerate


    def open_file(self):
        try:
            wf = wave.open(self.file_path, 'rb')
            return wf
        except IOError as ioe:
            sys.stderr.write('IOError on file ' + self.file_path + '\n' + str(ioe) + '. Skipping.\n')
        except EOFError as eofe:
            sys.stderr.write('EOFError on file ' + self.file_path + '\n' + str(eofe) + '. Skipping.\n')

    def chop_chunks(self,chunk_size=1024):
        chopped_chunks = []

        data = self.wf.readframes(chunk_size)
        while len(data) > 0:
            data_convert = []
            for point in data:
                data_convert.append(int(point))
            chopped_chunks.append(data_convert)
            data = self.wf.readframes(chunk_size)

        return chopped_chunks

    def get_hz_per_bin(self,fft_size):
        #print(self.sample_rate)
        #print(self.sample_rate/2)
        #print((self.sample_rate/2)/ fft_size)
        return (self.sample_rate/2) / fft_size

    def get_bass_bands(self,band_size,fft_size=512):
        return math.ceil(200/band_size)

    def get_mid_bands(self,band_size,fft_size=512):
        return math.ceil(1500/band_size)

    def get_low_highs(self,data_samples,b_i,m_i,sample_size=1024):

        bass_powers = []
        mid_powers = []
        high_powers = []

        for chunk in data_samples:
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
            bass_powers.append(int(np.real(bass_power)))

            mid_power = 0
            for val in mid_bands:
                mid_power += val
            mid_powers.append(int(np.real(mid_power)))

            high_power = 0
            for val in high_bands:
                high_power += val
            high_powers.append(int(np.real(high_power)))

        b_min = min(bass_powers)
        b_max = max(bass_powers)
        m_min = max(mid_powers)
        m_max = max(mid_powers)
        h_min = min(high_powers)
        h_max = max(high_powers)

        return [[b_min,b_max],[m_min,m_max],[h_min,h_max]]