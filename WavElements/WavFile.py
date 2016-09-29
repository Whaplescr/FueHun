import wave
import sys

class WaveFile:

    def __init__(self,file_path):

        self.file_path = file_path
        self.wf = self.open_file()

        self.frame_count = self.wf.getnframes()
        self.framerate = self.wf.getframerate()
        self.duration = self.frame_count / self.framerate

        self.n_channels = self.wf.getnchannels()

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
            chopped_chunks.append(data)
            data = self.wf.readframes(chunk_size)

        return chopped_chunks