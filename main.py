## CONTROL SCRIPT IMPORT -------------------------------------------------------
# import re
# from extronlib.system import GetSystemUpTime, Ping, ProgramLog, WakeOnLan
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
# from extronlib.interface import (ContactInterface, DigitalIOInterface, \
#     EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
#     IRInterface, RelayInterface, SerialInterface)
from extronlib.interface import SerialInterface
from extronlib.ui import Button, Knob, Label, Level
# from extronlib.system import Clock, MESet, Wait

import confhost 
import stream
import stream_const
import lcd
import lcd_const
import cameras
import cameras_const
import table
import ic2
import main_utils
import schneider_light
import autotracking
import logs_screen
import connection_check
from universal_sender import *

## MODULE INSTANCE -------------------------------------------------------------
ProProcessor = ProcessorDevice('ProXI')
MicControlInput = SerialInterface(ProProcessor, 'COM2', Baud=9600, Data=8, Parity='None', Stop=1, CharDelay=0, Mode='RS232')

## USER INTERFACE DEFINITION ---------------------------------------------------
WebGUI = UIDevice('WebGUI')#WEbUI alias name
## global variables DEFINITION ---------------------------------------------------
automode = False
conference_type = None

#BTN INIT
#PageMain
BtnImageSettings     = Button(WebGUI, 1, holdTime=None, repeatTime=None)
BtnTVSettings    = Button(WebGUI, 3, holdTime=None, repeatTime=None)
BtnCamControlSettings    = Button(WebGUI, 4, holdTime=None, repeatTime=None)
BtnMicControlSettings    = Button(WebGUI, 5, holdTime=None, repeatTime=None)
PowerControlSettings    = Button(WebGUI, 13, holdTime=None, repeatTime=None)
BtnSimpleConferenceModMenu = Button(WebGUI, 183, holdTime=None, repeatTime=None)
BtnSimpleConferenceModMenu2 = Button(WebGUI, 184, holdTime=None, repeatTime=None)
BtnExpertMode = Button(WebGUI, 174, holdTime=None, repeatTime=None)
logs_screen_btn = Button(WebGUI, 189, holdTime=None, repeatTime=None)
connection_page_btn = Button(WebGUI, 194, holdTime=None, repeatTime=None)


#Page Check Connections
back_from_conn_page_btn = Button(WebGUI, 133, holdTime=None, repeatTime=None)

#PageLogsToText
back_to_main_btn = Button(WebGUI, 134, holdTime=None, repeatTime=None)
restart_system_btn = Button(WebGUI, 195, holdTime=None, repeatTime=None)


#PageMicContol
BtnMainMenuMicControl    = Button(WebGUI, 9, holdTime=None, repeatTime=None)
manual_automode_btn = Button(WebGUI, 75, holdTime=None, repeatTime=None)

priority_launcher1    = Button(WebGUI, 135, holdTime=None, repeatTime=None)
priority_launcher2 = Button(WebGUI, 212, holdTime=None, repeatTime=None)

#PagePowerOn
BtnMainMenuPowerOn     = Button(WebGUI, 2, holdTime=None, repeatTime=None)  
light_1_power_on =  Button(WebGUI, 191, holdTime=None, repeatTime=None)  
light_1_power_off =  Button(WebGUI, 190, holdTime=None, repeatTime=None)  
light_2_power_on =  Button(WebGUI, 192, holdTime=None, repeatTime=None)  
light_2_power_off =  Button(WebGUI, 193, holdTime=None, repeatTime=None)  

cam1powerOn = Button(WebGUI, 146, holdTime=None, repeatTime=None)  
cam1powerOff = Button(WebGUI, 150, holdTime=None, repeatTime=None)  
cam2powerOn = Button(WebGUI, 151, holdTime=None, repeatTime=None)  
cam2powerOff = Button(WebGUI, 152, holdTime=None, repeatTime=None)  
cam3powerOn = Button(WebGUI, 185, holdTime=None, repeatTime=None)  
cam3powerOff = Button(WebGUI, 186, holdTime=None, repeatTime=None)  

video_wall_power_down_btn = Button(WebGUI, 145, holdTime=None, repeatTime=None)  
video_wall_power_up_btn = Button(WebGUI, 144, holdTime=None, repeatTime=None)  


