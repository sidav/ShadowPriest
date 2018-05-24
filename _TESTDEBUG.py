#import Overworld_Routines.OverworldView as OV

from Level_Routines.Controllers import LevelController as LC


#Following file is just a testing ground for any shit possible. It should not interfere with any other logic and should cause no problems when deleted.

def makeSomeTestCrap():
    # crap = Overworld(80, 21)
    # OV.drawOverworldMap(crap)

    # OW_Cont.initialize()
    # OW_Cont.control()

    # print(LOS.is_point_in_sector(5, 8, -1, 1, 5, 5, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 8, 10, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 2, 12, 90))

    # while(True):
    #     level = LM(80, 20)
    #     LV.draw_whole_level_map(level)
    #     CW.flushConsole()
    #     key = CW.readKey()
    #     while key.text != 'SPACE':
    #         key = CW.readKey()

    # print(MENU.single_select_menu("AHAHA MENU LOL", "Ahaha subheading lol", ['first', 'second', 'third']))
    # print(MENU.multi_select_menu("AHAHA MULTISELECT MENU LOL", "Ahaha subheading lol", ['first', 'second', 'third']))

    # a = Lockpick(3, 2)
    # solved = False
    # while not solved:
    #     CW.clearConsole()
    #     a.draw_puzzle(20, 5)
    #     CW.flushConsole()
    #     solved = a.do_turn()

    # A* TEST:
    map = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    def map_to_boolmap(somemap):
        boolmap = []
        for i in range(len(somemap)):
            column = []
            for j in range(len(somemap[0])):
                column.append(bool(somemap[i][j]))
            boolmap.append(column)
        return boolmap

    from Routines import AStarPathfinding
    asp = AStarPathfinding.AStarPathfinding(map, 1, 2, 4, 2)
    res = asp.findPath()
    for i in range(len(map)):
        print(map[i])

    for i in res:
        print(i.x, i.y)
    # /A* TEST

    # LC.initialize()
    # LC.control()
