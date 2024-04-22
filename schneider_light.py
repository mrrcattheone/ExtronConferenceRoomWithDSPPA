from struct import pack
from extronlib.interface import EthernetClientInterface
from extronlib.device import UIDevice
from extronlib.ui import Button
from extronlib import event
from extronlib.system import Timer, Wait

import time     # For monotonic()
import socket
import logs_screen
from universal_sender import *


# schneider_server=EthernetClientInterface('10.96.32.20', 502)
schneider_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
light_server_connect = False
connected_light = None
delay_duration = 5
delay_active = False
schneider_server_ip = '10.96.32.20'
schneider_server_port = 502



def Initialize():
    schneider_server.connect((schneider_server_ip, schneider_server_port))
    print('Connection initiated to schneider server')
    logs_screen.custom_logger('Connection initiated to schneider server')    

    
def __SetHelper(PowerCmdString, priority):
    global light_server_connect
    global delay_active
    
    if delay_active == True:
        print("Delay active. Unable to send data.")
    elif delay_active == False:
        delay_active = True

        if light_server_connect == True:
            # schneider_server.Send(PowerCmdString)            
            schneider_server_command = DevicesCommand(schneider_server, PowerCmdString, priority, schneider_server_ip, schneider_server_port)
            send_queue.append(schneider_server_command)
            send_queue.process()
            print('command sent to schneider server')
            logs_screen.custom_logger('command sent to schneider server')        

        else:
            print('Command not send. Check connection to light server.')
            logs_screen.custom_logger('Command not send. Check connection to light server.')

        time.sleep(delay_duration)
        delay_active = False
        print("Delay deactivated.")

        # Regex to make sure Update helper only catches 2 messages
        # Feedback on query when register is configured:
        # e.g. \x05\xA6\x00\x00\x00\x05\x0C\x03\x02\x00\x10
        # Feedback on query when register is not or incorrectly configured:
        # e.g. \x05\xA6\x00\x00\x00\x03\x0C\x83\x02


def command_selector(light_power_btn_id):
    command_list = {
        191 : {'command1': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x0B', 'command2': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x00', 'descr' : 'light 1 ON'},
        190 : {'command1': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x0A', 'command2': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x00', 'descr' : 'light 1 OFF'},
        192 : {'command1': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x15', 'command2': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x00', 'descr' : 'light 2 ON'},
        193 : {'command1': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x14', 'command2': b'\x05\xA6\x00\x00\x00\x06\x0C\x06\x00\x64\x00\x00', 'descr' : 'light 2 OFF'}
    }

    if light_power_btn_id in command_list:
        command = command_list[light_power_btn_id]
        if 'command1' in command:
            __SetHelper(command['command1'], 3)
        # if 'command2' in command:
        #     __SetHelper(command['command2'])
            logs_screen.custom_logger(command['descr'])
            print(command['descr'])


Initialize()