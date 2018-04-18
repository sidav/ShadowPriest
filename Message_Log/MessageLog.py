import Routines.TdlConsoleWrapper as CW
from GLOBAL_DATA.Global_Constants import LOG_HEIGHT, CONSOLE_HEIGHT, CONSOLE_WIDTH, MAP_HEIGHT, DEBUG_MESSAGES_ENABLED
from .Message import LogMessage

all_messages = []


def _add_message_object_to_list(msg):
    if len(all_messages) > 0:
        if all_messages[-1].text == msg.text:
            all_messages[-1].stack += 1
            return
        elif len(all_messages) > 1 and all_messages[-2].text == msg.text:
            all_messages.pop()
            all_messages[-1].stack += 1
            return
        elif all_messages[-1].replaceable:
            all_messages[-1] = msg
            return
    all_messages.append(msg)


def append_message(text):
    _add_message_object_to_list(LogMessage(text))


def append_replaceable_message(text):
    _add_message_object_to_list(LogMessage(text, replaceable=True))
    print_log()
    CW.flushConsole()


def append_error_message(text):
    if DEBUG_MESSAGES_ENABLED:
        _add_message_object_to_list(LogMessage('ERROR: '+text, color=(128, 32, 32)))


def append_warning_message(text):
    if DEBUG_MESSAGES_ENABLED:
        _add_message_object_to_list(LogMessage('WARNING: '+text, color=(192, 192, 32)))
    # print_log()
    # CW.flushConsole()


def print_log():
    last_msgs = all_messages[-LOG_HEIGHT:]

    for i in range(len(last_msgs)):
        CW.putString(str(' ' * CONSOLE_WIDTH), 0, MAP_HEIGHT + i)

    for i in range(len(last_msgs)):
        text = last_msgs[i].text
        stack = last_msgs[i].stack
        if last_msgs[i].stack > 1:
            text += ' (x{0})'.format(stack)
        CW.setForegroundColor(last_msgs[i].color)
        CW.putString(text, 0, MAP_HEIGHT+i)
