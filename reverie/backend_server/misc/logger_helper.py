import sys
import logging
from loguru import logger
from pathlib import Path

def configure_loguru_integration(
    log_dir,
    log_file,
    mode='a',
    console=True,
    log_level='DEBUG',
    intercept=True,
    filter_packages=['httpcore', 'httpx'],
    log_args={}):
    """
    Sets up and configures Loguru logger integration with Python's logging module.

    Parameters:
        log_dir (str): Directory where log files will be stored.
        log_file (str): Filename for the log file.
        mode (str): Mode for file writing (default 'a' for append).
        log_level (str): Minimum level of messages to log.
        intercept (bool): If True, intercepts messages from logging module.
        filter_packages (list): Optional list of packages for which to set logging level to CRITICAL.
        log_args (dict): Additional arguments for setting up stderr logging.

    Returns:
        loguru.Logger: Configured Loguru logger object.
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        log_path.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(log_path / log_file, level=log_level, mode=mode, **log_args)
    if console:
        logger.add(sys.stderr, level=log_level)

    if intercept:
        class InterceptHandler(logging.Handler):
            def emit(self, record):
                loguru_level = logger.level(record.levelname).name if record.levelname in logger._core.levels else record.levelno
                frame, depth = logging.currentframe(), 2
                while frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1
                logger.opt(depth=depth, exception=record.exc_info).log(loguru_level, record.getMessage())

        root_logger = logging.getLogger()
        root_logger.handlers = [InterceptHandler()]
        root_logger.setLevel(log_level)

    if filter_packages:
        for package in filter_packages:
            logging.getLogger(package).setLevel(logging.CRITICAL)

    return logger


if __name__ == "__main__":
    configure_loguru_integration(log_dir='logs', log_file='app.log', log_level='DEBUG', filter_packages=['httpx'])

    logging.getLogger('example_library').debug('This is a debug message from the library')
