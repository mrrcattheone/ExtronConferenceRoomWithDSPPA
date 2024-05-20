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
                    receiving_object.sendto(content, (ip_address, int(port)))
                    # time.sleep(0.09)
                    logs_screen.custom_logger("Ethernet interface: Command send")
                    print("Ethernet interface: Command send")
                    if ip_address in [
                        "10.90.5.53",
                        "10.90.5.52",
                        "10.90.5.51",
                    ]:  # TODO IF no connection on socket - error
                        state = "WAIT_FOR_ANSWER1"
                        while True:
                            if state == "WAIT_FOR_ANSWER1":
                                answer1 = receiving_object.recv(1024)
                                if answer1:
                                    state = "WAIT_FOR_ANSWER2"
                                    time.sleep(0.01)
                                    logs_screen.custom_logger(
                                        "WAIT_FOR_ANSWER1: First answer received"
                                    )
                                else:
                                    # First answer not received, resend command
                                    self.queue.insert(0, message)
                                    logs_screen.custom_logger(
                                        "WAIT_FOR_ANSWER1: First lost, resend command"
                                    )
                                    break
                            elif state == "WAIT_FOR_ANSWER2":
                                answer2 = receiving_object.recv(1024)
                                if answer2:
                                    # Both answers received, remove message from queue
                                    self.queue.remove(message)
                                    time.sleep(0.01)
                                    logs_screen.custom_logger("Both answers received")
                                    break
                                else:
                                    # Second answer not received, resend command
                                    self.queue.insert(0, message)
                                    logs_screen.custom_logger(
                                        "WAIT_FOR_ANSWER2: Second lost, resend command"
                                    )
                                    break
                    else:
                        self.queue.remove(message)

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
                    self.queue.remove(message)
                except Exception as e:
                    print("Ethernet interface: Unable to send data", str(e))
                    logs_screen.custom_logger(
                        "Ethernet interface: Unable to send data", str(e)
                    )

            else:
                # Обработка других типов объектов
                print("Unknown object type")

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []


send_queue = Send_Queie()
