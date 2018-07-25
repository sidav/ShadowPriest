from GLOBAL_DATA import Global_Constants as GC
import Routines.TdlConsoleWrapper as CW
import Routines.SidavRandom as RNG


def _determineXPosition(arr):
    ww = GC.CONSOLE_WIDTH
    if isinstance(arr, list):
        picw = len(arr[0])
        return int((ww - picw) * 0.5)
    elif isinstance(arr, str):
        picw = len(arr)
        return int((ww - picw)*0.47)


def _determineYPosition(arr):
    wh = GC.CONSOLE_HEIGHT
    pich = len(arr)
    return int((wh-pich)/3)


titlepic1 = \
    [
        "                           #######                           ",
        "                        #############                        ",
        "                       ###############                       ",
        "                     ###################                     ",
        "                     ###################                     ",
        "                    ######         ######                    ",
        "                    #####  1111111  #####                    ",
        "                    ####  111111111  ####                    ",
        "                    #### 11111111111 ####                    ",
        "                   ####  11111111111  ####                   ",
        "                   ###  1   11111   1  ###                   ",
        "  -==]- SHADOW     ##  1     111     1  ##      PRIEST -[==- ",
        "                  ### 111   11 11   111 ###                  ",
        "                  ###  111111   111111  ###                  ",
        "                  ###  111111   111111  ###                  ",
        "                  ####   1111 1 1111   ####                  ",
        "                 #######   1111111   #######                 ",
        "                 ####### 11 11111 11 #######                 ",
        "                  ###### 11       11 ######                  ",
        "                   #####  11     11  #####                   ",
        "                   ######  1111111  ######                   ",
        "                    ######  11111  ######                    ",
        "                     ######  111  ######                     "
    ]


def _drawTitlePic1():
    corner_x = _determineXPosition(titlepic1)
    corner_y = _determineYPosition(titlepic1)
    for y in range(len(titlepic1)):
        for x in range(len(titlepic1[y])):
            char = titlepic1[y][x]
            if char == '#':
                CW.setForegroundColor(96, 96, 128)
            elif char == '1':
                char = chr(206)
                CW.setForegroundColor(96, 96, 64)
            else:
                CW.setForegroundColor(96, 64, 128)
            CW.putChar(char, corner_x+x, corner_y+y)


titlepic2 = \
    [
        " @@@@ @  @@  @@@@  @@@@@   @@@@  @@ @@ @@     @@@@  @@@@@  @@ @@@@@  @@@@ @@@@",
        "!@    @  @@ @!  @@ @!  @@ @!  @@ @@ @! @@     @! @@ @!  @! @! @@    !@     @! ",
        " !@!  @!@!! @@!@!! @@  !! @@  !! @! !@ @!     @@!!  @@!!!  !@ @!!!   !@!   @! ",
        "   !! :  !! !:  !! !:  !! !!  !! !: !: !!     !:    !! :.  !: !!       !!  !: ",
        ":::   :   : :   :: ::,,:   ::.    :.  ::      .     :   :.  :  :::  ..:::  !  ",
    ]

def _drawTitlePic2():
    x = _determineXPosition(titlepic2)
    y = _determineYPosition(titlepic2)
    CW.setForegroundColor(220, 0, 0)
    CW.drawCharArrayAtPosition(titlepic2, x, y, True)


titlepic3 = \
    [
        "    :    #                                                 :!                 ",
        "@@###  :@           !@!           !                        #             : #  ",
        "@!  /@  @  #   @#     @@:     :   @#  !  :      :  !  ! :  :    :     !  !@@##",
        "@! /    @@@@#   !@@  @# @@  @:#@# :@! @#::@    !@@@@# @!# #@  #@ @# @@###  @# ",
        " @!#@!  @  @@  @ ##  @# !@  @  ##  @: @@ :@     @  @@ @*  !#  !@  # @! /   @# ",
        " /  @@  @  @@ @  ##  @# !@  @  #!  @: @@ :@     @  @@ @   !#  !@@   #@!#@! @# ",
        "@   @!  @  @@ @  #@  @# :@  @  #!  @: @@ :@     @  @# @   !#  #@  #  /  @! @# ",
        "#@@@#  #@# @# @@*#@! !@@#: :#@@@   #@@@@@#:    !@@@@  @@! !@# @@@#@ #@@@#  @@#",
        "                                                @                             ",
        "                                               !@#                            ",
    ]

def _drawTitlePic3():
    x = _determineXPosition(titlepic3)
    y = _determineYPosition(titlepic3)
    CW.setForegroundColor(132, 132, 104) #"pergament" color
    CW.drawCharArrayAtPosition(titlepic3, x, y, True)


def drawTitle():
    RNG.randomize()
    title = RNG.rand(3)+1
    #title = 1
    if title == 1:
        _drawTitlePic1()
    elif title == 2:
        _drawTitlePic2()
    elif title == 3:
        _drawTitlePic3()
    CW.setForegroundColor(132, 132, 104)
    pressanykey = "    Press ENTER"
    CW.putString(pressanykey, _determineXPosition(pressanykey), GC.CONSOLE_HEIGHT-2)

    CW.flushConsole()
    keypressed = CW.readKey()
    while (keypressed.key != "ENTER" and keypressed.text != ' '):
        if keypressed.key == 'F4':
            print('Oh fuck it\'s WRONG KEY OH CRAP')
            break
        keypressed = None #CW.readKey()
        keypressed = CW.readKey()
        print(keypressed.key)
        CW.flushConsole()
    print("Title screen successful.")