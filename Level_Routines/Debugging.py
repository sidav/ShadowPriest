from . import LevelView as LV
from .Controllers import LevelController as LC
from Message_Log import MessageLog as LOG


def do_debug_key(keypressed):
    if keypressed.keychar == 'F5':
        LV.DEBUG_RENDER_EVERYTHING ^= True
        LOG.append_warning_message('Debug rendering: {}'.format(str(LV.DEBUG_RENDER_EVERYTHING)))
        LC.force_redraw_screen(True)

    elif keypressed.keychar == 'F6':
        levelmodel = LC.current_level
        actors = levelmodel.get_all_units()
        for a in actors:
            if a.__class__.__name__ == 'Actor':
                a.set_current_state(a.states.calm)
        LOG.append_warning_message('All actor states have been reset.')