video_out1_btn = Button(WebGUI, 180, holdTime=None, repeatTime=None)  
video_out2_btn = Button(WebGUI, 181, holdTime=None, repeatTime=None)  
video_out3_btn = Button(WebGUI, 213, holdTime=None, repeatTime=None)  
video_out_loc1_btn = Button(WebGUI, 210, holdTime=None, repeatTime=None)  
video_out_loc2_btn = Button(WebGUI, 326, holdTime=None, repeatTime=None)  




# #Page LCD Contol
BtnMainMenuTVControl     = Button(WebGUI, 12, holdTime=None, repeatTime=None)


#PageCamControl
BtnMainMenuCamControl    = Button(WebGUI, 7, holdTime=None, repeatTime=None)

#PageImageControl
videoWallBtn1 = Button(WebGUI, 243, holdTime=None, repeatTime=None)
videoWallBtn2 = Button(WebGUI, 249, holdTime=None, repeatTime=None)
videoWallBtn3 = Button(WebGUI, 250, holdTime=None, repeatTime=None)
videoWallBtn4 = Button(WebGUI, 251, holdTime=None, repeatTime=None)
videoWallBtn5 = Button(WebGUI, 252, holdTime=None, repeatTime=None)
videoWallBtn6 = Button(WebGUI, 265, holdTime=None, repeatTime=None)
videoWallBtn7 = Button(WebGUI, 274, holdTime=None, repeatTime=None)

tableSplitterVideoBtn1 = Button(WebGUI, 254, holdTime=None, repeatTime=None)
tableSplitterVideoBtn2 = Button(WebGUI, 263, holdTime=None, repeatTime=None)
tableSplitterVideoBtn3 = Button(WebGUI, 264, holdTime=None, repeatTime=None)
tableSplitterVideoBtn4 = Button(WebGUI, 266, holdTime=None, repeatTime=None)

speakerVideoBtn1 = Button(WebGUI, 256, holdTime=None, repeatTime=None)
speakerVideoBtn2 = Button(WebGUI, 257, holdTime=None, repeatTime=None)
speakerVideoBtn3 = Button(WebGUI, 258, holdTime=None, repeatTime=None)
speakerVideoBtn4 = Button(WebGUI, 259, holdTime=None, repeatTime=None)

operatorVideoBtn1 = Button(WebGUI, 260, holdTime=None, repeatTime=None)
operatorVideoBtn2 = Button(WebGUI, 262, holdTime=None, repeatTime=None)
operatorVideoBtn3 = Button(WebGUI, 267, holdTime=None, repeatTime=None)
operatorVideoBtn4 = Button(WebGUI, 268, holdTime=None, repeatTime=None)
operatorVideoBtn5 = Button(WebGUI, 278, holdTime=None, repeatTime=None)
operatorVideoBtn6 = Button(WebGUI, 275, holdTime=None, repeatTime=None)

camVideoBtn1 = Button(WebGUI, 272, holdTime=None, repeatTime=None)
camVideoBtn2 = Button(WebGUI, 276, holdTime=None, repeatTime=None)
camVideoBtn3 = Button(WebGUI, 273, holdTime=None, repeatTime=None)
camVideoBtn4 = Button(WebGUI, 277, holdTime=None, repeatTime=None)


BtnMainMenuImageControl = Button(WebGUI, 8, holdTime=None, repeatTime=None)
BtnMainMenuImage_1Control = Button(WebGUI, 270, holdTime=None, repeatTime=None)

#PageModeSelection
localPresentationModeBtn = Button(WebGUI, 179, holdTime=None, repeatTime=None) 
videoConferenceModeBtn = Button(WebGUI, 153, holdTime=None, repeatTime=None)

begin_conference_btn = Button(WebGUI, 11, holdTime=None, repeatTime=None)  
terminate_conference_btn = Button(WebGUI, 207, holdTime=None, repeatTime=None)  

mic_off_conference_1 = Button(WebGUI, 203, holdTime=None, repeatTime=None)  
mic_off_conference_2 = Button(WebGUI, 231, holdTime=None, repeatTime=None)  
mic_off_conference_3 = Button(WebGUI, 178, holdTime=None, repeatTime=None)  
mic_off_conference_without_leader = Button(WebGUI, 237, holdTime=None, repeatTime=None)  

backFromModeBtn = Button(WebGUI, 149, holdTime=None, repeatTime=None)  

finishLocalConference = Button(WebGUI, 224, holdTime=None, repeatTime=None)  
finishVideoConference = Button(WebGUI, 245, holdTime=None, repeatTime=None)  

