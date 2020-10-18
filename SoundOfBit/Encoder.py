"""
将文件转换为音频
"""
import os
import wave
import threading
from SoundOfBit import Universal


class Encoder(threading.Thread):
    def __init__(self, file_location: str, save_location: str) -> None:
        super().__init__()
        # ---
        self.file_location = file_location
        self.save_location = save_location
        # ---
        self.setDaemon(True)
        self.current_progress = 0
        self.max_progress = os.path.getsize(file_location)
        self.finished = False

    def run(self) -> None:
        gen = Universal.fileIter(self.file_location, 10240)
        wav = wave.open(self.save_location, "w")
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(44100)
        while True:
            try:
                data = next(gen)
                wav.writeframes(data)
                self.current_progress += len(data)
            except StopIteration:
                wav.close()
                gen.close()
                self.finished = True
                break
