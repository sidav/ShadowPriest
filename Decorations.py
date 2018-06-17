from Routines import TdlConsoleWrapper as CW


def _get_skull_picture(align_left=True):
    if align_left:
        return [
            '     #########      ',
            '   #############    ',
            ' #################  ',
            ' #################  ',
            '################### ',
            '###    #####    ### ',
            '##      ###      ## ',
            '##      ###      ## ',
            ' ##    ## ##    ##  ',
            ' ### ###   ### ###  ',
            '  ###############   ',
            '   #############    ',
            '   ##  \\\\\\\\\  ##    ',
            '   ##  \\\\\\\\\  ##    ',
            '    ### ### ###     ',
            '     #########      ',
            '      #######       '
        ]
    else:
        return [
            '     #########     ',
            '   #############   ',
            ' ################# ',
            ' ################# ',
            '###################',
            '###    #####    ###',
            '##      ###      ##',
            '##      ###      ##',
            ' ##    ## ##    ## ',
            ' ### ###   ### ### ',
            '  ###############  ',
            '   #############   ',
            '   ##  /////  ##   ',
            '   ##  /////  ##   ',
            '    ### ### ###    ',
            '     #########     ',
            '      #######      '
        ]


def _draw_decoration(pic, x, y, color):
    CW.setForegroundColor(color)
    CW.drawCharArrayAtPosition(pic, x, y, True)


def draw_skull(x, y, color=(96, 96, 96), align_left=False):
    _draw_decoration(_get_skull_picture(align_left), x, y, color)