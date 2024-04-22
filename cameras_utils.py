from cameras_const import *


def append_to_cam_ctrl_grp(btns):
    for btn in btns:
        CAM_CONTROL_GRP.append(btn)    


def append_to_act_grp(btns):
    for btn in btns:
        CAM_ACTION_GRP.append(btn)  


def append_to_pres_grp(btns):
    for btn in btns:
        CAM_PRESET_GRP.append(btn)  

def append_to_cam_presets_act(btns):
    for btn in btns:
        CAM_PRESET_CONTROL_GRP.append(btn)

#btn set state if it is in id_to_skip
def set_state(cam_preset_list=False, cam_ids_list=False, id_cam_to_skip:int=None, id_preset_to_skip:int=None):

    if cam_preset_list==True: #associate function with list
        for btn in CAM_PRESETS.values():
            if btn.ID != id_preset_to_skip:
                btn.SetState(0)
            elif btn.ID == id_preset_to_skip:
                btn.SetState(1)

        
    if cam_ids_list==True: #associate function with list
        # print('cam id is TRUE')
        for btn in CAM_IDS.values():
            if btn.ID != id_cam_to_skip:
                btn.SetState(0)
            elif btn.ID == id_cam_to_skip:
                btn.SetState(1)
