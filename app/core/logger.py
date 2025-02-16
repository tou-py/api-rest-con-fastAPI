import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    name: str, log_file: str = "app.log", level: int = logging.INFO
) -> logging.Logger:
    """
    Configura y retorna un logger

    Args:
        name (str): nombre del logger
        log_file (str): nombre del archivo log
        level (int): nivel del logging (puede ser, logging.INFO, logging.DEBUG, etc.)
    Returns:
        logging.Logger: Instancia del logger configurado
    """
    # Se crea el directorio si este no existe
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    # Crear el logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configurar un handler del archivo
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Se establecen 5 MB por archivo, 3 archivos de respaldo
    file_handler = RotatingFileHandler(
        log_directory / log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


app_logger = setup_logger("app_logger")
