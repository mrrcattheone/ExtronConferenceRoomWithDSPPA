from stream_const import *


def append_to_ctrl_grp(btns):
    for btn in btns:
        STREAM_CONTROL_GRP.append(btn)


def set_enabled(enabled: bool, inputs=False, formats=False, outputs=False, ids_to_skip=None):
    if not ids_to_skip:
        ids_to_skip = []

    if inputs:
        for btn in INPUT_BTNS.values():
            if btn.ID not in ids_to_skip: 
                btn.SetEnable(enabled)

    if formats:
        for btn in FORMAT_BTNS.values():
            if btn.ID not in ids_to_skip: 
                btn.SetEnable(enabled)

    if outputs:
        for btn in OUTPUT_BTNS.values():
            if btn.ID not in ids_to_skip: 
                btn.SetEnable(enabled)


def set_state(state: int, inputs=False, formats=False, outputs=False, id_to_skip:int=None):
    if inputs:
        for btn in INPUT_BTNS.values():
            if btn.ID != id_to_skip:
                btn.SetState(state) 

    if formats:
        for btn in FORMAT_BTNS.values():
            if btn.ID != id_to_skip:
                btn.SetState(state)

    if outputs:
        for btn in OUTPUT_BTNS.values():
            if btn.ID != id_to_skip:
                btn.SetState(state)