tv_off_total_1 = Button(WebGUI, 200, holdTime=None, repeatTime=None)  
tv_on_total_1 = Button(WebGUI, 199, holdTime=None, repeatTime=None)  

tv_off_total_2 = Button(WebGUI, 233, holdTime=None, repeatTime=None)  
tv_on_total_2 = Button(WebGUI, 232, holdTime=None, repeatTime=None)  

tv_off_total_3 = Button(WebGUI, 217, holdTime=None, repeatTime=None)  
tv_on_total_3 = Button(WebGUI, 216, holdTime=None, repeatTime=None)  




#Btn events listing
BtnEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
#NavigationGroups
NaviGroup   = [BtnImageSettings, BtnTVSettings, BtnCamControlSettings, BtnMicControlSettings, PowerControlSettings, BtnMainMenuPowerOn, back_from_conn_page_btn,
               BtnMainMenuTVControl, BtnMainMenuImageControl, backFromModeBtn, BtnSimpleConferenceModMenu, BtnSimpleConferenceModMenu2, BtnExpertMode,
               BtnMainMenuImage_1Control, back_to_main_btn, BtnMainMenuMicControl, connection_page_btn]

# Total TV power control group
power_all_tv_up = [video_wall_power_up_btn, tv_on_total_1, tv_on_total_2, tv_on_total_3]
power_all_tv_down = [video_wall_power_down_btn, tv_off_total_1, tv_off_total_2, tv_off_total_3]

#PowerControlGroup
lightPowerGroup = [light_1_power_on, light_1_power_off, light_2_power_on, light_2_power_off]

camPowerGroup = [cam1powerOn, cam1powerOff, cam2powerOn, cam2powerOff, cam3powerOn, cam3powerOff]

priority_launcher = [priority_launcher1, priority_launcher2]

#MicControlGroup
mic_off_group = [mic_off_conference_1, mic_off_conference_2, mic_off_conference_3, mic_off_conference_without_leader]

#PageImageControlGroup
terminate_automode_and_conference = [finishLocalConference, finishVideoConference]

image_control_group = [videoWallBtn1, videoWallBtn2, videoWallBtn3, videoWallBtn4, videoWallBtn5, videoWallBtn6, videoWallBtn7,
                       tableSplitterVideoBtn1, tableSplitterVideoBtn2, tableSplitterVideoBtn3, tableSplitterVideoBtn4,
                       speakerVideoBtn1, speakerVideoBtn2, speakerVideoBtn3, speakerVideoBtn4, operatorVideoBtn1, operatorVideoBtn2,
                       operatorVideoBtn3, operatorVideoBtn4, operatorVideoBtn5, operatorVideoBtn6, camVideoBtn1, camVideoBtn2, camVideoBtn3,
                       camVideoBtn4]

video_out_btn_group = [video_out1_btn, video_out2_btn, video_out3_btn, video_out_loc1_btn, video_out_loc2_btn]


#PageModeSelection
conference_preset_group = [localPresentationModeBtn, videoConferenceModeBtn]
conference_start_and_stop_btns = [begin_conference_btn, terminate_conference_btn]


stream.init_buttons(WebGUI)
stream.init_control_group()
stream.reset()


cameras.init_buttons(WebGUI)        
cameras.init_cam_control_group()
cameras.socket_init()
# cameras.reset() #TODO

lcd.init_buttons(WebGUI)
lcd.init_lcd_control_group()
lcd.lcd_launch_reset() 

table.init_buttons(WebGUI)
table.init_table_lcd_control_group()

confhost.init_buttons(WebGUI)  
confhost.init_mic_btn_group()
confhost.set_default_btn_states()

connection_check.init_buttons(WebGUI)
connection_check.init_netcheck_control_group()

schneider_light.Initialize()


def Initialize():
    WebGUI.ShowPage('PageModeSelection')
    global micAnswer
    micAnswer = ''
    global mainBuffer
    mainBuffer = b''
    global automode
    automode = False
    autotracking.active_cam_mode == False
    manual_automode_btn.SetState(1)
    priority_launcher1.SetState(1)
    priority_launcher2.SetState(1)


