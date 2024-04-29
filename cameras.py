from struct import pack
from extronlib.interface import EthernetClientInterface
from extronlib.device import UIDevice
from extronlib.ui import Button
from extronlib import event
from extronlib.system import Timer, Wait

import socket

from cameras_utils import *
from cameras_const import *
import confhost
import universal_sender
import logs_screen
from universal_sender import *


# cam_node = EthernetClientInterface('10.90.5.51', 5678)
cam_node_udp = None
connected = None  # Stores the last time data/connection

active_cameras = 0  # set from main page in listener. camera btn id
active_preset_number = 0  # set from main page. preset number 1 to 9
active_presets = 0  # set from main page in listener. preset btn id

camera_connect_state = False
# cam_preset_list = False

last_id_first_sector = None
last_id_second_sector = None

cam1_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cam2_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cam3_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# previous_mic_ids = [None, None, None]

camera_nodes = {
    16: {
        "address": "10.90.5.51",
        "port": 1259,
        "protocol": "UDP",
    },  # was 5678 TCP and 1259 UDP
    17: {"address": "10.90.5.52", "port": 1259, "protocol": "UDP"},
    18: {"address": "10.90.5.53", "port": 1259, "protocol": "UDP"},
}


def camera_node_checker(camera_id):
    # global cam_node
    global cam_node_udp
    global camera_nodes

    if camera_id in camera_nodes:
        camera_node = camera_nodes[camera_id]
        if "address" in camera_node:
            cam_node_udp = camera_node
            # cam_node = EthernetClientInterface(camera_node['address'], int(camera_node['port']), camera_node['protocol'])
            # connect()


# ALL CAMERAS BTNS INIT. EVERY GROUP WITH SEPARATE EVENTS IN MAIN
def init_buttons(webgui: UIDevice):
    logs_screen.custom_logger("Initializing Camera buttons")
    print("Initializing Camera buttons")
    CAM_IDS[16] = Button(webgui, 16, holdTime=None, repeatTime=None)  # Cam1 btn
    CAM_IDS[17] = Button(webgui, 17, holdTime=None, repeatTime=None)  # Cam2 btn
    CAM_IDS[18] = Button(webgui, 18, holdTime=None, repeatTime=None)  # Cam3 btn

    CAM_ACTIONS[127] = Button(
        webgui, 127, holdTime=None, repeatTime=None
    )  # Power ON btn
    CAM_ACTIONS[126] = Button(
        webgui, 126, holdTime=None, repeatTime=None
    )  # Power OFF btn
    CAM_ACTIONS[15] = Button(webgui, 15, holdTime=None, repeatTime=None)  # Zoom in btn
    CAM_ACTIONS[102] = Button(
        webgui, 102, holdTime=None, repeatTime=None
    )  # Zoom out btn
    CAM_ACTIONS[108] = Button(webgui, 108, holdTime=None, repeatTime=None)  # Focus btn
    CAM_ACTIONS[103] = Button(webgui, 103, holdTime=None, repeatTime=None)  # UP btn
    CAM_ACTIONS[106] = Button(webgui, 106, holdTime=None, repeatTime=None)  # left btn
    CAM_ACTIONS[107] = Button(webgui, 107, holdTime=None, repeatTime=None)  # right btn
    CAM_ACTIONS[104] = Button(webgui, 104, holdTime=None, repeatTime=None)  # home btn
    CAM_ACTIONS[105] = Button(webgui, 105, holdTime=None, repeatTime=None)  # down btn

    CAM_PRESETS[109] = Button(webgui, 109, holdTime=None, repeatTime=None)  # 1 btn
    CAM_PRESETS[110] = Button(webgui, 110, holdTime=None, repeatTime=None)  # 2 btn
    CAM_PRESETS[111] = Button(webgui, 111, holdTime=None, repeatTime=None)  # 3 btn
    CAM_PRESETS[112] = Button(webgui, 112, holdTime=None, repeatTime=None)  # 4 btn
    CAM_PRESETS[113] = Button(webgui, 113, holdTime=None, repeatTime=None)  # 5 btn
    CAM_PRESETS[114] = Button(webgui, 114, holdTime=None, repeatTime=None)  # 6 btn
    CAM_PRESETS[115] = Button(webgui, 115, holdTime=None, repeatTime=None)  # 7 btn
    CAM_PRESETS[116] = Button(webgui, 116, holdTime=None, repeatTime=None)  # 8 btn
    CAM_PRESETS[117] = Button(webgui, 117, holdTime=None, repeatTime=None)  # 9 btn
    CAM_PRESETS[197] = Button(webgui, 197, holdTime=None, repeatTime=None)  # 8 btn
    CAM_PRESETS[198] = Button(webgui, 198, holdTime=None, repeatTime=None)  # 9 btn

    CAM_PRESETS_ACT[128] = Button(
        webgui, 128, holdTime=None, repeatTime=None
    )  # save preset btn
    CAM_PRESETS_ACT[129] = Button(
        webgui, 129, holdTime=None, repeatTime=None
    )  # show preset btn


