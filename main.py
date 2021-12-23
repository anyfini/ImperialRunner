import random

from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Ellipse, Rectangle, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget


Builder.load_file("menu.kv")

class MainWidget(Widget):
    from transforms import transform, transform_perspective, transform_2D
    from useractions import on_keyboard_up, on_keyboard_down, keyboard_closed, on_touch_move #, on_touch_down ,on_touch_up

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    ## Background change
    jungle_background = ObjectProperty()

    # For the vertical lines
    V_numberof_LINES = 6        # must be even number for clean middle
    V_LINES_spacing = 0.3       # percentage of screen
    vertical_lines = []

    # For the horizontal lines
    H_numberof_LINES = 8
    H_LINES_spacing = 0.1  # percentage of screen
    horizontal_lines = []

    # variables for the vertical movement
    current_offset_y = 0
    SPEED = 1                   # um speed zu ändern auch in der reset func ändern
    accelaration = 0.0002
    current_y_loop = 0

    # variables for the horizontal movement
    current_offset_x = 0
    SPEED_X = 1
    current_speed_x = 0
    pos_counter = V_numberof_LINES / 2
    swiped = False

    Numberof_TILES = 32
    tiles = []
    tiles_coordinates = []

    # runner variables:
    runner = None
    runner_radius = 0.05
    runner_default_y = 0.1
    runner_width = 0.15

    # bullet variables:
    bullet_size = 0.03
    bullet_speed = 3
    did_shoot = False
    counter = 0
    bullets = []

    state_game_over = False
    state_game_has_started = False

    menu_title = StringProperty("I  M  P  E  R  I  A  L     R  U  N  N  E  R")
    menu_button_title = StringProperty("START")

    score_txt = StringProperty()

    # Story
    Story = False
    my_story1 = StringProperty("")
    my_story2 = StringProperty("")
    my_story3 = StringProperty("")
    my_story4 = StringProperty("")
    my_story5 = StringProperty("")


    # Highscore
    Score = False
    highscores = [0,0,0,0]

    highscore1 = StringProperty("")
    first_place = 0
    highscore2 = StringProperty("")
    sec_place = 0
    highscore3 = StringProperty("")
    third_place = 0

    # difficulty
    hard_mode = False

    # background
    r = random.randint(0,3)
    if r == 0:
        displayed_image = 'images/bg2.jpg'
    elif r == 1:
        displayed_image = 'images/bg3.jpg'
    elif r == 2:
        displayed_image = 'images/bg4.jpg'
    elif r == 3:
        displayed_image = 'images/bg5.jpg'



    def __init__(self, **kwargs):                                                                                       ### From here on all for debuggin the perspective points ###
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_runner()
        self.reset_game()


        if self.is_desktop():
            # for the keyboard input on pc
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.score_txt = "SCORE: " + str(self.current_y_loop)
        self.pos_counter = self.V_numberof_LINES / 2
        self.swiped = False
        self.start = 0

        self.tiles_coordinates = []
        self.pre_file_tiles_coordinates()
        self.generate_tiles_coordinates()

        self.state_game_over = False

        if self.hard_mode:
            self.SPEED = 1.2
        else:
            self.SPEED = 0.8

    ### PC or Mobile ###
    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def runner_shoot(self):
        with self.canvas:
            Color(131/255,139/255,139/255)
            self.bullet = Ellipse()


    def bullet_shoot(self):

        self.bullets.append(1)
        base_y = self.runner_default_y * self.height
        bullet_half_width = self.bullet_size * self.width / 2
        self.bullet.size = bullet_half_width, bullet_half_width
        shooting_x, shooting_y = self.width / 2 - bullet_half_width / 2, base_y
        self.bullet.pos = shooting_x, shooting_y

    def bullet_movement(self):
        self.shooting_x, self.shooting_y = self.shooting_x, self.shooting_y + 10
        self.bullet.pos = self.transform(self.shooting_x, self.shooting_y)




    def init_runner(self):
        with self.canvas:
            Color(128/255,0,0)
            #x, y = self.transform(self.height * self.runner_default_y, self.width / 2)
            # self.runner = Triangle()
            self.runner = Ellipse()

    def update_runner(self):
        center_x = self.width / 2
        base_y = self.runner_default_y * self.height
        runner_half_width = self.runner_width * self.width / 2
        x1, y1 = self.transform(center_x - runner_half_width, base_y)
        x2, y2 = self.transform(center_x, base_y + runner_half_width)
        x3, y3 = self.transform(center_x + runner_half_width, base_y)
        #x4, y4 = self.transform(center_x + runner_half_width, base_y - runner_half_width)

        # self.runner.points = [x1, y1, x2, y2, x3, y3]
        self.runner.size = runner_half_width, runner_half_width
        self.pos = self.width / 2 - runner_half_width/ 2, base_y
        self.runner.pos = self.pos

    def check_runner_collision(self):
        for i in range(0,len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_runner_collision_with_tile(ti_x, ti_y):
                return True
        return False


    def check_runner_collision_with_tile(self, ti_x, ti_y):
        runner_x, runner_y = self.runner.pos
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        if xmin <= runner_x <= xmax and ymin <= runner_y <= ymax:
            return True
        else:
            return False

    def init_tiles (self):
        with self.canvas:
            Color(156/255,102/255,31/255, 0.7)
            for i in range(0, self.Numberof_TILES):
                self.tiles.append(Quad())

    def pre_file_tiles_coordinates(self):
        # 10 tiles all
        for i in range(0,10):
            self.tiles_coordinates.append((-1, i))
            self.tiles_coordinates.append((1, i))
            self.tiles_coordinates.append((0, i))


    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0

        # clean the coordinates that are out of the screen
        # ti_y < self.current_y_loop -> the tile that was at 0 is already out of the screen

        for i in range(len(self.tiles_coordinates) - 1, -1, -1):        # loop from the end to the start. -1 so we can get to 0 , the -1 so that we decrement
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]       # last element
            last_x = last_coordinates[0]            # weil wir gleiches x behalten keine 1
            last_y = last_coordinates[1] + 1        # +1 weil wir ein y weiter gehen

        print("foo1")


        for i in range(len(self.tiles_coordinates), self.Numberof_TILES):       # the first time len(self.tiles_coordinates) will be 0
            if self.hard_mode:
                r = random.randint(0, 2)
            else:
                r = random.randint(0, 3)

            # 0, 3 -> straight
            # 1 -> right
            # 2 -> left
            start_index = - int(self.V_numberof_LINES / 2) + 1
            end_index = start_index + self.V_numberof_LINES - 2
            if last_x <= start_index:
                r = random.randint(0,1)
                print("max rechts muss nach links")
            if last_x >= end_index:
                r = random.randint(2,3)
                print("max links muss nach rechts")


            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:                  # geht 1 nach oben ein nach rechts und 1 nach oben
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                print("Schritt nach rechts")
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            if r == 2:                  # geht 1 nach oben ein nach rechts und 1 nach oben
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            if r == 3 or r == 1:
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
                # last_y += 1
                # self.tiles_coordinates.append((last_x, last_y))



        print("foo2")


    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[self.width/2, 0, self.width/2, self.height])
            for i in range(0, self.V_numberof_LINES):
                self.vertical_lines.append(Line())


    def get_line_x_from_index(self, index):
        spacing = self.V_LINES_spacing * self.width
        central_line_x = self.perspective_point_x
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        start_index_y = 0
        spacing_y = self.H_LINES_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.Numberof_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            # 2     3
            #
            # 1     4
            x1, y1 = self.transform(xmin,ymin)
            x2, y2 = self.transform(xmin,ymax)
            x3, y3 = self.transform(xmax,ymax)
            x4, y4 = self.transform(xmax,ymin)



            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        # For 4 lines: -1, 0, 1, 2
        start_index = - int(self.V_numberof_LINES/2) + 1
        for i in range(start_index, start_index + self.V_numberof_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0,self.H_numberof_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = - int(self.V_numberof_LINES / 2) + 1
        end_index = start_index + self.V_numberof_LINES - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_numberof_LINES):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, deltatime):
        # print("delta time: " + str(deltatime * 60))
        time_factor = deltatime * 60  # so that the velosity increase is always happening at the same time
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_runner()


        if not self.state_game_over and self.state_game_has_started:

            # moving forward
            self.SPEED += self.accelaration
            #print("SPEEEEED: " + str(self.SPEED))
            speed_y = self.SPEED * self.height / 100     # so that the speed is independent of the window size
            #print("Speed: " + str(speed_y))
            self.current_offset_y += speed_y * time_factor

            # delay for the swiping
            if self.swiped:
                if self.start + 1 < self.current_y_loop:
                    print("Swipe wieder möglcih")
                    self.swiped = False

            # moving to the sides in a contineous way
            # speed_x = self.current_speed_x * self.width / 100   # so that the speed is independent of the window size
            # self.current_offset_x += speed_x * time_factor

            # for looping the vertical lines
            spacing_y = self.H_LINES_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "SCORE: " + str(self.current_y_loop)
                self.score = self.current_y_loop
                self.generate_tiles_coordinates()
                print("loop: " + str(self.current_y_loop))






        # # shooting
        # if self.did_shoot:
        #     bullet_speed_y = self.bullet_speed * self.height / 100
        #     self.current_bullet_offset = bullet_speed_y *time_factor
        #     self.bullet_shoot()
        #     self.counter += 1
        #     if self.counter >= 100:
        #         print("größer als 100")
        #         self.did_shoot = False
        #         self.counter = 0
        #         del self.bullets[0]



        if not self.check_runner_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "G A M E   O V E R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1
            print("Game over")
            print(self.width, self.height)

            # Highscore hinzufügen
            self.highscores.append(self.score)
            print("New Highscore: " + str(self.score))





    def on_menu_button_pressed(self):
        print("Button")
        self.reset_game()
        self.state_game_has_started = True
        self.hide_score()
        self.hide_story()
        self.menu_widget.opacity = 0


    def on_Story_button_pressed(self):
        print("Story Button")
        if not self.Story:
            self.Story = True
            self.my_story1 = "Das Imperiale Regime der Überwachung is überall, es gibt kein Entkommen. Jeder weiß das!"
            self.my_story2 = "Wenn du aus der Reihe tanzt, dich nicht an die Regeln hälst um deinen eigenen Instinkten "
            self.my_story3 = "und Träumen folgst, kommen die Wachen. Sie holen dich und du verschwindest! Aber was ist Leben ohne Träume und Hoffnung?"
            self.my_story4 = "Und du, du hast einen Traum, und du bist bereit den Menschen neue Hoffnung zu geben! Der Dschungel ist der Weg in die Freiheit!"
            self.my_story5 = "Run Beu, RUN!"
            print("reveal")
        else:
            self.hide_story()

    def hide_story(self):
        self.Story = False
        self.my_story1 = ""
        self.my_story2 = ""
        self.my_story3 = ""
        self.my_story4 = ""
        self.my_story5 = ""
        print("hide")

    def ranking_score(self):
        orderd_scores = []
        ranked_score = self.highscores.copy()
        if len(ranked_score) == 4:
            to_delete = ranked_score.index(min(ranked_score))
            del self.highscores[to_delete]

        self.first_place = max(ranked_score)
        orderd_scores.append(self.first_place)
        first_pos = ranked_score.index(max(ranked_score))
        del ranked_score[first_pos]

        self.sec_place = max(ranked_score)
        orderd_scores.append(self.sec_place)
        sec_pos = ranked_score.index(max(ranked_score))
        del ranked_score[sec_pos]

        self.third_place = max(ranked_score)
        orderd_scores.append(self.third_place)
        third_pos = ranked_score.index(max(ranked_score))
        del ranked_score[third_pos]






    def on_highscore_button_pressed(self):
        print("Button Highscore pressed")
        if not self.Score:
            self.ranking_score()
            self.highscore1 = "1. Platz: " + str(self.first_place)
            self.highscore2 = "2. Platz: " + str(self.sec_place)
            self.highscore3 = "3. Platz: " + str(self.third_place)
            self.Score = True
        else:
            self.hide_score()

    def hide_score(self):
        self.highscore1 = ""
        self.highscore2 = ""
        self.highscore3 = ""
        self.Score = False


    # switch for hard mode
    def on_switch_active(self, widget):
        #print("Switch: " + str(widget.active))
        self.hard_mode = widget.active


class ImperialRunnerApp(App):
    pass

ImperialRunnerApp().run()