#INCOMING DATA RS232
@event(MicControlInput, 'ReceiveData')
def MainFeedbackHandler(interface, rcvString):
    global automode
    print('Got RS232 string')
    logs_screen.custom_logger('Got RS232 string')
    print(rcvString)
    logs_screen.custom_logger(rcvString)
    print('Automode state is:')
    logs_screen.custom_logger('Automode state is:')
    print(automode)
    logs_screen.custom_logger(automode)

    confhost.mic_state_checker(rcvString, automode)


    
#mic btn click listner
@event(confhost.MIC_BTNS_GRP, BtnEventList)
def mic_bt_click(button, state):
    if state == 'Pressed':
        print('Mic btn clicked')
        logs_screen.custom_logger('Mic btn clicked')
        confhost.set_mic_power(button.ID)


#LCD on table lift UP
@event(table.PULL_UP_BTN_GRP, BtnEventList)
def table_up_btn_click(button, state):
    if state == 'Pressed':
        print('Table lift UP command')
        logs_screen.custom_logger('Table lift UP command')
        table.pull_up()

#LCD on table lift DOWN
@event(table.PULL_DOWN_BTN_GRP, BtnEventList)
def table_down_btn_click(button, state):
    if state == 'Pressed':
        print('Table lift DOWN command')
        logs_screen.custom_logger('Table lift DOWN command')
        table.pull_down()


