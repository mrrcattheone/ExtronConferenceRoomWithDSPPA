import socket
import time
import logs_screen
from extronlib.interface import SerialInterface


class Devices_Command:
    def __init__(
        self,
        receiving_object: object,
        content,
        priority: int,
        ip: str = None,
        port: int = None,
    ):
        self.receiving_object = receiving_object
        self.content = content
        self.priority = priority
        self.ip = ip
        self.port = port


class Send_Queie:
    def __init__(self):
        self.queue = []

    def append(self, message):
        self.queue.append(message)
        self.queue.sort(key=lambda msg: msg.priority)

    def get(self):
        return self.queue

    def process(self):

        if not self.queue:  # Проверяем, пуста ли очередь
            print("No messages in the queue.")
            logs_screen.custom_logger("No messages in the queue.")
            return

        for message in self.queue:
            receiving_object = message.receiving_object
            content = message.content
            ip_address = message.ip
            port = message.port
            if not isinstance(content, bytes):
                content = content.encode("utf-8")

            if isinstance(receiving_object, socket.socket):
                try:
                    # logs_screen.custom_logger("Output from Queie.process method:")
                    # # logs_screen.custom_logger(str(receiving_object))
                    # # logs_screen.custom_logger(type(receiving_object))
                    # logs_screen.custom_logger(str(content))
                    # logs_screen.custom_logger(str(type(content)))
                    # logs_screen.custom_logger(ip_address)
                    # logs_screen.custom_logger(str(type(ip_address)))
                    # logs_screen.custom_logger(port)
                    # logs_screen.custom_logger(str(type(port)))
                    receiving_object.sendto(content, (ip_address, int(port)))
                    time.sleep(0.05)
                    logs_screen.custom_logger("Ethernet interface: Command send")
                    print("Ethernet interface: Command send")
                except Exception as e:
                    print("Ethernet interface: Unable to send data", str(e))
                    logs_screen.custom_logger(
                        "Ethernet interface: Unable to send data", str(e)
                    )

            elif isinstance(receiving_object, SerialInterface):
                try:
                    # Если объект является экземпляром класса SerialInterface
                    receiving_object.Send(
                        content
                    )  # Выполняем команду для интерфейса SerialInterface
                    print("Serial interface: Command send")
                    logs_screen.custom_logger("Serial interface: Command send")
                except Exception as e:
                    print("Ethernet interface: Unable to send data", str(e))
                    logs_screen.custom_logger(
                        "Ethernet interface: Unable to send data", str(e)
                    )

            else:
                # Обработка других типов объектов
                print("Unknown object type")
            self.queue.remove(message)

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []


send_queue = Send_Queie()
