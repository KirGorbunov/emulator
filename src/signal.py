# -*- coding: utf-8 -*-
"""
Симулятор данных

(С) 2024 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import copy
import struct
import random

# ---- OUTER ----
import pandas as pd

# ---- LOGS ----
from src.logger import LOGGER

###########################################################


def createSignals(settings):
    """ """

    files = {}
    signals = {}

    extra = {"tag": "Main"}
    LOGGER.info("Creating signals...", extra=extra)

    # Перебор сигналов
    for name, params in settings.items():
        params = copy.deepcopy(params)
        if "base" in params:
            path = params["base"][0]
            col = params["base"][1]
            if path not in files:
                files[path] = pd.read_excel(path)
            params["base"] = files[path][col]
            #params["base"] = [random.random() for _ in range(100)]
        signals[name] = Signal(name, params)

    return signals


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class Signal:
    """ """

    def __init__(self, name, params):
        """ """

        self.name = name

        # Базовая часть сигнала
        if "base" in params:
            self.base = params["base"]
            self.base_n = 0
        else:
            self.base = []

        # Тип передаваемого сигнала
        if "type" in params:
            self.type = params["type"]
        else:
            self.type = ""

        # Константа
        if "constant" in params:
            self.constant = params["constant"]
        else:
            self.constant = 0

        self._generator = self._dataGenerator()

    # ---- Внутренняя логика ----

    def _getBase(self):
        """ """

        if len(self.base):
            self.base_n = self.base_n + 1 if self.base_n + 1 < len(self.base) else 0
            return self.base[self.base_n]
        else:
            return 0

    def _dataGenerator(self):
        """Генерация данных"""

        TS = 0
        while True:
            x = self.constant
            x += self._getBase()
            yield x
            TS += 1

    # ---- Управление соединением ----

    def next(self, n=1):
        """ """

        n = max(1, n)
        result = []

        for _ in range(n):
            value = self._generator.__next__()
            if self.type == "ushort-float16":
                buf = min(max(value, -65534), 65535)
                value = struct.unpack('H', struct.pack('e', buf))
            elif self.type == "ushort-float32":
                buf = min(max(value, -4294967294), 4294967295)
                value = struct.unpack('HH', struct.pack('f', buf))[::-1]
            elif self.type == "ushort-int16":
                buf = int(min(max(value, -65534), 65535))
                value = struct.unpack('H', struct.pack('h', buf))
            elif self.type == "ushort-int32":
                buf = int(min(max(value, -4294967294), 4294967295))
                value = struct.unpack('HH', struct.pack('i', buf))[::-1]
            else:
                value = [value]
            result.extend(value)

        return result
