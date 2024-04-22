from lcd_const import *


def append_to_lcd_ids_grp(btns):
    for btn in btns:
        LCD_IDS_GRP.append(btn)    


def append_to_action_grp(btns):
    for btn in btns:
        LCD_ACTION_GRP.append(btn)  

def append_to_power_grp(btns):
    for btn in btns:
        LCD_POWER_GRP.append(btn)  

def append_to_number_pads_grp(btns):
    for btn in btns:
        LCD_NUMBER_PADS_GRP.append(btn)  

# #btn set state if it is in id_to_skip
# def set_state(cam_preset_list=False, cam_ids_list=False, id_cam_to_skip:int=None, id_preset_to_skip:int=None):

#     if cam_preset_list==True: #associate function with list
#         for btn in CAM_PRESETS.values():
#             if btn.ID != id_preset_to_skip:
#                 btn.SetState(0)
#             elif btn.ID == id_preset_to_skip:
#                 btn.SetState(1)

        

#     if cam_ids_list==True: #associate function with list
#         print('cam id is TRUE')
#         for btn in CAM_IDS.values():
#             if btn.ID != id_cam_to_skip:
#                 btn.SetState(0)
#             elif btn.ID == id_cam_to_skip:
#                 btn.SetState(1)