#Navigation in application event    
@event(NaviGroup, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        button_actions = {
            1: {'pages': ['PageImageControl_1'], 'message': "Page Image Control Open" }, #temprary changed to _1
            2: {'pages': ['PageMain'], 'message': "Page Main Open" },
            3: {'pages': ['PageTVContol'], 'message': "PageTVControl Open" },
            4: {'pages': ['PageCamControl'], 'message': "PageCamControl Open" },
            5: {'pages': ['PageMicControl'],'message': "Page Mic Control Open" },
            6: {'pages': ['PageMain'], 'message': "Page Main Open" },
            7: {'pages': ['PageMain'], 'message': "Page Main Open" },
            8: {'pages': ['PageMain'], 'message': "Page Main Open" },
            9: {'pages': ['PageMain'], 'message': "Page Main Open" },
            10: {'pages': ['PageMain'], 'message': "Page Main Open" },
            11: {'pages': ['PageMain'], 'message': "Page Main Open" },
            12: {'pages': ['PageMain'], 'message': "Page Main Open" },
            13: {'pages': ['PagePowerOn'], 'message': "Page PowerON" },
            149: {'pages': ['PageMain'], 'message': "Page Main Open" },
            183: {'pages': ['PageModeSelection'], 'message': "Page Easy Conference Open" },
            154: {'pages': ['PageModeSelection'], 'message': "Page Easy Conference Open" },
            174: {'pages': ['PageMain'], 'message': "Page Main Open" },
            184: {'pages': ['PageModeSelection'], 'message': "Page Easy Conference Open" },
            179: {'pages': ['PageModeSelection_1'], 'message': "Page Presentation Open" },
            153: {'pages': ['PageModeSelection_2'], 'message': "Page Videoconference Open" },
            270: {'pages': ['PageMain'], 'message': "Page Main Open" },            
            133: {'pages': ['PageMain'], 'message': "Page Main Open" },
            134: {'pages': ['PageMain'], 'message': "Page Main Open" },
            194: {'pages': ['PageConnectionCheck'], 'message': "PageConnectionCheck Open" }
        }

        if button.ID in button_actions:
            action = button_actions[button.ID]
            if 'pages' in action:
                for page in action['pages']:
                    WebGUI.ShowPage(page)
            if 'message' in action:
                print(action['message'])
                logs_screen.custom_logger(action['message'])

#LOGS SCREEN EVENT
@event(logs_screen_btn, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        logs_screen.update_logs()
        WebGUI.ShowPage('PageLogsToText')




#STREAM CONTROL 
@event(stream_const.STREAM_CONTROL_GRP, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        stream.process_button(button)


#TV ID SELECT 
@event(lcd_const.LCD_IDS_GRP, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.lcd_node_changer(button.ID)
        print('TV ID selection btn pressed')
        logs_screen.custom_logger('TV ID selection btn pressed')


#TV ACTION SELECT 
@event(lcd_const.LCD_ACTION_GRP, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.menu_navigation(button.ID) #TODO ACTIONS
        print('TV menu btn pressed')
        logs_screen.custom_logger('TV menu btn pressed')


#TV POWER STATE SELECT 
@event(lcd_const.LCD_POWER_GRP, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.tv_power_control(button.ID) 
        print('TV power btn pressed')
        logs_screen.custom_logger('TV power btn pressed')


#TV NUMBERS COMMAND SENDER 
@event(lcd_const.LCD_NUMBER_PADS_GRP, BtnEventList)
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.set_keypad(button.ID)
        print('TV keypad btn pressed')
        logs_screen.custom_logger('TV keypad btn pressed')


#CAMERAS SELECTION EVENT
@event(cameras_const.CAM_CONTROL_GRP, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        cameras.camera_state_checker(button.ID)
        cameras.camera_node_checker(button.ID)
        cameras.active_cameras = button.ID
        cameras.active_presets = 0 #TODO RESET active PRESETS ON CHANGE


#PRESET SHOW AND SAVE BTNS
@event(cameras_const.CAM_PRESET_CONTROL_GRP, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        cameras.preset_walker(button.ID)



#CAMERAS SELECTION EVENT
@event(cameras_const.CAM_PRESET_GRP, BtnEventList) 
def ButtonObjectPressed(button, state):
    preset_btns_ids_to_numbers = {
        109: {'id' : 1},
        110: {'id' : 2},
        111: {'id' : 3},
        112: {'id' : 4},
        113: {'id' : 5},
        114: {'id' : 6},
        115: {'id' : 7},
        116: {'id' : 8},
        117: {'id' : 9},
        197: {'id' : 10},
        198: {'id' : 11}
    }
        
    if state == 'Pressed':
        
        if button.ID in preset_btns_ids_to_numbers:
            active_preset = preset_btns_ids_to_numbers[button.ID]
            cameras.active_preset_number=active_preset['id']
        cameras.active_presets = button.ID #TODO IF not needed - delete
        cameras.camera_preset_checker(button.ID)


#CAMERAS CONTROL EVENT
@event(cameras_const.CAM_ACTION_GRP, BtnEventList) 
def ButtonObjectPressed(button, state):
    
    if state == 'Pressed':

        button_actions = {
            103: {'action': '1', 'message': "UP" },
            104: {'action': '2', 'message': "HOME" },
            105: {'action': '3', 'message': "DOWN" },
            106: {'action': '4', 'message': "LEFT" },
            107: {'action': '5', 'message': "RIGHT" },
            15: {'action': '6', 'message': "ZOOM IN" },
            102: {'action': '7', 'message': "ZOOM OUT" },
            108: {'action': '8', 'message': "FOCUS" },
            127: {'action': '9', 'message': "POWER ON" },
            126: {'action': '10', 'message': "POWER OFF" }
        }

        if button.ID in button_actions:
            action = button_actions[button.ID]      
            print(action['message'])
            logs_screen.custom_logger(action['message'])
            cameras.cameras_actions(action['action'])
        else: 
            logs_screen.custom_logger('wrong button id in cameras control event')
            print('wrong button id in cameras control event')

    if state == 'Released':
        logs_screen.custom_logger('Released camera action key')
        print('Released camera action key')
        cameras.cameras_actions('0')
        cameras.cameras_actions('11')



#videowall power control from powerOn page 
@event(power_all_tv_up, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.total_power_on()
        
#videowall power control from powerOn page 
@event(power_all_tv_down, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        lcd.total_power_off()

#camera power control from powerOn page 
@event(camPowerGroup, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        cameras.cam_power_group(button.ID)

#light control 
@event(lightPowerGroup, BtnEventList) 
def ButtonObjectPressed(button, state):
    if state == 'Pressed':
        schneider_light.command_selector(button.ID)


#Conference Mode Selector 
@event(conference_preset_group, BtnEventList) 
def ButtonObjectPressed(button, state):
    global conference_type
    if state == 'Pressed':
        if button.ID == 179:
            localPresentationModeBtn.SetState(0)
            videoConferenceModeBtn.SetState(1)
            conference_type = 'local'
        elif button.ID == 153:
            localPresentationModeBtn.SetState(1)
            videoConferenceModeBtn.SetState(0)
            conference_type = 'video'            


#BEGIN CONFERENCE IN SIMPLE AUTOMODE
@event(conference_start_and_stop_btns, BtnEventList)
def conference_start_and_stop(button, state):
    global automode
    global conference_type

    if state == 'Pressed':
        if button.ID == 11: #begin
            if conference_type != None:
                main_utils.mic_off()

                if conference_type == 'local':
                    WebGUI.ShowPage('PageModeSelection_1')
                    ic2.quick_preset_launcher(conference_type)
                    automode = False
                elif conference_type == 'video':
                    WebGUI.ShowPage('PageModeSelection_2')
                    ic2.quick_preset_launcher(conference_type)
                    automode = True
                    #TODO RESET BTNS
                    #TODO RESET TRACKING

            else:
                logs_screen.custom_logger('Select type of conference first')
                print('Select type of conference first')
            #TODO RESET BTN STATES
            

#CHANGE VIDEO SOURCES IN EXPERT MODE
@event(image_control_group, BtnEventList)
def conference_start_and_stop(button, state):
    if state == 'Pressed':
        ic2.expert_mode_launcher(button.ID)


#EVENT FOR AUTOMODE MANUAL CONTROL
@event(manual_automode_btn, BtnEventList)
def automode_button(button, state):
    global automode
    if state == 'Pressed':
        if automode == False:
            manual_automode_btn.SetState(0)
            automode = True
            cameras.previous_mic_ids = [None, None, None]
            main_utils.mic_off()
            cameras.camera_set_default_preset()
        elif automode == True:
            manual_automode_btn.SetState(1)
            automode = False  
            cameras.previous_mic_ids = [None, None, None]
            main_utils.mic_off()
            cameras.camera_set_default_preset()


#TERMINATE AUTOMODE ON EXIT FROM CONFERENCE
@event(terminate_automode_and_conference, BtnEventList)
def automode_button(button, state):
    global automode
    if state == 'Pressed':
        WebGUI.ShowPage('PageModeSelection')
        manual_automode_btn.SetState(0)
        automode = False
        autotracking.previous_mic_ids = [None, None, None]
        autotracking.active_cam_mode == False
        ic2.videoconference_presentation_source(213)
        main_utils.mic_off()
        manual_automode_btn.SetState(1)
        priority_launcher1.SetState(1)
        priority_launcher2.SetState(1)
        autotracking.reset_autotracking_priority()


#SHUTDOWN MIC (ALL AND WITHOUT LEADER) IN CONFERENCE
@event(mic_off_group, BtnEventList)
def automode_button(button, state):
    if state == 'Pressed':
        main_utils.mic_killer(button.ID)

#RESET IMAGE STATES
@event(BtnMainMenuImageControl, 'Released')
def ButtHandler(btn, state):
    if state == 'Pressed':
        stream.reset()


#RESET CAMERA STATES ON EXIT
@event(BtnMainMenuCamControl, BtnEventList)
def mic_bt_click(button, state):
    if state == 'Pressed':
        cameras.reset_cameras_states()
        priority_launcher1.SetState(1)
        priority_launcher2.SetState(1)
        WebGUI.ShowPage('PageMain')


#RESTART DEVICE
@event(restart_system_btn, BtnEventList)
def ButtHandler(btn, state):
    if state == 'Pressed':
        ProProcessor.Reboot()
        logs_screen.custom_logger('Reboot initialized. Wait for system restart.')
        print('Reboot initialized. Wait for system restart.')


    
#connection check
@event(connection_check.CONNECTION_HOSTS_GRP, BtnEventList)
def netcheck_btn_click(button, state):
    if state == 'Pressed':
        print('Network host check connection btn clicked')
        logs_screen.custom_logger('Network host check connection btn clicked')
        connection_check.connection_checker(button.ID)


#select mode usb video mode in conference
@event(video_out_btn_group, BtnEventList)
def video_out_btn_click(button, state):
    if state == 'Pressed':
        print('Presentation mode changed in videoconference')
        logs_screen.custom_logger('Presentation mode changed in videoconference')
        ic2.videoconference_presentation_source(button.ID)


#cam priority mode activation
@event(priority_launcher, BtnEventList)
def cam_priority_btn_click(button, state):
    if state == 'Pressed':
        if button.State == 0:
            priority_launcher1.SetState(1)
            priority_launcher2.SetState(1)
            autotracking.active_cam_mode = True 
            autotracking.reset_autotracking_priority()
        elif button.State == 1:
            priority_launcher1.SetState(0)
            priority_launcher2.SetState(0)
            autotracking.active_cam_mode = False
            # autotracking.reset_autotracking_priority()
        print('Camera priority mode changed')
        logs_screen.custom_logger('Camera priority mode changed')



Initialize()