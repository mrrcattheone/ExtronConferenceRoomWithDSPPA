from extronlib import event, Version
from extronlib.interface import EthernetClientInterface
from extronlib.system import Timer, Wait
from extronlib.system import GetSystemUpTime, Ping, ProgramLog, WakeOnLan
from extronlib.device import UIDevice
from extronlib.ui import Button

from struct import pack #FOR PACKING COMMANDS STR TO BYTE

import time     # For monotonic()
import socket

from lcd_const import *
from lcd_utils import *
import logs_screen

# update power state 
# PowerCmdString = 'ka {0} FF\r'.format(ID)

tv_node = EthernetClientInterface('10.90.5.61', 9761, 'TCP') #FIRST TV 
tv_connected = None
connect_state = False
id_tv = "01"
selected_tv=0
selected_tv_mac=''

#TV ADDRESSES LIST
tv_addresses = {
    19 : {'ip': '10.90.5.61', 'port': 9761, 'mac': '74-E6-B8-4F-69-39', 'id': '01' },
    20 : {'ip': '10.90.5.62', 'port': 9761, 'mac': '74-E6-B8-4F-69-7E', 'id': '02' },
    21 : {'ip': '10.90.5.63', 'port': 9761, 'mac': '74-E6-B8-4F-68-B2', 'id': '03' },
    22 : {'ip': '10.90.5.64', 'port': 9761, 'mac': '74-E6-B8-4F-69-C7', 'id': '04' },
    23 : {'ip': '10.90.5.65', 'port': 9761, 'mac': '74-E6-B8-4F-69-3E', 'id': '05' },
    24 : {'ip': '10.90.5.66', 'port': 9761, 'mac': '74-E6-B8-4F-69-1E', 'id': '06' },
    25 : {'ip': '10.90.5.67', 'port': 9761, 'mac': '74-E6-B8-4F-69-B9', 'id': '07' },
    26 : {'ip': '10.90.5.68', 'port': 9761, 'mac': '74-E6-B8-4F-69-7D', 'id': '08' },
    27 : {'ip': '10.90.5.69', 'port': 9761, 'mac': '7C-64-6C-D0-C0-74', 'id': '09' }
}  

#INIT GUI OBJECTS
def init_buttons(webgui: UIDevice):
    print("Initializing TV control buttons")
    logs_screen.custom_logger("Initializing TV control buttons")
    LCD_IDS[19] = Button(webgui, 19, holdTime=None, repeatTime=None)    #TV1 btn
    LCD_IDS[20] = Button(webgui, 20, holdTime=None, repeatTime=None)    #TV2 btn
    LCD_IDS[21] = Button(webgui, 21, holdTime=None, repeatTime=None)    #TV3 btn
    LCD_IDS[22] = Button(webgui, 22, holdTime=None, repeatTime=None)    #TV4 btn
    LCD_IDS[23] = Button(webgui, 23, holdTime=None, repeatTime=None)    #TV5 btn
    LCD_IDS[24] = Button(webgui, 24, holdTime=None, repeatTime=None)    #TV6 btn
    LCD_IDS[25] = Button(webgui, 25, holdTime=None, repeatTime=None)    #TV7 btn
    LCD_IDS[26] = Button(webgui, 26, holdTime=None, repeatTime=None)    #TV8 btn
    LCD_IDS[27] = Button(webgui, 27, holdTime=None, repeatTime=None)    #TV9 btn

    LCD_NUMBER_PADS[28] = Button(webgui, 28, holdTime=None, repeatTime=None)    #1 btn
    LCD_NUMBER_PADS[29] = Button(webgui, 29, holdTime=None, repeatTime=None)    #2 btn
    LCD_NUMBER_PADS[30] = Button(webgui, 30, holdTime=None, repeatTime=None)    #3 btn
    LCD_NUMBER_PADS[31] = Button(webgui, 31, holdTime=None, repeatTime=None)    #4 btn
    LCD_NUMBER_PADS[32] = Button(webgui, 32, holdTime=None, repeatTime=None)    #5 btn
    LCD_NUMBER_PADS[33] = Button(webgui, 33, holdTime=None, repeatTime=None)    #6 btn
    LCD_NUMBER_PADS[34] = Button(webgui, 34, holdTime=None, repeatTime=None)    #7 btn
    LCD_NUMBER_PADS[35] = Button(webgui, 35, holdTime=None, repeatTime=None)    #8 btn
    LCD_NUMBER_PADS[36] = Button(webgui, 36, holdTime=None, repeatTime=None)    #9 btn
    LCD_NUMBER_PADS[120] = Button(webgui, 120, holdTime=None, repeatTime=None)    #0 btn

    LCD_POWER[42] = Button(webgui, 42, holdTime=None, repeatTime=None)    #Power ON btn
    LCD_POWER[97] = Button(webgui, 97, holdTime=None, repeatTime=None)    #Power OFF btn
    
    LCD_ACTIONS[76] = Button(webgui, 76, holdTime=None, repeatTime=None)  #menu
    LCD_ACTIONS[121] = Button(webgui, 121, holdTime=None, repeatTime=None)  #back
    LCD_ACTIONS[122] = Button(webgui, 122, holdTime=None, repeatTime=None)  #exit
    LCD_ACTIONS[38] = Button(webgui, 38, holdTime=None, repeatTime=None)  #up
    LCD_ACTIONS[37] = Button(webgui, 37, holdTime=None, repeatTime=None)  #left
    LCD_ACTIONS[40] = Button(webgui, 40, holdTime=None, repeatTime=None)  #enter
    LCD_ACTIONS[39] = Button(webgui, 39, holdTime=None, repeatTime=None)  #right
    LCD_ACTIONS[41] = Button(webgui, 41, holdTime=None, repeatTime=None)  #down

