import confhost
import logs_screen


def mic_off():  # DISABLE ALL MIC AT CONFERENCE BEGINING
    for mic in range(0, 21):
        PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
        confhost.__SetHelper(PowerCmdString, 1)
    confhost.set_default_btn_states()


def mic_off_with_exception(
    id_mic_to_skip, sector
):  # DISABLE ALL MIC IN SECTOR EXCEPT ONE
    logs_screen.custom_logger("Got ID_MIC to skip: ")
    logs_screen.custom_logger(id_mic_to_skip)
    print("Got ID_MIC to skip: ")
    print(id_mic_to_skip)
    if sector == 1:
        for mic in range(2, 11):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, 1)
    elif sector == 2:
        for mic in range(11, 21):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, 1)
    elif sector == 3:
        for mic in range(1, 21):
            if mic != id_mic_to_skip:
                PowerCmdString = b"\xfb\xfd\x81\x03\x01\x00" + bytes([mic])
                confhost.__SetHelper(PowerCmdString, 1)
                confhost.all_mic_disabled = True

    else:
        print("Wrong sector or first mic")
        logs_screen.custom_logger("Wrong sector or first mic")
    # confhost.set_default_btn_states()


def mic_killer(btn_id):
    if btn_id == 203:
        mic_off_with_exception(0, 3)
    elif btn_id == 231:
        mic_off_with_exception(0, 3)
    elif btn_id == 178:
        mic_off_with_exception(0, 3)
    elif btn_id == 237:
        mic_off_with_exception(1, 3)
