from Routines import TdlConsoleWrapper as CW, SidavRandom as RND
from GLOBAL_DATA import Global_Constants as GC

_death_text = [
    " _  _  _____  __ __ // _____ _____    _____ _____  ___  _____ ",
    " \\\\// ((   )) || ||    ||_// ||==     ||  ) ||==  ||=|| ||  ) ",
    "  //   \\\\_//  \\\\_//    || \\\\ ||___  _ ||_// ||___ || || ||_// ",
    "                                                              "
]

# _death_text = [
#     'Yb  dP  dP"Yb  88   88  .o. 88""Yb 888888     8888b.  888888    db    8888b.',
#     ' YbdP  dP   Yb 88   88, dP  88__dP 88__        8I  Yb 88__     dPYb    8I  Yb',
#     '  8P   Yb   dP Y8   8P      88"Yb  88""        8I  dY 88      dP  Yb   8I  dY',
#     '  dP    YbodP  `YbodP`      88  Yb 888888     8888Y"  888888 dP""""Yb 8888Y"'
# ]
#
# _death_text = [
#     ' %%  %%   %%%%   %%  %% %% %%%%%   %%%%%%         %%%%%   %%%%%%   %%%%   %%%%%  ',
#     '  %%%%   %%  %%  %%  %% %% %%  %%  %%             %%  %%  %%      %%  %%  %%  %% ',
#     '   %%    %%  %%  %%  %%  % %%%%%   %%%%           %%  %%  %%%%    %%%%%%  %%  %% ',
#     '   %%    %%  %%  %%  %%    %%  %%  %%             %%  %%  %%      %%  %%  %%  %% ',
#     '   %%     %%%%    %%%%     %%  %%  %%%%%%         %%%%%   %%%%%%  %%  %%  %%%%%  '
# ]

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
    return int((wh-pich)/3)


def _draw_death_text():
    # CW.setForegroundColor(196, 0, 0)
    xpos = _determine_x_position(_death_text)
    ypos = _determine_y_position(_death_text)
    # CW.drawCharArrayAtPosition(_death_text, x, y, True)
    # for i in range(len(_death_text)):
    #     CW.putString(_death_text[i], x, i + y)
    for y in range(len(_death_text)):
        for x in range(len(_death_text[y])):
            curr_char = list(_death_text[y])[x]
            if curr_char != ' ':
                CW.putChar(curr_char, x + xpos, y + ypos)


def show_death_screen(player):
    bottom_margin = GC.LOG_HEIGHT + 2 # the 2 is the UI height
    w = GC.CONSOLE_WIDTH
    h = GC.CONSOLE_HEIGHT - bottom_margin
    bloody_pixels_on_screen = [[' '] * h for _ in range(w)]
    blood_sparkles = [',', ';', '!', '*', '`', '%', '&', '?', chr(177)]
    total_shown_pixels = 0
    sparkles_color = (128, 0, 0)
    blood_per_frame = 50

    # FIRST: fade in the YOURE DEAD label.
    text_r = 0
    text_g = 0
    text_b = 0
    # while (text_r < 200):
    #     CW.setForegroundColor(text_r, text_g, text_b)
    #     draw_death_text()
    #     text_r += 16
    #     text_g += 1
    #     text_b += 1
    #     CW.flushConsole()
    #     import time
    #     time.sleep(0.1)

    # SECOND: draw the blood around
    while total_shown_pixels < w * h:
        # draw blood
        for _ in range(blood_per_frame):
            if total_shown_pixels >= w*h:
                break
            number = RND.rand(w * h)
            coord_x, coord_y = number % w, number // w

            while bloody_pixels_on_screen[coord_x][coord_y] != ' ':
                number += 1
                if number >= w*h:
                    number = 0
                coord_x, coord_y = number % w, number // w

            CW.setForegroundColor(sparkles_color)
            sparkle = blood_sparkles[RND.rand(len(blood_sparkles))] # chr(RND.rand(256))
            CW.putChar(sparkle, coord_x, coord_y)

            bloody_pixels_on_screen[coord_x][coord_y] = sparkle
            total_shown_pixels += 1

        CW.flushConsole()

    total_shown_pixels = 0
    while total_shown_pixels < w * h:
        # draw blood
        for _ in range(blood_per_frame):
            if total_shown_pixels >= w*h:
                break
            number = RND.rand(w * h)
            coord_x, coord_y = number % w, number // w

            while bloody_pixels_on_screen[coord_x][coord_y] == ' ':
                number += 1
                if number >= w * h:
                    number = 0
                coord_x, coord_y = number % w, number // w

            CW.setForegroundColor(sparkles_color)
            CW.putChar(' ', coord_x, coord_y)
            bloody_pixels_on_screen[coord_x][coord_y] = ' '
            total_shown_pixels += 1

        # text_r = int(255 * total_shown_pixels / (w * h) )
        CW.setForegroundColor(sparkles_color)
        _draw_death_text()
        CW.flushConsole()
    CW.readKey()
