from Routines import TdlConsoleWrapper as CW, SidavRandom as RND
from GLOBAL_DATA import Global_Constants as GC

_death_text = [
    " _  _  _____  __ __ // _____ _____    _____ _____  ___  _____ ",
    " \\\\// ((   )) || ||    ||_// ||==     ||  ) ||==  ||=|| ||  ) ",
    "  //   \\\\_//  \\\\_//    || \\\\ ||___  _ ||_// ||___ || || ||_// ",
    "                                                              "
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
    return int((wh-pich)/3)


def _draw_death_text():
    # CW.setForegroundColor(196, 0, 0)
    x = _determine_x_position(_death_text)
    y = _determine_y_position(_death_text)
    CW.drawCharArrayAtPosition(_death_text, x, y, True)


def show_death_screen(player):
    bottom_margin = GC.LOG_HEIGHT + 2 # the 2 is the UI height
    w = GC.CONSOLE_WIDTH
    h = GC.CONSOLE_HEIGHT - bottom_margin
    bloody_pixels_on_screen = [[False] * h for _ in range(w)]
    blood_sparkles = [',', ';', '!', '*', '`', '%', '&', chr(177)]
    total_shown_pixels = 0
    sparkles_color = (96, 0, 0)
    blood_per_frame = 25

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
            number = RND.rand(w * h)
            coord_x, coord_y = number % w, number // w

            print("{} of {} ({}/{})".format(total_shown_pixels, w * h, w, h))

            while bloody_pixels_on_screen[coord_x][coord_y]:
                number += 1
                if number >= w*h:
                    number = 0
                coord_x, coord_y = number % w, number // w

            CW.setForegroundColor(sparkles_color)
            sparkle_index = RND.rand(len(blood_sparkles))
            CW.putChar(blood_sparkles[sparkle_index], coord_x, coord_y)
            bloody_pixels_on_screen[coord_x][coord_y] = True
            total_shown_pixels += 1

        # draw 'you're dead' label
        text_r = int(255 * total_shown_pixels / (w * h) )
        CW.setForegroundColor(text_r, text_g, text_b)
        _draw_death_text()
        CW.flushConsole()
    CW.readKey()
