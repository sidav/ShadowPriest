from . import LevelView as LV
from .Controllers import LevelController as LC
from Message_Log import MessageLog as LOG
from .Player import DeathScreen
from GLOBAL_DATA import Global_Constants as GC


def do_debug_key(keypressed):
    if keypressed.keychar == 'F12':
        GC.DEBUG_ENABLED ^= 1
        if GC.DEBUG_ENABLED:
            LOG.append_warning_message('Developer mode is enabled.')
        else:
            LOG.append_message('Developer mode is disabled. Have a good death!')
        return 
    if GC.DEBUG_ENABLED:
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

        elif keypressed.keychar == 'F7':
            DeathScreen.show_death_screen(None, True)

        elif keypressed.keychar == 'F8':
            GC.DEBUG_AI_DISABLED ^= 1
            if GC.DEBUG_AI_DISABLED:
                LOG.append_warning_message('All AIs lobotomized.')
            else:
                LOG.append_message('All AIs are now self-aware.')
    else:
        LOG.append_message('These commands are available only in developer mode.')
