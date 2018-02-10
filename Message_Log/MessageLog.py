import Routines.TdlConsoleWrapper as CW
from GLOBAL_DATA.Global_Constants import LOG_HEIGHT, CONSOLE_HEIGHT, CONSOLE_WIDTH
from .LogMessage import LogMessage

all_messages = []


def _add_message_object_to_list(msg):
    if len(all_messages) > 0:
        if all_messages[-1].replaceable:
            all_messages[-1] = msg
            return
    all_messages.append(msg)


def append_message(text):
    _add_message_object_to_list(LogMessage(text))


def append_replaceable_message(text):
    _add_message_object_to_list(LogMessage(text, replaceable=True))
    print_log()
    CW.flushConsole()

def print_log():
    last_msgs = all_messages[-LOG_HEIGHT:]
    for i in range(len(last_msgs)):
        CW.setForegroundColor(last_msgs[i].color)
        CW.putString(last_msgs[i].text, 0, CONSOLE_HEIGHT-LOG_HEIGHT+i)