# INIT CAMERAS SOCKETS
def socket_init():
    try:
        cam1_socket.connect(("10.90.5.51", 1259))
        cam1_socket.setblocking(False)
        print("Camera 1 socket opened sucessfully.")
        logs_screen.custom_logger("Camera 1 socket opened sucessfully.")
    except:
        print("Error connecting camera 1 socket. Check it out")
        logs_screen.custom_logger("Error connecting camera 1 socket. Check it out")

    try:
        cam2_socket.connect(("10.90.5.52", 1259))
        cam2_socket.setblocking(False)
        print("Camera 2 socket opened sucessfully.")
        logs_screen.custom_logger("Camera 2 socket opened sucessfully.")
    except:
        print("Error connecting camera 2 socket. Check it out")
        logs_screen.custom_logger("Error connecting camera 2 socket. Check it out")

    try:
        cam3_socket.connect(("10.90.5.53", 1259))
        cam3_socket.setblocking(False)
        print("Camera 3 socket opened sucessfully.")
        logs_screen.custom_logger("Camera 3 socket opened sucessfully.")
    except:
        print("Error connecting camera 3 socket. Check it out")
        logs_screen.custom_logger("Error connecting camera 3 socket. Check it out")


# INIT CAMERA BTNS AND GET THEIR DATA
def init_cam_control_group():
    logs_screen.custom_logger("Initializing Cameras control group")
    print("Initializing Cameras control group")
    append_to_cam_ctrl_grp(CAM_IDS.values())
    append_to_act_grp(CAM_ACTIONS.values())
    append_to_pres_grp(CAM_PRESETS.values())
    append_to_cam_presets_act(CAM_PRESETS_ACT.values())


# CHECK IF CAMERA CHOSEN AND BUTTON STATE CHANGED
def camera_state_checker(camera_id):
    global active_cameras
    if camera_id in CAM_IDS:
        set_state(cam_ids_list=True, id_cam_to_skip=camera_id)
    else:
        logs_screen.custom_logger("Wrong preset ID.")
        print("Wrong preset ID.")


# CHECK IF CAMERA PRESET IS CHOSEN AND BUTTON STATE CHANGED
def camera_preset_checker(camera_preset):
    # global cam_preset_list
    global active_presets
    print("Active camera is:")
    logs_screen.custom_logger("Active camera is:")
    print(active_cameras)
    logs_screen.custom_logger(active_cameras)

    if active_cameras != 0:
        if camera_preset in CAM_PRESETS:
            set_state(cam_preset_list=True, id_preset_to_skip=camera_preset)
        else:
            logs_screen.custom_logger("Wrong camera ID.")
            print("Wrong camera ID.")
    else:
        print("Select camera first")
        logs_screen.custom_logger("Select camera first")


# SET ALL CAMS TO 11 PRESET
def camera_set_default_preset():
    global active_presets
    global active_cameras
    global active_preset_number

    for cam in range(16, 19):
        camera_node_checker(cam)
        active_presets = 11
        active_cameras = cam
        active_preset_number = active_presets
        preset_walker(128)
        logs_screen.custom_logger("All cameras go preset 11")


# Cam power control
def cam_power_group(button_id):
    camera_mapping = {
        146: (16, 9),  # power on cam 1
        151: (16, 10),  # power off cam 1
        185: (17, 9),  # power on cam 2
        150: (17, 10),  # power off cam 2
        152: (18, 9),  # power on cam 3
        186: (18, 10),  # power off cam 3
    }

    if button_id in camera_mapping:
        camera_node, action = camera_mapping[button_id]
        camera_node_checker(camera_node)
        cameras_actions(action)


# CAMERAS ACTIONS COMMANDS
def cameras_actions(command):
    int_command = int(command)
    print("Command is")
    logs_screen.custom_logger("Command is")
    print(command)
    logs_screen.custom_logger(command)
    actions = {
        0: b"\x81\x01\x06\x01\x01\x01\x03\x03\xFF",  # STOP
        1: b"\x81\x01\x06\x01\x05\x05\x03\x01\xFF",  # UP
        2: b"\x81\x01\x06\x04\xFF",  # HOME
        3: b"\x81\x01\x06\x01\x05\x05\x03\x02\xFF",  # DOWN
        4: b"\x81\x01\x06\x01\x05\x05\x01\x03\xFF",  # LEFT
        5: b"\x81\x01\x06\x01\x05\x05\x02\x03\xFF",  # RIGHT
        6: b"\x81\x01\x04\x07\x02\xFF",  # ZOOM IN 8x 01 04 07 02 FF
        7: b"\x81\x01\x04\x07\x03\xFF",  # ZOOM OUT 8x 01 04 07 03 FF
        8: b"\x81\x01\x04\x18\x01\xFF",  # FOCUS 8x 01 04 18 01 FF
        9: b"\x81\x01\x04\x00\x02\xFF",  # POWER ON
        10: b"\x81\x01\x04\x00\x03\xFF",  # POWER OFF
        11: b"\x81\x01\x04\x07\x00\xFF",  # STOP ZOOM
    }

    if int_command in actions:
        action = actions[int_command]
        __SetHelper(action, 3)
    else:
        print("Invalid command")
        logs_screen.custom_logger("Invalid command")


