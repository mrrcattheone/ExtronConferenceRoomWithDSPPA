from struct import pack
from extronlib.interface import SerialInterface, EthernetClientInterface
from extronlib.device import UIDevice, ProcessorDevice
from extronlib.ui import Button, Label
from extronlib import event

from confhost_const import *
from confhost_utils import *
import autotracking
import logs_screen
from universal_sender import *

mic_id = ""
mic_state = ""
MIC_BTNS_GRP = None  # TODO move to const
clicked_mic_id = 0
all_mic_disabled = False
automode = False

ProProcessor = ProcessorDevice("ProXI")
MicControl = SerialInterface(
    ProProcessor,
    "COM2",
    Baud=9600,
    Data=8,
    Parity="None",
    Stop=1,
    CharDelay=0,
    Mode="RS232",
)

WebGUI = UIDevice("WebGUI")  # WEbUI alias name

mic_state_label = Label(WebGUI, 331)


def init_buttons(webgui: UIDevice):
    print("Initializing Conference Host buttons")
    logs_screen.custom_logger("Initializing Conference Host buttons")

    MIC_BTNS[56] = {
        "btn_obj": Button(webgui, 56, holdTime=None, repeatTime=None),
        "btn_id": 1,
    }
    MIC_BTNS[57] = {
        "btn_obj": Button(webgui, 57, holdTime=None, repeatTime=None),
        "btn_id": 2,
    }
    MIC_BTNS[58] = {
        "btn_obj": Button(webgui, 58, holdTime=None, repeatTime=None),
        "btn_id": 3,
    }
    MIC_BTNS[59] = {
        "btn_obj": Button(webgui, 59, holdTime=None, repeatTime=None),
        "btn_id": 4,
    }
    MIC_BTNS[60] = {
        "btn_obj": Button(webgui, 60, holdTime=None, repeatTime=None),
        "btn_id": 5,
    }
    MIC_BTNS[61] = {
        "btn_obj": Button(webgui, 61, holdTime=None, repeatTime=None),
        "btn_id": 6,
    }
    MIC_BTNS[62] = {
        "btn_obj": Button(webgui, 62, holdTime=None, repeatTime=None),
        "btn_id": 7,
    }
    MIC_BTNS[63] = {
        "btn_obj": Button(webgui, 63, holdTime=None, repeatTime=None),
        "btn_id": 8,
    }
    MIC_BTNS[64] = {
        "btn_obj": Button(webgui, 64, holdTime=None, repeatTime=None),
        "btn_id": 9,
    }
    MIC_BTNS[65] = {
        "btn_obj": Button(webgui, 65, holdTime=None, repeatTime=None),
        "btn_id": 10,
    }
    MIC_BTNS[73] = {
        "btn_obj": Button(webgui, 73, holdTime=None, repeatTime=None),
        "btn_id": 11,
    }
    MIC_BTNS[72] = {
        "btn_obj": Button(webgui, 72, holdTime=None, repeatTime=None),
        "btn_id": 12,
    }
    MIC_BTNS[71] = {
        "btn_obj": Button(webgui, 71, holdTime=None, repeatTime=None),
        "btn_id": 13,
    }
    MIC_BTNS[70] = {
        "btn_obj": Button(webgui, 70, holdTime=None, repeatTime=None),
        "btn_id": 14,
    }
    MIC_BTNS[69] = {
        "btn_obj": Button(webgui, 69, holdTime=None, repeatTime=None),
        "btn_id": 15,
    }
    MIC_BTNS[68] = {
        "btn_obj": Button(webgui, 68, holdTime=None, repeatTime=None),
        "btn_id": 16,
    }
    MIC_BTNS[67] = {
        "btn_obj": Button(webgui, 67, holdTime=None, repeatTime=None),
        "btn_id": 17,
    }
    MIC_BTNS[66] = {
        "btn_obj": Button(webgui, 66, holdTime=None, repeatTime=None),
        "btn_id": 18,
    }
    MIC_BTNS[78] = {
        "btn_obj": Button(webgui, 78, holdTime=None, repeatTime=None),
        "btn_id": 19,
    }
    MIC_BTNS[77] = {
        "btn_obj": Button(webgui, 77, holdTime=None, repeatTime=None),
        "btn_id": 20,
    }


