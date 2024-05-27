import threading
import socket
import time
import logs_screen
from threading import Thread
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


class ListenerThread(Thread):
    def __init__(self, receiving_object, queue, message):
        super().__init__()
        self.receiving_object = receiving_object
        self.queue = queue
        self.message = message
        self.answer1 = None
        self.answer2 = None

    def run(self):
        while True:
            self.answer1 = self.receiving_object.recv(1024)
            if self.answer1:
                break

        while True:
            self.answer2 = self.receiving_object.recv(1024)
            if self.answer2:
                break

        if self.answer1 and self.answer2:
            self.queue.remove(self.message)
            time.sleep(0.3)
            logs_screen.custom_logger("Both answers received")
        else:
            self.queue.insert(0, self.message)
            logs_screen.custom_logger("Answers lost, resend command")


class Send_Queue:

    # Init sending operations queue.
    def __init__(self):
        self.queue = []

    # Adds new message to queue. Contains socket or serial port, command, priority, ip address and port, if needed.
    def append(self, message):
        self.queue.append(message)
        self.queue.sort(key=lambda msg: msg.priority)

    # Special sender only for ethernet interface. Works after process method.
    def send_message_ethernet(self, message, event):
        receiving_object = message.receiving_object
        content = message.content
        ip_address = message.ip
        port = message.port
        try:
            receiving_object.sendto(content, (ip_address, int(port)))
            logs_screen.custom_logger("Ethernet interface: Command send")
            print("Ethernet interface: Command send")

            if ip_address in ["10.90.5.53", "10.90.5.52", "10.90.5.51"]:
                listener_thread = ListenerThread(receiving_object, self.queue, message)
                listener_thread.start()
                listener_thread.join(timeout=0.5)
            # else:
            #     self.queue.remove(message)

        except Exception as e:
            print("Ethernet interface: Unable to send data")
            logs_screen.custom_logger("Ethernet interface: Unable to send data")
        event.set()  # Set function endpoint

    # Special sender only for serial interface. Works after process method.
    def send_message_serial(self, message, event):
        receiving_object = message.receiving_object
        content = message.content
        try:
            receiving_object.Send(content)
            logs_screen.custom_logger("Serial interface: Command send")
            print("Serial interface: Command send")
            # self.queue.remove(message)

        except Exception as e:
            print("Serial interface: Unable to send data")
            logs_screen.custom_logger("Serial interface: Unable to send data")
        event.set()  # Set function endpoint

    # Select first item from queue and define its instance to send it with right interface.
    def process(self):
        if not self.queue:
            print("No messages in the queue.")
            logs_screen.custom_logger("No messages in the queue.")
            return

        while self.queue:
            message = self.queue[0]
            receiving_object = message.receiving_object

            # if not isinstance(content, bytes):
            #     content = message.content.encode("utf-8")

            if isinstance(receiving_object, socket.socket):
                try:
                    # Create listener for endpoint in send_message_ethernet
                    event_ethernet = threading.Event()

                    # Ethernet interface command send in separate thread
                    thread_ethernet = threading.Thread(
                        target=self.send_message_ethernet,
                        args=(message, event_ethernet),
                    )
                    thread_ethernet.start()

                    # Waiting endpoint send_message_ethernet
                    event_ethernet.wait()
                    self.queue.remove(message)
                except Exception as e:
                    print("Ethernet interface: Unable to send data")
                    logs_screen.custom_logger("Ethernet interface: Unable to send data")

            elif isinstance(receiving_object, SerialInterface):
                try:
                    # Create listener for endpoint in send_message_serial
                    event_serial = threading.Event()

                    # Serial interface command send in separate thread
                    thread_serial = threading.Thread(
                        target=self.send_message_serial,
                        args=(message, event_serial),
                    )
                    thread_serial.start()

                    # Waiting endpoint send_message_serial
                    event_serial.wait()
                    self.queue.remove(message)

                except Exception as e:
                    print("Serial interface: Unable to send data")
                    logs_screen.custom_logger("Serial interface: Unable to send data")

            else:
                print("Unknown receiving object type.")
                logs_screen.custom_logger("Unknown receiving object type.")
                self.queue.remove(message)


send_queue = Send_Queue()
