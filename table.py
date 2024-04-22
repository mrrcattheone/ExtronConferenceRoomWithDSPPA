from struct import pack
from extronlib.interface import SerialInterface, EthernetClientInterface
from extronlib.device import UIDevice, ProcessorDevice
from extronlib.ui import Button

from table_const import * 
from universal_sender import *

import logs_screen


ProProcessor = ProcessorDevice('ProXI')
lcd_table_lift = SerialInterface(ProProcessor, 'COM1', Baud=9600, Data=8, Parity='None', Stop=1, CharDelay=0, Mode='RS485')


def init_buttons(webgui: UIDevice):
    print("Initializing table's lcd control buttons")
    logs_screen.custom_logger("Initializing table's lcd control buttons")
    PULL_UP_BTNS[201] = Button(webgui, 201, holdTime=None, repeatTime=None)
    PULL_UP_BTNS[139] = Button(webgui, 139, holdTime=None, repeatTime=None)
    PULL_UP_BTNS[54] = Button(webgui, 54, holdTime=None, repeatTime=None)
    PULL_UP_BTNS[214] = Button(webgui, 214, holdTime=None, repeatTime=None)
    PULL_UP_BTNS[235] = Button(webgui, 235, holdTime=None, repeatTime=None)

    PULL_DOWN_BTNS[202] = Button(webgui, 202, holdTime=None, repeatTime=None)
    PULL_DOWN_BTNS[140] = Button(webgui, 140, holdTime=None, repeatTime=None)
    PULL_DOWN_BTNS[55] = Button(webgui, 55, holdTime=None, repeatTime=None)
    PULL_DOWN_BTNS[215] = Button(webgui, 215, holdTime=None, repeatTime=None)
    PULL_DOWN_BTNS[236] = Button(webgui, 236, holdTime=None, repeatTime=None)



def append_to_liftup_ctrl_grp(btns):
    for btn in btns:
        PULL_UP_BTN_GRP.append(btn)


def append_to_liftdown_ctrl_grp(btns):
    for btn in btns:
        PULL_DOWN_BTN_GRP.append(btn)


def init_table_lcd_control_group():
    logs_screen.custom_logger("Initializing TABLE control group")
    print("Initializing TABLE control group")
    append_to_liftup_ctrl_grp(PULL_UP_BTNS.values())
    append_to_liftdown_ctrl_grp(PULL_DOWN_BTNS.values())
        
       

def pull_up(): #PULL UP LCD'S ON TABLE
    PowerCmdString = b'\xF0\xF1\x00\xFF\xFF\x50\x04\xFF\xFF\x03\x01\x35'
    __SetHelper(PowerCmdString) 


def pull_down(): #PULL DOWN LCD'S ON TABLE
    PowerCmdString = b'\xF0\xF1\x00\xFF\xFF\x50\x04\xFF\xFF\x03\x02\x36'
    __SetHelper(PowerCmdString) 


def __SetHelper(commandstring):
    try:    
        lcd_table_lift_command = Devices_Command(lcd_table_lift, commandstring, 3)
        send_queue.append(lcd_table_lift_command)
        send_queue.process()
        # lcd_table_lift.Send(data=commandstring)
        logs_screen.custom_logger('COM1 command sucessfully sent')
        print('COM1 command sucessfully sent')
    except:
        logs_screen.custom_logger('COM1 command not sent')
        print('COM1 command not sent')


