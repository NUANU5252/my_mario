import game_framework
import pico2d

import start_state
import main_state

cavers_width = 48*16
cavers_height = 48*12
pico2d.open_canvas(cavers_width, cavers_height)
game_framework.run(start_state)
# game_framework.run(main_state)
pico2d.close_canvas()