# DATA SENDER VIA ETHERNET INTERFACE
def __SetHelper(PowerCmdString, priority_com):
    global cam_node_udp
    priority_com = priority_com
    if cam_node_udp != None:
        socket_sender(
            message=PowerCmdString,
            ip_address=cam_node_udp["address"],
            port=int(cam_node_udp["port"]),
            priority=priority_com,
        )
        logs_screen.custom_logger("Command send to socket_sender")
    else:
        print("Unable to send from camera to socket_sender. Wrond parameters")
        logs_screen.custom_logger(
            "Unable to send from camera to socket_sender. Wrond parameters"
        )


# UDP SENDER
def socket_sender(message, ip_address, port, priority):  # TODO ADD PRIORITY

    if ip_address == "10.90.5.51":
        try:
            cam1_socket_command = Devices_Command(
                cam1_socket, message, int(priority), str(ip_address), int(port)
            )
            send_queue.append(cam1_socket_command)
            send_queue.process()
            logs_screen.custom_logger("Command sent to queue from camera 1")
            print("Command sent to queue from camera 1")
            # cam1_socket.sendto(message, (ip_address, port))
        except Exception as e:
            print("Unable to send data to queue from cam_socket 1.", str(e))
            logs_screen.custom_logger(
                "Unable to send data to queue from cam_socket 1.", str(e)
            )
    elif ip_address == "10.90.5.52":
        try:
            cam2_socket_command = Devices_Command(
                cam2_socket, message, int(priority), str(ip_address), int(port)
            )
            send_queue.append(cam2_socket_command)
            send_queue.process()
            logs_screen.custom_logger("Command sent to queue from camera 2")
            print("Command sent to queue from camera 2")
            # cam2_socket.sendto(message, (ip_address, port))
        except Exception as e:
            print("Unable to send data to queue from cam_socket 2.", str(e))
            logs_screen.custom_logger(
                "Unable to send data to queue from cam_socket 2.", str(e)
            )
    elif ip_address == "10.90.5.53":
        try:
            cam3_socket_command = Devices_Command(
                cam3_socket, message, int(priority), str(ip_address), int(port)
            )
            send_queue.append(cam3_socket_command)
            send_queue.process()
            logs_screen.custom_logger("Command sent to queue from camera 3")
            print("Command sent to queue from camera 3")
            # cam3_socket.sendto(message, (ip_address, port))
        except Exception as e:
            print("Unable to send data to queue from cam_socket 3.", str(e))
            logs_screen.custom_logger(
                "Unable to send data to queue from cam_socket 3.", str(e)
            )
    else:
        print("Wrong ip_address in socket_sender.")
        logs_screen.custom_logger("Wrong ip_address in socket_sender.")


# reset states of camera btns and variables
def reset_cameras_states():
    set_state(cam_preset_list=True, cam_ids_list=True)
    connected = None
    active_cameras = 0  # set from main page in listener. camera btn id
    active_preset_number = 0  # set from main page. preset number 1 to 9
    active_presets = 0

    logs_screen.custom_logger("Chosen cameras have been reset sucessfully.")
    print("Chosen cameras have been reset sucessfully.")


# PRESET ACTIONS
def preset_walker(preset_btn):

    if active_cameras != 0:
        if active_presets != 0:
            if active_preset_number != 0:
                if preset_btn == 128:  # show

                    for cam_pr in CAM_PRESET_GRP:
                        PowerCmdString = (
                            b"\x81\x01\x04\x3F\x02"
                            + bytes([active_preset_number])
                            + b"\xFF"
                        )
                        __SetHelper(PowerCmdString, 2)
                        logs_screen.custom_logger(
                            "Command SHOW PRESET send to socket_sender"
                        )
                        logs_screen.custom_logger(PowerCmdString, 2)
                        # print(PowerCmdString)
                elif preset_btn == 129:  # save
                    for cam_pr in CAM_PRESET_GRP:
                        PowerCmdString = (
                            b"\x81\x01\x04\x3F\x01"
                            + bytes([active_preset_number])
                            + b"\xFF"
                        )
                        __SetHelper(PowerCmdString, 2)
                        # print(PowerCmdString)
                        logs_screen.custom_logger(
                            "Command SAVE PRESET send to socket_sender"
                        )
                        logs_screen.custom_logger(PowerCmdString, 2)
            else:
                logs_screen.custom_logger("Wrong preset ID")
                print("Wrong preset ID")
        else:
            logs_screen.custom_logger("Not selected preset")
            print("Not selected preset")
    else:
        logs_screen.custom_logger("Active camera not selected")
        print("Active camera not selected")