#INIT BTN GROUPS FOR TV CONTROL
def init_lcd_control_group():
    print("Initializing LCD control group")
    logs_screen.custom_logger("Initializing LCD control group")
    append_to_lcd_ids_grp(LCD_IDS.values())
    append_to_action_grp(LCD_ACTIONS.values())
    append_to_power_grp(LCD_POWER.values())
    append_to_number_pads_grp(LCD_NUMBER_PADS.values())



def connect_to_tv_node(ip, port):
    global tv_socket
    try:
        tv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tv_socket.settimeout(10)  # Устанавливаем таймаут в 10 секунд
        tv_socket.connect((ip, port))
        tv_socket.close()
        print("Connected to tv_node successfully!")
        # Добавьте здесь любую логику или действия, которые требуются после успешного подключения
    except:
        print("Unable to connect to tv_node")
        # Добавьте здесь любую логику или обработку ошибок, если подключение не удалось


#TV ID AND ADDRESS SELECT
def lcd_node_changer(tv_btn_id):
    global tv_node
    global tv_addresses
    global id_tv
    global selected_tv
    global selected_tv_mac
    
    if tv_btn_id in tv_addresses:
        tv_node_obj = tv_addresses[tv_btn_id]
        selected_tv=tv_btn_id

        selected_tv_mac=tv_node_obj['mac']
        # tv_node = EthernetClientInterface(tv_node_obj['ip'], int(tv_node_obj['port']), 'TCP')
        id_tv = tv_node_obj['id']
        try:
            print('Trying to connect TV. TV node is:')
            logs_screen.custom_logger('Trying to connect TV. TV node is:')
            print(tv_node)
            logs_screen.custom_logger(tv_node)
            connect_to_tv_node(tv_node_obj['ip'], tv_node_obj['port'])
        except:
            print('Unable to connect TV. Check its power state or just try to wake it up.')
            logs_screen.custom_logger('Unable to connect TV. Check its power state or just try to wake it up.')
        
            
        for btn in LCD_IDS_GRP:
            if btn.ID == tv_btn_id:
                btn.SetState(1)
            else:
                btn.SetState(0)


