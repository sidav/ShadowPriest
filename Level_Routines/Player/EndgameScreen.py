from Routines import TdlConsoleWrapper as CW, SidavRandom as RND
from GLOBAL_DATA import Global_Constants as GC
import time

_fade_in_sparkles_per_frame = 75
_fade_out_sparkles_per_frame = 45
_sparkles_color = (32, 132, 0)

_death_texts = [
    [
        " ________             __          ___                __          _           __",
        "/_  __/ /  ___ ____  / /__ ___   / _/__  ____  ___  / /__ ___ __(_)__  ___ _/ /",
        " / / / _ \/ _ `/ _ \/  '_/(_-<  / _/ _ \/ __/ / _ \/ / _ `/ // / / _ \/ _ `/_/ ",
        "/_/ /_//_/\_,_/_//_/_/\_\/___/ /_/ \___/_/   / .__/_/\_,_/\_, /_/_//_/\_, (_)  ",
        "                                            /_/          /___/       /___/     "
    ]
]
def _determine_x_position(arr):
    ww = GC.CONSOLE_WIDTH
    if isinstance(arr, list):
        picw = len(arr[0])
        return int((ww - picw) * 0.5)
    elif isinstance(arr, str):
        picw = len(arr)
        return int((ww - picw)*0.47)


def _determine_y_position(arr):
    wh = GC.CONSOLE_HEIGHT
    pich = len(arr)
    return int((wh-pich)/5)


def finalize_pic(pic):
    final = []
    for i in range(len(pic)):
        final.append(list(pic[i]))

    for i in range(len(final)):
        for j in range(len(final[i])):
            print("{}, {}".format(len(final), len(final[i])))
            if final[i][j] == '#':
                final[i][j] = chr(219)
            elif final[i][j] == '%':
                final[i][j] = chr(178)
            elif final[i][j] == ':':
                final[i][j] = chr(176)
    return final

def get_char_for_sparkle(death_text, fade_in, x = 0, y = 0):
    blood_sparkles = [';', '!', '*', '%', '&', '?', '_', '\\', '/', '|', '(', ')', '$', '@', '~', '#', chr(177)]
    if fade_in:
        # curr_char = blood_sparkles[RND.rand(len(blood_sparkles))]
        rand = RND.rand(255)
        if 64 < rand < 91:
            rand = RND.rand(255)
        curr_char = chr(rand)
        return curr_char
    else:
        xpos = _determine_x_position(death_text)
        ypos = _determine_y_position(death_text)
        if x - xpos < 0 or x - xpos >= len(death_text[0]) or y - ypos < 0 or y -ypos >= len(death_text):
            # print('OUT OF BOUNDS, x{} xpos{} coord{}'.format(x, xpos, x-xpos))
            return ' '
        # print('IN BOUNDS, x{} xpos{} coord{}'.format(x, xpos, x - xpos))
        curr_char = list(death_text[y-ypos])[x-xpos]
        return curr_char


def show_endgame_screen(forced=False):
    if forced or not GC.DEBUG_ENABLED:
        _death_texts[0] = finalize_pic(_death_texts[0])
        chosen_text = _death_texts[RND.rand(len(_death_texts))]

        bottom_margin = 2 # the number is the UI height
        w = GC.CONSOLE_WIDTH
        h = GC.CONSOLE_HEIGHT - bottom_margin
        bloody_pixels_on_screen = [[False] * h for _ in range(w)]
        total_shown_pixels = 0

        # FIRST: fill the screen with blood.
        while total_shown_pixels < w * h:
            # draw blood
            for _ in range(_fade_in_sparkles_per_frame):
                if total_shown_pixels >= w*h:
                    break
                number = RND.rand(w * h)
                coord_x, coord_y = number % w, number // w

                while bloody_pixels_on_screen[coord_x][coord_y]:
                    number += 1
                    if number >= w*h:
                        number = 0
                    coord_x, coord_y = number % w, number // w

                CW.setForegroundColor(_sparkles_color)
                sparkle = get_char_for_sparkle(chosen_text, True)
                CW.putChar(sparkle, coord_x, coord_y)

                bloody_pixels_on_screen[coord_x][coord_y] = True
                total_shown_pixels += 1
            CW.flushConsole()

        # SECOND: clear everything except the 'you're dead' label.
        total_shown_pixels = 0
        while total_shown_pixels < w * h:
            # draw blood
            for _ in range(_fade_out_sparkles_per_frame):
                if total_shown_pixels >= w*h:
                    break
                number = RND.rand(w * h)
                coord_x, coord_y = number % w, number // w

                while not bloody_pixels_on_screen[coord_x][coord_y]:
                    number += 1
                    if number >= w * h:
                        number = 0
                    coord_x, coord_y = number % w, number // w

                CW.setForegroundColor(_sparkles_color)
                CW.putChar(get_char_for_sparkle(chosen_text, False, coord_x, coord_y), coord_x, coord_y)
                bloody_pixels_on_screen[coord_x][coord_y] = False
                total_shown_pixels += 1
            # CW.setForegroundColor(sparkles_color)
            CW.flushConsole()
        show_statistics()
        time.sleep(1)
        CW.readKey()
        if not forced:
            exit()


def show_statistics():
    from ..Controllers import LevelController as LC
    from . import Statistics as stat
    time.sleep(1)
    CW.setForegroundColor(0, 128, 0)
    line = "Your walkthrough lasted for {}.{} turns.".format(LC.get_current_turn() // 10, LC.get_current_turn() % 10)
    put_line_in_a_middle(line, 11)
    CW.flushConsole()
    time.sleep(1)
    line = "You killed {} enemies and knocked out {} ones.".format(stat.enemies_killed, stat.enemies_KOed)
    put_line_in_a_middle(line, 12)
    CW.flushConsole()
    time.sleep(1)
    line = "You have been spotted {} times and caused {} alarms".format(stat.spotted_times, stat.total_alarms)
    put_line_in_a_middle(line, 13)
    CW.flushConsole()
    time.sleep(1)
    line = "You have healed {} hitpoints, and lost {} hitpoints in total".format(stat.total_hp_lost, stat.total_healed)
    put_line_in_a_middle(line, 14)
    CW.flushConsole()
    time.sleep(1)


def put_line_in_a_middle(line, y):
    x = GC.CONSOLE_WIDTH // 2 - len(line) // 2
    CW.putString(line, x, y)
