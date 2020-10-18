"""
将音频转换为文件
"""
import os
import threading
from SoundOfBit import Universal


class Decoder(threading.Thread):
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
        gen = Universal.waveIter(self.file_location, 10240)
        file = open(self.save_location, "wb")
        while True:
            try:
                data = next(gen)
                file.write(data)
                self.current_progress += len(data)
            except StopIteration:
                file.close()
                gen.close()
                self.finished = True
                break