def init_mic_btn_group():
    global MIC_BTNS_GRP
    MIC_BTNS_GRP = [btn["btn_obj"] for btn in MIC_BTNS.values()]


# INCOMING DATA RS232
@event(MicControl, "ReceiveData")
def MainFeedbackHandler(interface, rcvString):
    # global automode
    print("RS232 string message received")
    logs_screen.custom_logger("RS232 string message received")
    print(rcvString)
    logs_screen.custom_logger(rcvString)
    mic_state_checker(rcvString)


def mic_state_checker(rcvString):  # parse string for mic id
    global mic_id
    global mic_state
    global all_mic_disabled
    global automode

    if len(rcvString) >= 6:
        mic_id = rcvString[6]
        logs_screen.custom_logger("mic ID is:")
        logs_screen.custom_logger(mic_id)
        print("mic ID is:")
        print(mic_id)
        mic_state = rcvString[4]
        logs_screen.custom_logger("mic state is:")
        logs_screen.custom_logger(mic_state)
        print("mic state is:")
        print(mic_state)  # 2 on, 1 off
        if len(rcvString) >= 8 and rcvString[7] is not None:
            all_mic_disabled = True
            logs_screen.custom_logger("last mic was disabled = True")
            print("last mic was disabled = True")
        mic_power_state(mic_id, mic_state)
        if automode == True:
            autotracking.autotrack(mic_id, mic_state)
    else:
        logs_screen.custom_logger(
            "Invalid rcvString length. Waiting for valid command."
        )
        print("Invalid rcvString length. Waiting for valid command.")


# Set default state to mic btns in manual mode
def set_default_btn_states():
    for btn in MIC_BTNS_GRP:
        btn.SetState(1)
    logs_screen.custom_logger("Mic btn`s state was set to 1")
    print("Mic btn`s state was set to 1")


# set state on/off
def mic_power_state(id_mic, state_mic):
    global all_mic_disabled
    # test_btn = int(id_mic)

    for btn_id, btn_info in MIC_BTNS.items():
        if btn_info["btn_id"] == int(id_mic):
            for btn in MIC_BTNS_GRP:
                if btn.ID == btn_id:
                    if state_mic == 2:
                        btn.SetState(0)
                        print("set state ON")
                        logs_screen.custom_logger("set state ON")
                        all_mic_disabled = False
                    elif state_mic == 1:
                        btn.SetState(1)
                        logs_screen.custom_logger("set state OFF")
                        print("set state OFF")
                    elif state_mic == 0:
                        print("Mic btn set state ON, but mic is already ON")
                        logs_screen.custom_logger(
                            "Mic btn set state ON, but mic is already ON"
                        )
                        all_mic_disabled = False


def __SetHelper(commandstring, priority):
    mic_control_command = Devices_Command(MicControl, commandstring, priority)
    send_queue.append(mic_control_command)
    send_queue.process()


def mic_labels_text_show(text, duration=1):
    mic_state_label.SetText(text)
    mic_state_label.SetVisible(True)


def mic_labels_text_hide():
    mic_state_label.SetVisible(False)


def set_mic_power(btn_id, priority=3):
    global clicked_mic_id
    if btn_id in MIC_BTNS.keys():
        clicked_mic_id = MIC_BTNS[btn_id]["btn_id"]
        for btn in MIC_BTNS_GRP:
            if btn.ID == btn_id:
                if btn.State == 1:
                    PowerCmdString = b"\xfb\xfd\x81\x03\x02\x00" + bytes(
                        [clicked_mic_id]
                    )
                    __SetHelper(PowerCmdString, priority)
                    logs_screen.custom_logger("Mic state changed to 0")
                    logs_screen.custom_logger(PowerCmdString)
                    print(PowerCmdString)
                elif btn.State == 0:
                    PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes(
                        [clicked_mic_id]
                    )
                    __SetHelper(PowerCmdString, priority)
                    logs_screen.custom_logger("Mic state changed to 1")
                    logs_screen.custom_logger(PowerCmdString)
                    print(PowerCmdString)
    else:
        logs_screen.custom_logger("Not found btn id in list")
        print("Not found btn id in list")
