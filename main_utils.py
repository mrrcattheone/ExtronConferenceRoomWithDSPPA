import confhost
import logs_screen


def mic_off():  # DISABLE ALL MIC AT CONFERENCE BEGINING
    for mic in range(0, 21):
        PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
        confhost.__SetHelper(PowerCmdString, 2)
    confhost.set_default_btn_states()


# DISABLE ALL MIC IN SECTOR EXCEPT SELECTED ONE
def mic_off_with_exception(id_mic_to_skip, sector, priority=2):
    logs_screen.custom_logger("Got ID_MIC to skip: ")
    logs_screen.custom_logger(id_mic_to_skip)
    print("Got ID_MIC to skip: ")
    print(id_mic_to_skip)
    if sector == 1:
        for mic in range(2, 11):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, priority)
    elif sector == 2:
        for mic in range(11, 21):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, priority)
    elif sector == 3:
        for mic in range(1, 21):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, priority)
                confhost.all_mic_disabled = True
    else:
        print("Wrong sector or first mic")
        logs_screen.custom_logger("Wrong sector or first mic")
    # confhost.set_default_btn_states()


def latest_active_mic_off(mic_id, priority=2):
    PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic_id])
    confhost.__SetHelper(PowerCmdString, priority)
    logs_screen.custom_logger("Latest mic turned off")


# shutdown all mics with highest priority (last case without cheafs mic)
def mic_killer(btn_id):
    if btn_id == 203:
        mic_off_with_exception(0, 3, 1)
    elif btn_id == 231:
        mic_off_with_exception(0, 3, 1)
    elif btn_id == 178:
        mic_off_with_exception(0, 3, 1)
    elif btn_id == 237:
        mic_off_with_exception(1, 3, 1)
