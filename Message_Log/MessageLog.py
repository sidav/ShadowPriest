import Routines.TdlConsoleWrapper as CW
from GLOBAL_DATA.Global_Constants import LOG_HEIGHT, CONSOLE_HEIGHT, CONSOLE_WIDTH

all_messages = []


def append_message(text):
    all_messages.append(text)

def print_log():
    last_msgs = all_messages[-4:]
    CW.setForegroundColor(200, 200, 200)
    for i in range(len(last_msgs)):
        CW.putString(last_msgs[i], 0, CONSOLE_HEIGHT-LOG_HEIGHT+i)
