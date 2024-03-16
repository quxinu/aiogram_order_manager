import logging
from colorama import Fore, Style, init
import datetime


init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_message = super().format(record)

        current_time_utc3 = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        formatted_time = current_time_utc3.strftime('%d-%m-%Y %H:%M:%S')

        return (
            self.COLORS.get(record.levelname, Fore.WHITE)
            + f"[{formatted_time}] {log_message}"
            + Style.RESET_ALL
        )

def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter('> [%(levelname)s]: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger