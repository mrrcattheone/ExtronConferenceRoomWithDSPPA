import socket
import threading
import time

from extronlib import event, Version
from extronlib.interface import EthernetClientInterface
from extronlib.system import Timer, Wait
from extronlib.system import GetSystemUpTime, Ping, ProgramLog, WakeOnLan
from extronlib.device import UIDevice
from extronlib.ui import Button

from lcd_const import *
from lcd_utils import *
from universal_sender import *
import logs_screen


# globals
current_tv_mac = ""
current_tv_ip = ""
current_tv_port = 0
current_tv_id = ""
tv_connection_state = False
lcd_command_priority = 10

# TV ADDRESSES LIST
tv_addresses = {
    19: {"ip": "10.90.5.61", "port": 9761, "mac": "74-E6-B8-4F-69-39", "id": "01"},
    20: {"ip": "10.90.5.62", "port": 9761, "mac": "74-E6-B8-4F-69-7E", "id": "02"},
    21: {"ip": "10.90.5.63", "port": 9761, "mac": "74-E6-B8-4F-68-B2", "id": "03"},
    22: {"ip": "10.90.5.64", "port": 9761, "mac": "74-E6-B8-4F-69-C7", "id": "04"},
    23: {"ip": "10.90.5.65", "port": 9761, "mac": "74-E6-B8-4F-69-3E", "id": "05"},
    24: {"ip": "10.90.5.66", "port": 9761, "mac": "74-E6-B8-4F-69-1E", "id": "06"},
    25: {"ip": "10.90.5.67", "port": 9761, "mac": "74-E6-B8-4F-69-B9", "id": "07"},
    26: {"ip": "10.90.5.68", "port": 9761, "mac": "74-E6-B8-4F-69-7D", "id": "08"},
    27: {"ip": "10.90.5.69", "port": 9761, "mac": "7C-64-6C-D0-C0-74", "id": "09"},
}


# INIT GUI OBJECTS
def init_buttons(webgui: UIDevice):
    print("Initializing TV control buttons")
    logs_screen.custom_logger("Initializing TV control buttons")
    LCD_IDS[19] = Button(webgui, 19, holdTime=None, repeatTime=None)  # TV1 btn
    LCD_IDS[20] = Button(webgui, 20, holdTime=None, repeatTime=None)  # TV2 btn
    LCD_IDS[21] = Button(webgui, 21, holdTime=None, repeatTime=None)  # TV3 btn
    LCD_IDS[22] = Button(webgui, 22, holdTime=None, repeatTime=None)  # TV4 btn
    LCD_IDS[23] = Button(webgui, 23, holdTime=None, repeatTime=None)  # TV5 btn
    LCD_IDS[24] = Button(webgui, 24, holdTime=None, repeatTime=None)  # TV6 btn
    LCD_IDS[25] = Button(webgui, 25, holdTime=None, repeatTime=None)  # TV7 btn
    LCD_IDS[26] = Button(webgui, 26, holdTime=None, repeatTime=None)  # TV8 btn
    LCD_IDS[27] = Button(webgui, 27, holdTime=None, repeatTime=None)  # TV9 btn

    LCD_NUMBER_PADS[28] = Button(webgui, 28, holdTime=None, repeatTime=None)  # 1 btn
    LCD_NUMBER_PADS[29] = Button(webgui, 29, holdTime=None, repeatTime=None)  # 2 btn
    LCD_NUMBER_PADS[30] = Button(webgui, 30, holdTime=None, repeatTime=None)  # 3 btn
    LCD_NUMBER_PADS[31] = Button(webgui, 31, holdTime=None, repeatTime=None)  # 4 btn
    LCD_NUMBER_PADS[32] = Button(webgui, 32, holdTime=None, repeatTime=None)  # 5 btn
    LCD_NUMBER_PADS[33] = Button(webgui, 33, holdTime=None, repeatTime=None)  # 6 btn
    LCD_NUMBER_PADS[34] = Button(webgui, 34, holdTime=None, repeatTime=None)  # 7 btn
    LCD_NUMBER_PADS[35] = Button(webgui, 35, holdTime=None, repeatTime=None)  # 8 btn
    LCD_NUMBER_PADS[36] = Button(webgui, 36, holdTime=None, repeatTime=None)  # 9 btn
    LCD_NUMBER_PADS[120] = Button(webgui, 120, holdTime=None, repeatTime=None)  # 0 btn

    LCD_POWER[42] = Button(webgui, 42, holdTime=None, repeatTime=None)  # Power ON btn
    LCD_POWER[97] = Button(webgui, 97, holdTime=None, repeatTime=None)  # Power OFF btn

    LCD_ACTIONS[76] = Button(webgui, 76, holdTime=None, repeatTime=None)  # menu
    LCD_ACTIONS[121] = Button(webgui, 121, holdTime=None, repeatTime=None)  # back
    LCD_ACTIONS[122] = Button(webgui, 122, holdTime=None, repeatTime=None)  # exit
    LCD_ACTIONS[38] = Button(webgui, 38, holdTime=None, repeatTime=None)  # up
    LCD_ACTIONS[37] = Button(webgui, 37, holdTime=None, repeatTime=None)  # left
    LCD_ACTIONS[40] = Button(webgui, 40, holdTime=None, repeatTime=None)  # enter
    LCD_ACTIONS[39] = Button(webgui, 39, holdTime=None, repeatTime=None)  # right
    LCD_ACTIONS[41] = Button(webgui, 41, holdTime=None, repeatTime=None)  # down


# INIT BTN GROUPS FOR TV CONTROL
def init_lcd_control_group():
    print("Initializing LCD control group")
    logs_screen.custom_logger("Initializing LCD control group")
    append_to_lcd_ids_grp(LCD_IDS.values())
    append_to_action_grp(LCD_ACTIONS.values())
    append_to_power_grp(LCD_POWER.values())
    append_to_number_pads_grp(LCD_NUMBER_PADS.values())


# CHANGE TV NODE IF IT IS IN LIST. SET PARAMS TO GLOBAL
def lcd_node_changer(node_btn_id):
    global current_tv_mac, current_tv_ip, current_tv_port, current_tv_id
    if node_btn_id in tv_addresses:
        tv_info = tv_addresses[node_btn_id]
        current_tv_mac = tv_info["mac"]
        current_tv_ip = tv_info["ip"]
        current_tv_port = tv_info["port"]
        current_tv_id = tv_info["id"]
        print("TV selected sucessfully")
        logs_screen.custom_logger("TV selected sucessfully")
        connect_to_tv()
    else:
        print("Error. Btn_id not found in tv list.")
        logs_screen.custom_logger("Error. Btn_id not found in tv list.")

    for btn in LCD_IDS_GRP:
        if btn.ID == node_btn_id:
            btn.SetState(1)
        else:
            btn.SetState(0)


# CONNECTION CHECK
def connect_to_tv():
    global tv_connection_state
    if current_tv_id != "":
        try:
            # SET TV CONNECTION
            tv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tv_socket.settimeout(2)  # RECONNECT TIMEOUT
            tv_socket.connect((current_tv_ip, current_tv_port))
            tv_connection_state = True
            tv_socket.close()
            print("Connection to TV sucessfull")
            logs_screen.custom_logger("Connection to TV sucessfull")
        except:
            print("Error connecting selected TV.")
            logs_screen.custom_logger("Error connecting selected TV.")
            tv_connection_state = False


# CREATE NEW DEVICES_COMMAND MESSAGE AND PULL TO SEND QUEIE
def send_data_to_tv(data):
    global tv_connection_state
    if tv_connection_state == True:
        try:
            tv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tv_socket.settimeout(1)
            tv_socket.connect((current_tv_ip, current_tv_port))
            tv_socket_command = Devices_Command(
                tv_socket,
                data.encode(),
                lcd_command_priority,
                current_tv_ip,
                current_tv_port,
            )
            send_queue.append(tv_socket_command)
            send_queue.process()
            tv_socket.close()
        except:
            print("Error sending data.")
            logs_screen.custom_logger("Error sending data.")
    else:
        print("No connection. Can`t be send.")


def tv_connection_thread():
    connect_to_tv()


def connect_to_tv_async():
    tv_thread = threading.Thread(target=tv_connection_thread)
    tv_thread.start()


