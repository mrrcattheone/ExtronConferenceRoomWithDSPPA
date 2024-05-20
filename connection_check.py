from extronlib.device import UIDevice
from extronlib.ui import Button
from extronlib.system import Ping
from extronlib.ui import Button, Knob, Label, Level
import time

from connection_check_const import *
from connection_check_utils import *
import logs_screen


WebGUI = UIDevice("WebGUI")  # WEbUI alias name

label_ping_show = Label(WebGUI, 131)
state_control_label = Label(WebGUI, 330)


# ALL CAMERAS BTNS INIT. EVERY GROUP WITH SEPARATE EVENTS IN MAIN
def init_buttons(webgui: UIDevice):
    logs_screen.custom_logger("Initializing Connection Check buttons")
    print("Initializing Connection Check buttons")
    CONNECTION_HOST[187] = {
        "btn_obj": Button(webgui, 187, holdTime=None, repeatTime=None),
        "address": "10.90.5.61",
    }  # TV1 btn
    CONNECTION_HOST[188] = {
        "btn_obj": Button(webgui, 188, holdTime=None, repeatTime=None),
        "address": "10.90.5.62",
    }  # TV2 btn
    CONNECTION_HOST[196] = {
        "btn_obj": Button(webgui, 196, holdTime=None, repeatTime=None),
        "address": "10.90.5.63",
    }  # TV3 btn
    CONNECTION_HOST[208] = {
        "btn_obj": Button(webgui, 208, holdTime=None, repeatTime=None),
        "address": "10.90.5.64",
    }  # TV4 btn
    CONNECTION_HOST[285] = {
        "btn_obj": Button(webgui, 285, holdTime=None, repeatTime=None),
        "address": "10.90.5.65",
    }  # TV5 btn
    CONNECTION_HOST[286] = {
        "btn_obj": Button(webgui, 286, holdTime=None, repeatTime=None),
        "address": "10.90.5.66",
    }  # TV6 btn
    CONNECTION_HOST[287] = {
        "btn_obj": Button(webgui, 287, holdTime=None, repeatTime=None),
        "address": "10.90.5.67",
    }  # TV7 btn
    CONNECTION_HOST[288] = {
        "btn_obj": Button(webgui, 288, holdTime=None, repeatTime=None),
        "address": "10.90.5.68",
    }  # TV8 btn
    CONNECTION_HOST[289] = {
        "btn_obj": Button(webgui, 289, holdTime=None, repeatTime=None),
        "address": "10.90.5.69",
    }  # TV9 btn
    CONNECTION_HOST[290] = {
        "btn_obj": Button(webgui, 290, holdTime=None, repeatTime=None),
        "address": "10.90.5.51",
    }  # Cam1 btn
    CONNECTION_HOST[291] = {
        "btn_obj": Button(webgui, 291, holdTime=None, repeatTime=None),
        "address": "10.90.5.52",
    }  # Cam2 btn
    CONNECTION_HOST[292] = {
        "btn_obj": Button(webgui, 292, holdTime=None, repeatTime=None),
        "address": "10.90.5.53",
    }  # Cam3 btn
    CONNECTION_HOST[301] = {
        "btn_obj": Button(webgui, 301, holdTime=None, repeatTime=None),
        "address": "",
    }  # videowall btn
    CONNECTION_HOST[302] = {
        "btn_obj": Button(webgui, 302, holdTime=None, repeatTime=None),
        "address": "",
    }  # delegates btn
    CONNECTION_HOST[303] = {
        "btn_obj": Button(webgui, 303, holdTime=None, repeatTime=None),
        "address": "",
    }  # speaker btn
    CONNECTION_HOST[304] = {
        "btn_obj": Button(webgui, 304, holdTime=None, repeatTime=None),
        "address": "",
    }  # pc out btn
    CONNECTION_HOST[305] = {
        "btn_obj": Button(webgui, 305, holdTime=None, repeatTime=None),
        "address": "",
    }  # operator btn
    CONNECTION_HOST[298] = {
        "btn_obj": Button(webgui, 298, holdTime=None, repeatTime=None),
        "address": "",
    }  # pc1 btn
    CONNECTION_HOST[299] = {
        "btn_obj": Button(webgui, 299, holdTime=None, repeatTime=None),
        "address": "",
    }  # pc2 btn
    CONNECTION_HOST[300] = {
        "btn_obj": Button(webgui, 300, holdTime=None, repeatTime=None),
        "address": "",
    }  # pc3 btn
    CONNECTION_HOST[308] = {
        "btn_obj": Button(webgui, 308, holdTime=None, repeatTime=None),
        "address": "",
    }  # server schneider btn


# INIT CAMERA BTNS AND GET THEIR DATA
def init_netcheck_control_group():
    logs_screen.custom_logger("Initializing Connection Check control group")
    print("Initializing Connection Check control group")
    append_to_net_ctrl_grp(*[btn["btn_obj"] for btn in CONNECTION_HOST.values()])


# check connection
def connection_checker(clicked_netcheck_btn):
    logs_screen.custom_logger("Checking connection")
    if clicked_netcheck_btn in CONNECTION_HOST:
        state_labels_text_show("Проверка соединения...")
        net_host = CONNECTION_HOST[clicked_netcheck_btn]
        result = Ping(net_host["address"])
        print(
            "Успешно: {}, Потеряно: {}, Среднее время: {:.2f}".format(
                result[0], result[1], result[2]
            )
        )
        logs_screen.custom_logger(
            "Успешно: {}, Потеряно: {}, Среднее время: {:.2f}".format(
                result[0], result[1], result[2]
            )
        )
        label_ping_show.SetText(
            "Успешно: {}, Потеряно: {}, Среднее время: {:.2f}".format(
                result[0], result[1], result[2]
            )
        )
        state_labels_text_hide()


def state_labels_text_show(text, duration=1):
    state_control_label.SetText(text)
    state_control_label.SetVisible(True)


def state_labels_text_hide():
    state_control_label.SetVisible(False)
