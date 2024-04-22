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


ic2_outputs = {
    80 : {'ip': '10.90.5.42', 'port': 41234, 'height':'1920', 'width':'1080', 'type':'udp://'}, #display delegat
    81 : {'ip': '10.90.5.43', 'port': 41234, 'height':'1920', 'width':'1080', 'type':'udp://'}, #splitter hdmi
    82 : {'ip': '10.90.5.44', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'udp://'}, #videowall
    83 : {'ip': '10.90.5.45', 'port': 41234, 'height':'1920', 'width':'1080', 'type':'udp://'}, #display operator
    84 : {'ip': '10.90.5.46', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'udp://'}, #msp
}

ic2_inputs = {
    1 : {'ip': '10.90.5.31', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'udp://'}, #sharelink
    2 : {'ip': '10.90.5.32', 'port': 41234, 'height':'1920', 'width':'1080', 'type':':udp//'}, #pcin dvi fullhd
    3 : {'ip': '10.90.5.33', 'port': 41234, 'height':'3840', 'width':'2160', 'type':':udp//'}, #pcin hdmi 4k
    4 : {'ip': '10.90.5.35', 'port': 41234, 'height':'1920', 'width':'1080', 'type':'udp://'}, #pcin dp fullhd
    5 : {'ip': '10.90.5.51', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'rtsp://'}, #cam1
    6 : {'ip': '10.90.5.52', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'rtsp://'}, #cam2
    7 : {'ip': '10.90.5.53', 'port': 41234, 'height':'3840', 'width':'2160', 'type':'rtsp://'} #cam3
}



connected = None    # Stores the last time data/connection
socket_msp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


ic2_node=EthernetClientInterface('10.90.5.42', 41234, 'UDP')
ic2_node.SetBufferSize(2048)

def stream_node_checker(ic_2):
    global ic2_node

    if ic_2 in ic2_outputs:
        ic_2_node = ic2_outputs[ic_2]
        if 'ip' in ic_2_node:
            ic2_node = EthernetClientInterface(Hostname=ic_2_node['ip'], IPPort=int(ic_2_node['port']))
            # connect()


