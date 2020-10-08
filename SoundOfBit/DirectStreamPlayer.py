"""
直接播放文件
将文件二进制内容直接写入音频流
"""
import os
import pyaudio
import threading
from SoundOfBit import Universal


class DirectStreamPlayer(threading.Thread):
    def __init__(self, file_location, buffer: int = 10240) -> None:
        super().__init__()
        # ---
        self.file_location = file_location
        self.buffer = buffer
        # ---
        self.setDaemon(True)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(output=True, rate=44100, format=pyaudio.paInt16, channels=1)
        self.current_progress = 0
        self.max_progress = os.path.getsize(file_location)
        self.finished = False

    def run(self) -> None:
        print("Playing file: {}".format(self.file_location))
        gen = Universal.fileIter(self.file_location, self.buffer)
        while True:
            try:
                data = next(gen)
                self.stream.write(data)
                self.current_progress += len(data)
            except StopIteration:
                gen.close()
                self.stream.close()
                self.p.terminate()
                self.finished = True
                break
