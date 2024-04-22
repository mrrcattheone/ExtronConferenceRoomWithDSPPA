import cameras
import main_utils
import ic2
import logs_screen

active_mic_list = []
previous_mic_ids = [None, None, None]
active_cam_mode = True

active_cameras = 0 # set from main page in listener. camera btn id
active_preset_number = 0 # set from main page. preset number 1 to 9
active_presets = 0 # set from main page in listener. preset btn id

#init
def Initialize():
    global previous_mic_ids
    previous_mic_ids = [None, None, None]
    logs_screen.custom_logger('Autotracking initialized')
    

#reset autotracking states
def reset_autotracking_priority():
    ic2.videoconference_with_priority(0)
    logs_screen.custom_logger('Head priority on')
    print('Head priority on')


#autotracking via mic ids
def autotrack(id_mic, mic_state):

    global previous_mic_ids   
    # global active_cam_mode

    
    id_presets_to_id_mic = {
        1 : {'preset': 1, 'sector': 0, 'active_cam': 17},
        2 : {'preset': 1, 'sector': 1, 'active_cam': 18},
        3 : {'preset': 2, 'sector': 1, 'active_cam': 18},
        4 : {'preset': 3, 'sector': 1, 'active_cam': 18},
        5 : {'preset': 4, 'sector': 1, 'active_cam': 18},
        6 : {'preset': 5, 'sector': 1, 'active_cam': 18},
        7 : {'preset': 6, 'sector': 1, 'active_cam': 18},
        8 : {'preset': 7, 'sector': 1, 'active_cam': 18},
        9 : {'preset': 8, 'sector': 1, 'active_cam': 18},
        10: {'preset': 9, 'sector': 1, 'active_cam': 18},
        11 : {'preset': 10, 'sector': 2, 'active_cam': 16},
        12 : {'preset': 9, 'sector': 2, 'active_cam': 16},
        13 : {'preset': 8, 'sector': 2, 'active_cam': 16},
        14 : {'preset': 7, 'sector': 2, 'active_cam': 16},
        15 : {'preset': 6, 'sector': 2, 'active_cam': 16},
        16 : {'preset': 5, 'sector': 2, 'active_cam': 16},
        17 : {'preset': 4, 'sector': 2, 'active_cam': 16},
        18 : {'preset': 3, 'sector': 2, 'active_cam': 16},
        19 : {'preset': 2, 'sector': 2, 'active_cam': 16},
        20 : {'preset': 1, 'sector': 2, 'active_cam': 16},
        }
    
    if id_mic in id_presets_to_id_mic: #если полученный ИД найден в списке, то...
        live_mic = id_presets_to_id_mic[id_mic]
        logs_screen.custom_logger('Found mic_id in id_presets_to_id_mic list.')
        print('Found mic_id in id_presets_to_id_mic list.')

        # if confhost.all_mic_disabled == True: #all cam off = preset 11
        #     cameras.camera_set_default_preset()

        if mic_state == 2: #On
            if previous_mic_ids[live_mic['sector']] == None: #if it is = None then it is first item in the list
                
                cameras.camera_node_checker(live_mic['active_cam'])
                cameras.active_presets = live_mic['preset']
                cameras.active_cameras = live_mic['active_cam']
                cameras.active_preset_number = cameras.active_presets
                cameras.preset_walker(128)
                previous_mic_ids[live_mic['sector']] = id_mic
                logs_screen.custom_logger('previous_mic_ids = None and it is first iteration')
                

            elif previous_mic_ids[live_mic['sector']] != None:
                if previous_mic_ids[live_mic['sector']] == id_mic:
                    logs_screen.custom_logger('Error: double time active mic. Check it.')
                    print('Error: double time active mic. Check it.')
                elif previous_mic_ids[live_mic['sector']] != id_mic:
                    main_utils.mic_off_with_exception(id_mic, live_mic['sector'])
                    cameras.camera_node_checker(live_mic['active_cam'])
                    cameras.active_presets = live_mic['preset']
                    cameras.active_cameras = live_mic['active_cam']
                    cameras.active_preset_number = cameras.active_presets
                    cameras.preset_walker(128)  
                    logs_screen.custom_logger('previous_mic_ids != id_mic')
                    previous_mic_ids[live_mic['sector']] = id_mic #current id_mic goes previous

            if active_cam_mode == False:#ic2 control
                ic2.videoconference_with_priority(live_mic['sector'])
                logs_screen.custom_logger('Chairman priority disabled')
                print('Chairman priority disabled')
            # else:
            #     logs_screen.custom_logger('Head priority enabled')
            #     print('Head priority enabled')

            
        elif mic_state == 1: #off    
            if previous_mic_ids[live_mic['sector']] != None: #if previous is not empty
                if previous_mic_ids[live_mic['sector']] == id_mic: #if it is same as was - delete from prev and go equal view
                    previous_mic_ids[live_mic['sector']] = None
                    cameras.camera_node_checker(live_mic['active_cam'])
                    cameras.active_presets = 11
                    cameras.active_cameras = live_mic['active_cam']
                    cameras.active_preset_number = cameras.active_presets
                    cameras.preset_walker(128)  
                    logs_screen.custom_logger('is same as was - delete from prev and go equal view')

            else:
                logs_screen.custom_logger('Error: Double mic state = 1 (off). Check it.')
                print('Error: Double mic state = 1 (off). Check it.')
                
                
                     
Initialize()
            