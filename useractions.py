import time

from kivy.uix.widget import Widget


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None



### Input on PC ###
def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    spacing = self.V_LINES_spacing * self.width
    if keycode[1] == 'left':
        # self.current_speed_x = self.SPEED_X
        if self.pos_counter > 1:
            self.pos_counter -= 1
            self.current_offset_x += spacing

        print(self.pos_counter)
    elif keycode[1] == 'right':
        # self.current_speed_x = - self.SPEED_X
        if self.pos_counter < self.V_numberof_LINES - 1:
            self.pos_counter += 1
            self.current_offset_x -= spacing
        print(self.pos_counter)

    # ## shooting
    # elif keycode[1] == 'up':
    #     self.runner_shoot()
    #     self.did_shoot = True

    return True



def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True

## Input on mobile ###
# def on_touch_down(self, touch):
#     if not self.state_game_over and self.state_game_has_started:
#         if touch.x < self.width/2:
#             # print("<-")
#             self.current_speed_x = self.SPEED_X
#         else:
#             # print("->")
#             self.current_speed_x = - self.SPEED_X
#     return super(Widget, self).on_touch_down(touch)
#     # if touch.x < self.width / 2:
#     #     # print("<-")
#     #     self.current_speed_x = self.SPEED_X
#     # else:
#     #     # print("->")
#     #     self.current_speed_x = - self.SPEED_X
#
# def on_touch_up(self, touch):
#     # print("Up")
#     self.current_speed_x = 0
#

def on_touch_move(self, touch):
    spacing = self.V_LINES_spacing * self.width
    if touch.x < touch.ox - 200:
        if self.pos_counter > 1 and not self.swiped:
            self.start = self.current_y_loop
            self.swiped = True
            self.pos_counter -= 1
            self.current_offset_x += spacing

        print(self.pos_counter)


    elif touch.x > touch.ox + 200:
        # self.current_speed_x = - self.SPEED_X
        if self.pos_counter < 5  and not self.swiped:
            self.start = self.current_y_loop
            self.swiped = True
            self.pos_counter += 1
            self.current_offset_x -= spacing
        print(self.pos_counter)