# TV POWER STATE SET
def tv_power_control(tv_btn_id):
    global tv_addresses
    global current_tv_id
    global tv_connection_state
    if current_tv_id != "":
        if tv_btn_id == 42:
            WakeOnLan(current_tv_mac, port=9)
        elif tv_btn_id == 97:
            if tv_connection_state == True:
                PowerCmdString = "ka {0} 00".format(current_tv_id)  # ka {0} 00\r
                send_data_to_tv(PowerCmdString)
                print("TV power command send to sender from tv_power_control")
                logs_screen.custom_logger(
                    "TV power command send to sender from tv_power_control"
                )
            else:
                logs_screen.custom_logger(
                    "Unable t send command. TV not connected. Check connection."
                )
                print("Unable t send command. TV not connected. Check connection.")


# set number on pad
def set_keypad(tv_btn_id):
    global tv_connection_state
    global current_tv_id
    if tv_connection_state == True:

        ValueStateValues = {
            28: {"key": "11"},
            29: {"key": "12"},
            30: {"key": "13"},
            31: {"key": "14"},
            32: {"key": "15"},
            33: {"key": "16"},
            34: {"key": "17"},
            35: {"key": "18"},
            36: {"key": "19"},
            120: {"key": "10"},
        }
        if tv_btn_id in ValueStateValues:
            value = ValueStateValues[tv_btn_id]
            PowerCmdString = "mc {0} {1} 20 0D".format(
                int(current_tv_id), ValueStateValues[tv_btn_id]["key"]
            )
            send_data_to_tv(PowerCmdString)
            print("TV command send to sender from set_keypad")
            logs_screen.custom_logger("TV command send to sender from set_keypad")
        else:
            logs_screen.custom_logger("Invalid btn ID in keypad")
            print("Invalid btn ID in keypad")
    else:
        print("Unable to connect TV. Check connection first.")
        logs_screen.custom_logger("Unable to connect TV. Check connection first.")


# NAVIGATION COMMANDS
def menu_navigation(tv_btn_id):
    global tv_connection_state
    global current_tv_id
    if tv_connection_state == True:
        """Set Menu Navigation
        value: Enum
        qualifier: {'Device ID' : Enum}
        """

        ValueStateValues = {
            76: {"value": "43"},
            121: {"value": "28"},
            122: {"value": "5B"},
            38: {"value": "40"},
            37: {"value": "07"},
            40: {"value": "44"},
            39: {"value": "06"},
            41: {"value": "41"},
        }
        #         ValueStateValues = {
        #     'Up'   : '40',
        #     'Down' : '41',
        #     'Left' : '07',
        #     'Right': '06',
        #     'Enter': '44',
        #     'Back' : '28',
        #     'Exit' : '5B',
        #     'Menu' : '43'
        # }

        if tv_btn_id in ValueStateValues:
            MenuNavigationCmdString = "mc {0} {1} 20 0D".format(
                int(current_tv_id), ValueStateValues[tv_btn_id]["value"]
            )
            send_data_to_tv(MenuNavigationCmdString)
            print("TV command send to sender from menu_navigation")
            logs_screen.custom_logger("TV command send to sender from menu_navigation")
        else:
            print("Invalid Command")
            logs_screen.custom_logger("Invalid Command")


# total power off
def total_power_off():
    global current_tv_ip, current_tv_port, tv_connection_state

    tv_connection_state = True
    for key, value in tv_addresses.items():
        current_tv_ip = value["ip"]
        current_tv_port = value["port"]
        PowerCmdString = "ka {0} 00".format(value["id"])  # ka {0} 00\r
        send_data_to_tv(PowerCmdString)
        time.sleep(1)  # Pause for 1 second

    lcd_launch_reset()

    print("All TVs power down")
    logs_screen.custom_logger("All TVs power down")


# total power up
def total_power_on():
    for key, value in tv_addresses.items():
        WakeOnLan(value["mac"], port=9)
        time.sleep(1)  # Pause for 1 second
    lcd_launch_reset()
    print("All TVs power up")
    logs_screen.custom_logger("All TVs power up")


def lcd_launch_reset():
    for btn in LCD_IDS_GRP:
        btn.SetState(0)

    global current_tv_mac
    current_tv_mac = ""
    global current_tv_ip
    current_tv_ip = ""
    global current_tv_port
    current_tv_port = 0
    global current_tv_id
    current_tv_id = ""
    global tv_connection_state
    tv_connection_state = False
    print("TV states reset")
    logs_screen.custom_logger("TV states reset")
