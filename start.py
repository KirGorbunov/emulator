# -*- coding: utf-8 -*-
"""
Симулятор данных

(С) 2024 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import copy
import os
import csv
import json
import time
import logging
from datetime import datetime

# ---- OUTER ----

# ---- INNER ----
from src.signal import createSignals
from src.modbus import createServers
from src.logger import updatePath

# ---- LOGS ----
from src.logger import LOGGER

###########################################################


def plot(data):
    """ """

    import matplotlib.pyplot as plt

    for name, values in data:
        plt.plot(values, label=name)

    plt.legend()
    plt.show()


def main():
    """ """

    debug = 0
    extra = {"tag": "Main"}

    # Чтение конфига
    with open("config.json", "r") as f:
        config = json.loads(f.read())

    # Проверка сигналов
    if debug:

        signals = createSignals(config["signals"])
        data = []
        for name, signal in signals.items():
            data.append([name, signal.next(8000)])
        plot(data)
    # Запуск
    else:
        LOGGER.info(f"Mimic start", extra=extra)

        servers = createServers(config)
        period = 10
        for name, server in servers.items():
            server.start()
            period = server.period

        while True:
            for name, server in servers.items():
                server.write()
            time.sleep(period)


if __name__ == '__main__':
    main()
