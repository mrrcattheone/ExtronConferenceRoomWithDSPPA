INPUT_BTNS = {}
FORMAT_BTNS = {}
OUTPUT_BTNS = {}
CTRL_BTNS = {}

STREAM_CONTROL_GRP = []

FORMAT_OUTPUTS = {
    96: 1,  # 1x1
    297: 2, # 2x1
    98: 3,  # 3x1
    99: 4   # 4x1
}

DEVICES_TMP = {
    'First_Operator_Output': '{SetWindows;600004;10.90.5.32-0,udp://224.168.5.32:35248,0,0,3840,2160}',
    'Second_Operator_Output': '{SetWindows;600004;10.90.5.33-0,udp://224.168.5.33:35252,0,0,3840,2160}',
    'Third_Operator_Output': '{SetWindows;600004;10.90.5.35-0,udp://224.168.5.35:35260,0,0,3840,2160}',
    'Speaker_Output': '{SetWindows;600004;10.90.5.31-0,udp://224.168.5.31:35244,0,0,3840,2160}'
}

OUPUT_RESOLUTIONS = {
    80: (3840, 2160),
    81: (1980, 1020),
    82: (1980, 1020),
    83: (1980, 1020),
    84: (1980, 1020),
    85: (1980, 1020),
    86: (1980, 1020)
}

OUTPUTS = {
    80: "SetWindows;600004;10.90.5.32-0,udp://224.168.5.32:35248,0,0,{},{}",
    81: "SetWindows;600004;10.90.5.33-0,udp://224.168.5.33:35252,0,0,{},{}"
}
