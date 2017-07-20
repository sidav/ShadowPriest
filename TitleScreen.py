import Routines.ConsoleWrapper as CW
import ShadowPriest as Main
import Routines.SidavRandom as RNG


def _determineXPosition(arr):
    ww = Main.CONSOLE_WIDTH
    picw = len(arr[0])
    return int((ww-picw)/2)

def _determineYPosition(arr):
    wh = Main.CONSOLE_HEIGHT
    pich = len(arr)
    return int((wh-pich)/3)


titlepic1 = \
    [
        "                         o+ommmy++:                      ",
        "                     +mdmmmmmmmmmmms+                    ",
        "                   +mmmmmmmmmmmmmmmmmm.                  ",
        "                  hmmmmmmmmmmmmmmmmmmmm-                 ",
        "                 smmmmmmmmmmmmmmmmmmmmmm                 ",
        "                 mmmmmmmmmmmmmmmmmmmmmmdo                ",
        "                 mmmmmmmmmmmmmmmmmmmmmmmN                ",
        "                 dmmmmmdmd+++++smmmmmmmmm                ",
        "                 mmmmm+o+hmmmmmm+++sdmmmN                ",
        "-==|- SHADOW     mmm++ommdmmmmmdmmys.mmdh    PRIEST -|==-",
        "                ymmh+h.   /mmmm\   .m mmm                ",
        "                mmdysmmdmmmmmmmmmmmmm mmmm               ",
        "               mmmmm`+oo/.``..``-+o+/hmmmd+              ",
        "              ymmmmmm`.............`ommmmmm              ",
        "              :mmmmmm ............. dmmmmmm              ",
        "               ommmmN ..............-mmmmm               ",
        "                hmmmmd+`.........``+mmmmm.               ",
        "                 +mmmmmm+`.....``+mmmmms+                ",
        "                   -+++++o......++++++                   ",
    ]


def _drawTitlePic1():
    x = _determineXPosition(titlepic1)
    y = _determineYPosition(titlepic1)
    CW.setForegroundColor(96, 96, 128)
    CW.drawCharArrayAtPosition(titlepic1, x, y, True)


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
        "@! /    @@@@#   !@@  @# @@  @ #@# :@! @#::@    !@@@@# @!# #@  #@ @# @@###  @# ",
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
    CW.setForegroundColor(128, 128, 96)
    CW.drawCharArrayAtPosition(titlepic3, x, y, True)


def drawTitle():
    RNG.randomize()
    title = 1#RNG.rand(3)+1
    if title == 1:
        _drawTitlePic1()
    elif title == 2:
        _drawTitlePic2()
    elif title == 3:
        _drawTitlePic3()