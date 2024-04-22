from extronlib.device import UIDevice
from extronlib.ui import Button

from stream_util import *
from stream_const import *
import logs_screen


active_inputs = []
active_formats = []
active_outputs = []


def init_buttons(webgui: UIDevice):
    print("Initializing Stream buttons")
    logs_screen.custom_logger("Initializing Stream buttons")
    INPUT_BTNS[80] = Button(webgui, 80, holdTime=None, repeatTime=None)
    INPUT_BTNS[81] = Button(webgui, 81, holdTime=None, repeatTime=None)
    INPUT_BTNS[82] = Button(webgui, 82, holdTime=None, repeatTime=None)
    INPUT_BTNS[83] = Button(webgui, 83, holdTime=None, repeatTime=None)
    INPUT_BTNS[84] = Button(webgui, 84, holdTime=None, repeatTime=None)
    INPUT_BTNS[85] = Button(webgui, 85, holdTime=None, repeatTime=None)
    INPUT_BTNS[86] = Button(webgui, 86, holdTime=None, repeatTime=None)

    FORMAT_BTNS[96] = Button(webgui, 96, holdTime=None, repeatTime=None)
    FORMAT_BTNS[297] = Button(webgui, 297, holdTime=None, repeatTime=None)
    FORMAT_BTNS[98] = Button(webgui, 98, holdTime=None, repeatTime=None)
    FORMAT_BTNS[99] = Button(webgui, 99, holdTime=None, repeatTime=None)

    OUTPUT_BTNS[88] = Button(webgui, 88, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[89] = Button(webgui, 89, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[90] = Button(webgui, 90, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[91] = Button(webgui, 91, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[92] = Button(webgui, 92, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[93] = Button(webgui, 93, holdTime=None, repeatTime=None)
    OUTPUT_BTNS[94] = Button(webgui, 94, holdTime=None, repeatTime=None)
    
    CTRL_BTNS[101] = Button(webgui, 101, holdTime=None, repeatTime=None)


def init_control_group():
    print("Initializing Stream control group")
    logs_screen.custom_logger("Initializing Stream control group")
    append_to_ctrl_grp(INPUT_BTNS.values())
    append_to_ctrl_grp(FORMAT_BTNS.values())
    append_to_ctrl_grp(OUTPUT_BTNS.values())
    append_to_ctrl_grp(CTRL_BTNS.values())
    # print("Stream control group:" + str(STREAM_CONTROL_GRP))


def reset():
    print('Resetting Stream buttons')
    logs_screen.custom_logger('Resetting Stream buttons')
    active_inputs.clear()
    active_formats.clear()
    active_outputs.clear()
    set_enabled(True, inputs=True)
    set_enabled(False, formats=True, outputs=True)
    set_state(0, inputs=True, formats=True, outputs=True)


def process_button(button: Button):
    # print("Processing button ID:" + str(button.ID))

    if button.ID in INPUT_BTNS.keys():
        if len(active_inputs) >= 1:
            active_inputs.clear()

        button.SetState(1)
        set_state(0, inputs=True, formats=True, outputs=True, id_to_skip=button.ID)
        set_enabled(False, outputs=True)
        set_enabled(True, formats=True)

        active_formats.clear()
        active_outputs.clear()

        active_inputs.append(button.ID)

    elif button.ID in FORMAT_BTNS.keys():
        if len(active_formats) >= 1:
            set_state(0, formats=True, outputs=True)
            active_outputs.clear()
            active_formats.clear()
                
        button.SetState(1)
        active_formats.append(button.ID)
        set_enabled(True, outputs=True)

    elif button.ID in OUTPUT_BTNS.keys():
        max_outputs = FORMAT_OUTPUTS[active_formats[0]]

        if len(active_outputs) < max_outputs:
 
            if button.State == 1:
                button.SetState(0)
                active_outputs.remove(button.ID)
            else:
                button.SetState(1)
                active_outputs.append(button.ID)
        
            if len(active_outputs) == max_outputs:
                set_enabled(False, outputs=True, ids_to_skip=active_outputs)
        else:
            if button.ID in active_outputs:
                button.SetState(0)
                active_outputs.remove(button.ID)
                set_enabled(True, outputs=True)


    elif button.ID in CTRL_BTNS.keys():
        if button.ID == 101 and len(active_inputs) > 0 \
            and len(active_formats) > 0 and len(active_outputs) > 0:
                input_id = active_inputs[0]
                output_res = OUPUT_RESOLUTIONS[input_id]
                output_cmd = OUTPUTS[input_id]


