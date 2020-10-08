import sys
import click
from SoundOfBit import *


@click.command()
@click.option("--file_location", type=click.Path(exists=True), required=True, nargs=1)
@click.option("--save_location", type=click.Path(), default=None, nargs=1)
@click.option("--buffer", type=int, default=10240, nargs=1)
@click.option("--play", is_flag=True)
def main(file_location: str, save_location: str,
         buffer: int, play: bool) -> None:
    thread_pool = []
    if play:  # 播放文件
        player = DirectStreamPlayer(file_location, buffer)
        player.start()
        thread_pool.append(player)
    if save_location:  # 指定了保存位置，进行转换
        converter = Converter(file_location, save_location, buffer)
        converter.start()
        thread_pool.append(converter)
    # 阻塞，等待所有线程结束。
    # 不能用join，用join的话线程无法响应Ctrl+C
    # 对所有线程使用is_alive
    while True:
        # 如果没有创建任何线程
        if not thread_pool:
            sys.exit(0)
        # 如果所有线程都结束了，退出
        if {t.is_alive() for t in thread_pool} == {False}:
            sys.exit(0)


if __name__ == "__main__":
    main()
