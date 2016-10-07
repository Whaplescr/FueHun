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