#UDP SENDER
def socket_sender(message, ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto(message.encode('utf-8'), (ip_address, port))
    ic2_node_command = Devices_Command(sock, message.encode('utf-8'), 3, ip_address, port)
    send_queue.append(ic2_node_command)
    send_queue.process()

    logs_screen.custom_logger('Command sent to queue from camera 1')
    print('Command sent to queue from camera 1')
    logs_screen.custom_logger('Command send to IC2')
    print('Command send to IC2')
    sock.close()

#QUICK CONFERENCE MODE
def quick_preset_launcher(conference_mode):
    if conference_mode == 'local':
        command_list = {
            1:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.33-0,udp://224.168.5.33:35252,0,0,3840,2160}"},
            2:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
            3:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
            4:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.33-0,udp://224.168.5.33:35253,0,0,960,540; 10.90.5.35-0,udp://224.168.5.35:35260,960,0,960,540; 10.90.5.31-0,udp://224.168.5.31:35245,480,540,960,540}"}
        }
        for command_id, command_data in command_list.items():
            address = command_data['address']
            port = int(command_data['port'])
            command = command_data['command']
            
            socket_sender(command, address, port)
    elif conference_mode == 'video':
        command_list = {
            1:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.52-0,rtsp://10.90.5.52,0,0,3840,2160;10.90.5.51-1,rtsp://10.90.5.51,0,0,1440,810;10.90.5.53-0,rtsp://10.90.5.53,2400,0,1440,810}"},
            2:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.33-0,udp://224.168.5.33:35252,0,0,3840,2160}"},
            3:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
            4:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
            5:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.33-0,udp://224.168.5.33:35253,0,0,960,540; 10.90.5.35-0,udp://224.168.5.35:35260,960,0,960,540; 10.90.5.31-0,udp://224.168.5.31:35245,480,540,960,540}"}
        }
        for command_id, command_data in command_list.items():
            address = command_data['address']
            port = int(command_data['port'])
            command = command_data['command']
            
            socket_sender(command, address, port)

        
#PRIORITY MODE FOR VIDEOCONFERENCE
def videoconference_with_priority(priority_camera_number):
    global socket_msp
    cam_ic_list = {
        2:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.51-0,rtsp://10.90.5.51,0,0,3840,2160;10.90.5.52-1,rtsp://10.90.5.52,0,0,1440,810;10.90.5.53-0,rtsp://10.90.5.53,2400,0,1440,810}"},
        0:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.52-0,rtsp://10.90.5.52,0,0,3840,2160;10.90.5.51-1,rtsp://10.90.5.51,0,0,1440,810;10.90.5.53-0,rtsp://10.90.5.53,2400,0,1440,810}"},
        1:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.53-0,rtsp://10.90.5.53,0,0,3840,2160;10.90.5.51-1,rtsp://10.90.5.51,0,0,1440,810;10.90.5.52-0,rtsp://10.90.5.52,2400,0,1440,810}"},
    }
    
    if priority_camera_number in cam_ic_list:
       
        selected_command = cam_ic_list[priority_camera_number]
        address = selected_command['address']
        port = int(selected_command['port'])
        command = selected_command['command']
        try:
            socket_msp.sendto(command.encode('utf-8'), (address, port))
            print('Main camera changed')
            logs_screen.custom_logger('Main camera changed')
        except:
            print('Unable to send command to IC2. Check connection')
            logs_screen.custom_logger('Unable to send command to IC2. Check connection')
    else:
        print('Wrong parameter in videoconference_with_priority variable')
        logs_screen.custom_logger('Wrong parameter in videoconference_with_priority variable')


#ic expert mode ic2 view launcher
def expert_mode_launcher(btn_id):
    

    command_list = {
        #wall
        243:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.32-0,udp://224.168.5.32:35248,0,0,3840,2160}"},
        249:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.33-0,udp://224.168.5.33:35252,0,0,3840,2160}"},
        250:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.35-0,udp://224.168.5.35:35260,0,0,3840,2160}"},
        251:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.31-0,udp://224.168.5.31:35244,0,0,3840,2160}"},
        252:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.51-0,rtsp://10.90.5.51,0,0,3840,2160}"},
        265:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.52-0,rtsp://10.90.5.52,0,0,3840,2160}"},
        274:{'address':'10.90.5.44', 'port':'41234', 'command': "{SetWindows;600004;10.90.5.53-0,rtsp://10.90.5.53,0,0,3840,2160}"},
        #table
        254:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.32-0,udp://224.168.5.32:35248,0,0,1920,1080}"},
        263:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
        264:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.35-0,udp://224.168.5.35:35260,0,0,1920,1080}"},
        266:{'address':'10.90.5.43', 'port':'41234', 'command': "{SetWindows;600003;10.90.5.31-0,udp://224.168.5.31:35245,0,0,1920,1080}"},
        #speaker
        256:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.32-0,udp://224.168.5.32:35248,0,0,1920,1080}"},
        257:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
        258:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.35-0,udp://224.168.5.35:35260,0,0,1920,1080}"},
        259:{'address':'10.90.5.42', 'port':'41234', 'command': "{SetWindows;600002;10.90.5.31-0,udp://224.168.5.31:35245,0,0,1920,1080}"},
        #operator
        260:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.32-0,udp://224.168.5.32:35248,0,0,1920,1080}"},
        262:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.33-0,udp://224.168.5.33:35253,0,0,1920,1080}"},
        267:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.35-0,udp://224.168.5.35:35260,0,0,1920,1080}"},
        268:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.31-0,udp://224.168.5.31:35245,0,0,1920,1080}"},
        278:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.52-0,rtsp://10.90.5.52/2,480,0,960,540;10.90.5.51-0,rtsp://10.90.5.51/2,0,540,960,540;10.90.5.53-0,rtsp://10.90.5.53/2,960,540,960,540}"},
        275:{'address':'10.90.5.45', 'port':'41234', 'command': "{SetWindows;600005;10.90.5.33-0,udp://224.168.5.33:35253,0,0,960,540; 10.90.5.35-0,udp://224.168.5.35:35260,960,0,960,540; 10.90.5.31-0,udp://224.168.5.31:35245,480,540,960,540}"},
        #cam
        272:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.52-0,rtsp://10.90.5.52,0,0,3840,2160;10.90.5.51-1,rtsp://10.90.5.51,0,0,1440,810;10.90.5.53-0,rtsp://10.90.5.53,2400,0,1440,810}"},
        277:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.51-0,rtsp://10.90.5.51,0,0,3840,2160;10.90.5.52-1,rtsp://10.90.5.52,0,0,1440,810;10.90.5.53-0,rtsp://10.90.5.53,2400,0,1440,810}"},
        273:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.53-0,rtsp://10.90.5.53,0,0,3840,2160;10.90.5.51-1,rtsp://10.90.5.51,0,0,1440,810;10.90.5.52-0,rtsp://10.90.5.52,2400,0,1440,810}"},
        276:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.52-0,rtsp://10.90.5.52,0,1620,960,540;10.90.5.53-0,rtsp://10.90.5.53,2880,1620,960,540;10.90.5.31-0,udp://224.168.5.31:35244,0,0,3840,2160}"},
        777:{'address':'10.90.5.46', 'port':'41234', 'command': "{SetWindows;600006;10.90.5.31-0,udp://224.168.5.31:35245,0,0,3840,2160}"}
    }
    if btn_id in command_list:
        selected_command = command_list[btn_id]
        address = selected_command['address']
        port = int(selected_command['port'])
        command = selected_command['command']
        
        socket_sender(command, address, port)

#run special ic2 mode in conference
def videoconference_presentation_source(source_btn):
    if source_btn == 180: #PC out
        #258 264
        expert_mode_launcher(258)
        expert_mode_launcher(264)
    elif source_btn == 181:#presentor to cam
        #259 266 777
        expert_mode_launcher(259)
        expert_mode_launcher(266)
        expert_mode_launcher(777)
    elif source_btn == 213: #finish presentation
        #263 257 272
        expert_mode_launcher(263)
        expert_mode_launcher(257)
        expert_mode_launcher(272)
        expert_mode_launcher(249)
    elif source_btn == 210: #presentor to all
        #251 266 259
        expert_mode_launcher(251)
        expert_mode_launcher(266)
        expert_mode_launcher(259)
    elif source_btn == 326: #pc to all
        #251 266 259
        expert_mode_launcher(249)
        expert_mode_launcher(257)
        expert_mode_launcher(263)
    else:
        print('Wrong argument in videoconference_presentation_source')
