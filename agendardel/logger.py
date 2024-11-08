# import logging
# from colorama import Fore, Style, init

# # Initialize Colorama
# init(autoreset=True)

# # Custom formatter for colored logging
# class CustomFormatter(logging.Formatter):
#     log_format = "%(asctime)s | %(levelname)s: %(message)s"
#     date_format = "%Y-%m-%d %H:%M:%S"

#     COLORS = {
#         logging.DEBUG: Fore.BLUE,
#         logging.INFO: Fore.GREEN,
#         logging.WARNING: Fore.YELLOW,
#         logging.ERROR: Fore.RED,
#         logging.CRITICAL: Fore.RED + Style.BRIGHT,
#     }

#     def format(self, record):
#         log_color = self.COLORS.get(record.levelno, Fore.WHITE)
#         date_color = Fore.WHITE

#         # Use the parent class to format the log message with date and level
#         formatted_message = super().format(record)

#         # Apply colors to the formatted message parts
#         date_part = f"{date_color}{record.asctime}{Style.RESET_ALL}"  # Date in white
#         level_part = f"{log_color}{record.levelname}{Style.RESET_ALL}"  # Level in respective color
#         message_part = f"{Fore.WHITE}{record.message}{Style.RESET_ALL}"  # Message in white

#         # Rebuild the final message with colors
#         colored_log = f"{date_part} | {level_part}: {message_part}"

#         return colored_log


# # Set up logger
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# handler.setFormatter(CustomFormatter(fmt="%(asctime)s | %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

# ============================

# import logging
# from colorama import Fore, Style, init

# # Initialize Colorama
# init(autoreset=True)

# # Custom formatter for colored logging
# class CustomFormatter(logging.Formatter):
#     log_format = "%(asctime)s | %(levelname)s: %(message)s"
#     date_format = "%Y-%m-%d %H:%M:%S"

#     COLORS = {
#         logging.DEBUG: Fore.BLUE,
#         logging.INFO: Fore.GREEN,
#         logging.WARNING: Fore.YELLOW,
#         logging.ERROR: Fore.RED,
#         logging.CRITICAL: Fore.RED + Style.BRIGHT,
#     }

#     def format(self, record):
#         log_color = self.COLORS.get(record.levelno, Fore.WHITE)
#         date_color = Fore.WHITE

#         # Use the parent class to format the log message with date and level
#         formatted_message = super().format(record)

#         # Apply colors to the formatted message parts
#         date_part = f"{date_color}{self.formatTime(record, self.date_format)}{Style.RESET_ALL}"
#         level_part = f"{log_color}{record.levelname}{Style.RESET_ALL}"
#         message_part = f"{Fore.WHITE}{record.getMessage()}{Style.RESET_ALL}"

#         # Rebuild the final message with colors
#         colored_log = f"{date_part} | {level_part}: {message_part}"

#         return colored_log


# # Set up logger
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# handler.setFormatter(CustomFormatter(fmt="%(asctime)s | %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

# ============================

# agendardel/logger.py
import logging
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    log_format = "%(asctime)s | %(levelname)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        date_part = f"{Fore.WHITE}{self.formatTime(record, self.date_format)}{Style.RESET_ALL}"
        level_part = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        message_part = f"{Fore.WHITE}{record.getMessage()}{Style.RESET_ALL}"
        return f"{date_part} | {level_part}: {message_part}"

# Setup logger
logger = logging.getLogger("agendardel")
if not logger.handlers:  # Ensure no duplicate handlers
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

logger.propagate = False  # Prevent FastAPI log propagation
