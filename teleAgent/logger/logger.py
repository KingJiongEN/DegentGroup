import logging
import os
from pathlib import Path
from colorama import Fore, Style, init

from teleAgent.constants import DATA_STORE_ROOT
from teleAgent.core.config import settings

# Initialize colorama for Windows compatibility
init()

class ColorLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.red = self.red_message

    def red_message(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            msg = f"{Fore.RED}{msg}{Style.RESET_ALL}"
            self._log(logging.INFO, msg, args, **kwargs)

class ColorFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, 'red_message'):
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(
    name: str = 'app_logger', 
    log_files: list = None, 
    level: int = logging.INFO,
    console: bool = True
) -> ColorLogger:
    """
    Set up a logger with the given name, log files, and level.
    Optionally, enable logging to console.
    
    :param name: Name of the logger.
    :param log_files: List of file paths for the log files.
    :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
    :param console: Whether to log to console.
    :return: Configured logger instance.
    """
    if log_files is None:
        log_files = []

    logging.setLoggerClass(ColorLogger)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Ensure each log directory exists and add file handlers
    for log_file in log_files:
        log_dir = Path(log_file).parent
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Console handler configuration
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# Set up a shared logger using settings
shared_logger = setup_logger(
    name='chatgroup_app', 
    log_files=settings.LOG_FILES, 
    level=getattr(logging, settings.LOG_LEVEL.upper()), 
    console=settings.LOG_CONSOLE
)

# Dictionary to store all created logger instances
_loggers = {}

def get_logger(
    name: str = None,
    log_files: list = None,
    level: int = None,
    console: bool = None
) -> ColorLogger:
    """
    Get a configured logger instance.
    If the logger already exists, return the existing instance; otherwise, create a new one.
    
    :param name: Name of the logger. If None, return the shared default logger.
    :param log_files: List of log file paths. If None, use the default log files from settings.
    :param level: Logging level. If None, use the default log level from settings.
    :param console: Whether to log to the console. If None, use the default console setting from settings.
    :return: Configured logger instance.
    """
    # If no name is specified, return the shared default logger
    if name is None:
        return shared_logger
        
    # Check if a logger with the same name already exists
    if name in _loggers:
        return _loggers[name]
        
    # Use default settings if log_files, level, or console are not specified
    log_files = log_files if log_files is not None else settings.LOG_FILES
    level = level if level is not None else getattr(logging, settings.LOG_LEVEL.upper())
    console = console if console is not None else settings.LOG_CONSOLE

    # Create a new logger instance
    logger = setup_logger(
        name=name,
        log_files=log_files,
        level=level,
        console=console
    )
    
    # Store in the logger dictionary
    _loggers[name] = logger
    
    return logger

# Example usage:
# from teleAgent.logger.logger import get_logger
# 
# # Get the default shared logger
# logger = get_logger()
# 
# # Get a logger for a specific module
# module_logger = get_logger('my_module', 
#                          log_files=[f'{DATA_STORE_ROOT}/logs/my_module.log'])
#
# # Get a hierarchical logger in a sub-module
# sub_logger = get_logger('my_module.sub_component')