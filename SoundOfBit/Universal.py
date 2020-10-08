import wave


def fileIter(file_location: str, buffer: int = 10240):
    """
    文件二进制内容迭代
    :param file_location: 文件位置
    :param buffer: 缓冲区大小，每次读取的大小
    """
    with open(file_location, "rb") as f:
        while True:
            data = f.read(buffer)
            if not data:
                break
            else:
                yield data


def waveIter(wave_location: str, buffer: int = 10240):
    """
    波形文件二进制内容迭代
    :param wave_location: 波形文件位置
    :param buffer: 缓冲区大小，每次读取的大小
    """
    with wave.open(wave_location, "r") as wav:
        while True:
            data = wav.readframes(buffer)
            if not data:
                break
            else:
                yield data
