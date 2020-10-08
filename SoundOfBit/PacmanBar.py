"""
吃豆人进度条
|      Coooooooooooooooooooooooo|
|         Cooooooooooooooooooooo|
|            Coooooooooooooooooo|
"""
import sys
import colorama


class PacmanBar:
    def __init__(self, max_progress: int = 1,
                 prefix_content: str = "", suffix_content: str = "",
                 max_char_length: int = 50) -> None:
        """
        :param max_progress: 总进度大小
        :param prefix_content: 进度条末尾内容
        :param suffix_content: 进度条前端内容
        :param max_char_length: 进度条字符最大长度
        """
        self.max_progress = max_progress
        self.prefix_content = prefix_content
        self.suffix_content = suffix_content
        self.max_char_length = max_char_length
        # ---
        colorama.init(autoreset=True)
        self.current_progress = 0  # 当前进度大小
        self.pacman = colorama.Fore.LIGHTYELLOW_EX + "C" + colorama.Fore.RESET  # 吃豆人，黄色的大写C
        self.bean = colorama.Fore.LIGHTYELLOW_EX + "o" + colorama.Fore.RESET  # 豆子，黄色小写o

    def printBar(self) -> None:
        past_length = int(self.current_progress / self.max_progress * self.max_char_length) + 1
        bar = "{} |{}{}{}| {}".format(self.prefix_content,
                                      "-" * past_length,
                                      self.pacman,  # 吃豆人
                                      self.bean * (self.max_char_length - past_length),
                                      self.suffix_content)
        sys.stdout.write("" * 1000); sys.stdout.flush()
        sys.stdout.write("\r"); sys.stdout.flush()
        sys.stdout.write(bar); sys.stdout.flush()
