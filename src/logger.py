# -*- coding: utf-8 -*-
"""
Функционал для работы лога

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# -- BUILT --
import os
import logging
from datetime import datetime

# ---- INNER ----
import modbus_tk.utils

# ---- GLOBAL AND CONSTANT ----
MODBUS_LOGGER = modbus_tk.utils.create_logger()

###########################################################


def createLogger(path, logName="", level=logging.INFO, logger=None, tag="%(tag)s"):
    """
    Настраивает и возвращает логгер. Может настроить уже созданный логгер

    Parameters
    ----------
    path: str
        Имя файла (путь) для сохранения лога
    logName: str, optional
        Системное имя лога
    level: int, optional
        Уровень ведения лога
    logger: logging.Logger, optional
        Логгер. Если необходимо не создать новый, а добавить вывод в старый
    tag: str, optional
        Тег записи

    Returns
    -------
    logging.Logger
        Логгер
    """

    # Создание пути к логу, если он не существует
    dirPath = os.path.dirname(path)
    if dirPath and not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # Создание нового лога, если имя не пустое
    if logName:
        logger = logging.Logger(logName)
        logger.setLevel(level)

    # Создание методов вывода
    fileHandle = logging.FileHandler(path)
    consoleHandle = logging.StreamHandler()
    # Шаблон записи
    formatter = logging.Formatter(f"%(asctime)s [{tag}][%(levelname)s] - "
                                  f"%(message)s", "%d.%m.%Y %H:%M:%S")
    fileHandle.setFormatter(formatter)
    consoleHandle.setFormatter(formatter)

    # Привязка методов вывода
    logger.addHandler(consoleHandle)
    logger.addHandler(fileHandle)

    return logger


def updatePath(logs: list, name: str, oldPath: str) -> str:
    """Обновление пути логов. Возвращает новый путь логов"""

    newPath = f"{name} - {datetime.now().strftime('%y.%m')}.log"

    if newPath == oldPath:
        return oldPath

    else:
        for log in logs:
            stream = open(newPath, 'a')

            # Подмена пути к логам, предполагается, что fileHandle последний
            fileHandle = log.handlers[-1]
            fileHandle.setStream(stream)

        return newPath


# ---- LOGS ----
logName = "logs/mimic"
logPath = f"{logName} - {datetime.now().strftime('%y.%m')}.log"
LOGGER = createLogger(logPath, "main_log", logging.DEBUG)
createLogger(logPath, logger=MODBUS_LOGGER, level=logging.DEBUG, tag="Modbus")