#TV POWER STATE SET
def tv_power_control(tv_btn_id):
    global tv_addresses
    global selected_tv_mac
    global selected_tv
    if selected_tv != None: 
        if tv_btn_id == 42:
            if selected_tv in tv_addresses:
                l2_address = selected_tv_mac
                WakeOnLan(l2_address, port=9)
        elif tv_btn_id == 97:
            if connect_state == True:
                if selected_tv in tv_addresses:
                    tv_node_obj = tv_addresses[selected_tv]
                    PowerCmdString = 'ka {0} 00\r'.format(tv_node_obj['id'])#ka {0} 00\r
                    __SetHelper(PowerCmdString)
                else:
                    logs_screen.custom_logger('Wrong selected_tv. Not found in tv_addresses.')
                    print('Wrong selected_tv. Not found in tv_addresses.')
            else:
                logs_screen.custom_logger("TV not found. Check connection.")
                logs_screen.custom_logger(tv_node)
                print("TV not found. Check connection.")
                print(tv_node)
                connect()
   

def __SetHelper(commandstring, qualifier=1, queryDisallowTime=0):
    print("command ready to send on TV:")
    print(commandstring)         
    global tv_node
    global connect_state
    # KeypadCmdBytes = commandstring.encode('utf-8')

    if connect_state == False:
        connect()
        try:
            tv_node.Send(commandstring)
            logs_screen.custom_logger('Command send to TV')
            print('Command send to TV')
        except:
            print('Failed to connect TV and error in send command')
            logs_screen.custom_logger('Failed to connect TV and error in send command')
    elif connect_state == True:
        tv_node.Send(commandstring)
        logs_screen.custom_logger('Command send to TV')
        print('Command send to TV')
        # logs_screen.custom_logger('Unable to send command. TV not tv_connected.')
        # print('Unable to send command. TV not tv_connected.')


#set number on pad
def set_keypad(tv_btn_id):
    global connect_state
    global id_tv
    if connect_state == True:
        
        ValueStateValues = {        
            28: { 'key': '11'},
            29: { 'key': '12'},
            30: { 'key': '13'},
            31: { 'key': '14'},
            32: { 'key': '15'},
            33: { 'key': '16'},
            34: { 'key': '17'},
            35: { 'key': '18'},
            36: { 'key': '19'},
            120: { 'key': '10'}
        }
        if tv_btn_id in ValueStateValues:
            value =  ValueStateValues[tv_btn_id]                      
            # print(value)
            KeypadCmdString = 'mc {0} {1}\r'.format(id_tv, value['key'])#mc {0} {1}\r
            __SetHelper(commandstring=KeypadCmdString)
        else:
            logs_screen.custom_logger('Invalid btn ID in keypad')
            print('Invalid btn ID in keypad')
    else:
        print('Unable to connect TV. Check connection first.')
        logs_screen.custom_logger('Unable to connect TV. Check connection first.')


def menu_navigation(tv_btn_id):
    global connect_state
    global id_tv
    if connect_state == True:
        """Set Menu Navigation
        value: Enum
        qualifier: {'Device ID' : Enum}
        """
        
        ValueStateValues = {
            76: {'value': '43'},
            121:  {'value': '28'},
            122: {'value': '5B'},
            38: {'value': '40'},
            37: {'value': '07'},
            40: {'value': '44'},
            39: {'value': '06'},
            41:  {'value': '41'}
        }

        if tv_btn_id in ValueStateValues: 
            logs_screen.custom_logger('ID TV')
            logs_screen.custom_logger(id_tv)
            print('ID TV')
            print(id_tv)
            MenuNavigationCmdString = 'mc {0} {1}\r'.format(int(id_tv), int(ValueStateValues['value']))#mc {0} {1}\r
            __SetHelper(MenuNavigationCmdString)
        else:
            print('Invalid Command') 
            logs_screen.custom_logger('Invalid Command') 

    else:
        logs_screen.custom_logger("TV not found. Check connection.")
        logs_screen.custom_logger(tv_node)
        print("TV not found. Check connection.")
        print(tv_node)
        # connect()




Initialize()