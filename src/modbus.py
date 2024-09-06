# -*- coding: utf-8 -*-

"""
Симулятор данных

(С) 2024 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----


# ---- OUTER ----


# ---- INNER ----
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from src.signal import createSignals

# ---- LOGS ----
from src.logger import LOGGER

###########################################################


def createServers(settings):
    """ """

    signals = createSignals(settings["signals"])
    servers = {}

    extra = {"tag": "Main"}
    LOGGER.info("Creating servers...", extra=extra)

    for name, params in settings["servers"].items():
        servers[name] = ModbusServer(name, params, signals)
        host = {servers[name].host}
        port = {servers[name].port}
        LOGGER.info(f"Creat '{name}': host - {host}, port - {port}", extra=extra)

    t = 1
    return servers


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class Slave:
    """ """

    def __init__(self, name, server, settings, signals):
        """ """

        # Параметры лога
        self.name = name
        self.extra = {"tag": f"{server.name}-{name}"}

        self.slaveID = settings["slaveID"]

        self.server = server.server
        self.slave = self.server.add_slave(self.slaveID)
        self.slave.add_block('0', cst.HOLDING_REGISTERS, 0, 10000)

        self.signals = {}
        for register, name in settings["holdings"].items():
            self.signals[int(register)] = signals[name]
            LOGGER.info(f"Signal '{name}' is attached to holdings {register}", extra=self.extra)


    def write(self):
        """ """

        LOGGER.info(f"write...", extra=self.extra)

        for register, signal in self.signals.items():
            values = signal.next()
            for i in range(len(values)):
                self.slave.set_values('0', register+i, values[i])
                LOGGER.info(f"write [{values[i]}] in holding {register+i}", extra=self.extra)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class ModbusServer:
    """Класс реализующий сервер TCP slave"""

    def __init__(self, name, settings, signals):
        """Инициализирует новый экземпляр класса ModbusServer"""

        # Параметры лога
        self.name = name
        self.extra = {"tag": name}

        # Сетевые настройки
        self.host = settings["host"]
        self.port = settings["port"]

        # Время изменения сигналов в секундах
        time = settings["period"]
        self.period = time[2] + time[1] * 60 + time[0] * 3600

        # Сервер
        self.server = modbus_tcp.TcpServer(self.port, self.host)
        self.slaves = {}
        for name, params in settings["slaves"].items():
            self.slaves[name] = Slave(name, self, params, signals)
            slaveID = self.slaves[name].slaveID
            LOGGER.info(f"Create slave '{name}': slaveID - {slaveID}", extra=self.extra)

    # ---- Управление соединением ----

    def start(self):
        """Запускает сервер"""

        self.server.start()
        #LOGGER.info("Start TCP Slave")

    def stop(self):
        """Останавливает сервер"""

        self.server.stop()
        #LOGGER.info("Stop TCP Slave")

    # ---- Управление данными ----

    def write(self):
        """Записывает данные в регистры, начиная с выбранного"""

        for name, slave in self.slaves.items():
            slave.write()

    def read(self, address: int, count: int) -> list:
        """Читает данные с регистров, начиная с выбранного"""

        return self.slave.get_values('0', address, count)

