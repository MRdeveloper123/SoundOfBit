import sys
import click
from SoundOfBit import *


@click.command()
@click.option("--from_file", type=click.Path(exists=True), required=True, nargs=1)
@click.option("--to_file", type=click.Path(), default=None, nargs=1)
@click.option("--play", is_flag=True)
@click.option("--encode", is_flag=True)
@click.option("--decode", is_flag=True)
def main(from_file: str, to_file: str,
         play: bool, encode: bool, decode: bool) -> None:
    thread_pool = []
    if encode and decode:  # 不能既要编码又要解码
        print("Can't encode and decode at the same time")
        sys.exit(0)
    if play:  # 播放文件
        player = DirectStreamPlayer(from_file)
        player.start()
        thread_pool.append(player)
    if encode:  # 进行编码,将文件转换为音频
        if not to_file:  # 接下来的操作都需要指定保存位置才行
            print("Must specific '--to_file' argument")
            sys.exit(0)
        encoder = Encoder(from_file, to_file)
        encoder.start()
        thread_pool.append(encoder)
    if decode:  # 进行解码,将音频转换为文件
        if not to_file:  # 接下来的操作都需要指定保存位置才行
            print("Must specific '--to_file' argument")
            sys.exit(0)
        decoder = Decoder(from_file, to_file)
        decoder.start()
        thread_pool.append(decoder)
    # ---
    # 阻塞，等待所有线程结束。
    # 不能用join，用join的话线程无法响应Ctrl+C
    # 对所有线程使用is_alive
    print("Converting&Playing file...")
    bar = PacmanBar(thread_pool[0].max_progress)
    while True:
        # 如果没有创建任何线程,或者如果所有线程都结束了,退出
        if not thread_pool or {t.is_alive() for t in thread_pool} == {False}:
            # 打印完进度
            bar.current_progress = bar.max_progress  # 确保是100%
            bar.suffix_content = "100%"
            bar.printBar()
            print("\r\nSuccess")
            sys.exit(0)
        bar.current_progress = thread_pool[0].current_progress
        bar.suffix_content = "{}%".format(int(thread_pool[0].current_progress / thread_pool[0].max_progress * 100))
        bar.printBar()


if __name__ == "__main__":
    main()
