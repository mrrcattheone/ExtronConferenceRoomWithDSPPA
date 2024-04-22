from connection_check_const import *

def append_to_net_ctrl_grp(*btns):
    for btn in btns:
        CONNECTION_HOSTS_GRP.append(btn)