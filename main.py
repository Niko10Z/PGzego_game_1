import pgzero.game
import pgzrun
from random import randint, choice as random_choice

from pgzero import music
from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.constants import mouse
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds

TITLE = "Tank battle"
WIDTH = 800
HEIGHT = 600
GAME_MODE = 0  # 0 - main menu, 1 - game
SOUND_ON = True  # False - sound off, True - sound on
LEVEL_NUM = 1
SCORE = 0
WINNER_SCORE = 10
bg_objects = []
bullet_objects = []
enemy_objects = []
smoke_animation = ('staff/smoke_grey0', 'staff/smoke_grey1', 'staff/smoke_grey2')
smoke_objects = []
explosion_animation = ('staff/smoke_yellow0', 'staff/smoke_yellow1', 'staff/smoke_yellow2', 'staff/smoke_yellow3')
explosion_objects = []
tracks_objects = []
walls_objects = []
box_objects = []


def fill_bg(img):
    global bg_objects
    y = 0
    while y < HEIGHT:
        x = 0
        while x < WIDTH:
            bg_objects.append((img, (x, y)))
            x += 128
        y += 128


def on_mouse_down(pos, button):
    """
    Вызывается при нажатии на кнопку мыши
    pos: кортеж (x, y) с координатами курсора
    button: номер кнопки
    """
    global button_start, button_sound, button_exit
    if GAME_MODE == 0:
        if button == mouse.LEFT:
            if button_start.collidepoint(pos):
                button_start.image = 'menu/button_main_menu_pressed'
            elif button_sound.collidepoint(pos):
                button_sound.image = 'menu/button_main_menu_pressed'
            elif button_exit.collidepoint(pos):
                button_exit.image = 'menu/button_main_menu_pressed'


def on_mouse_up(pos, button):
    """
    Вызывается при отпускании кнопки мыши
    pos: кортеж (x, y) с координатами курсора
    button: номер кнопки
    """
    global GAME_MODE, SOUND_ON, LEVEL_NUM, SCORE, button_start, button_sound, button_exit
    if GAME_MODE == 0:
        if button == mouse.LEFT:
            if button_start.collidepoint(pos):
                SCORE = 0
                LEVEL_NUM = 1
                new_game(LEVEL_NUM)
            elif button_sound.collidepoint(pos):
                SOUND_ON = not SOUND_ON
                if not SOUND_ON:
                    sounds.engine_no_move.stop()
                    sounds.engine_move.stop()
                    music.pause()
                else:
                    music.unpause()
            elif button_exit.collidepoint(pos):
                pgzero.game.exit()
            button_start.image = 'menu/button_main_menu'
            button_sound.image = 'menu/button_main_menu'
            button_exit.image = 'menu/button_main_menu'


def on_mouse_move(pos, rel, buttons):
    """
    Вызывается при отпускании кнопки мыши
    pos: кортеж (x, y) с координатами курсора в конце движения
    rel: кортеж (delta_x, delta_y) с величинами смещения курсора
    buttons: множество с номерами зажатых кнопок мыши
    """
    pass


def on_key_down(key, mod, unicode):
    """
    Вызывается при нажатии кнопки клавиатуры.
    key: номер нажатой клавиши
    mod: битовая маска с нажатиями клавиш-модификаторов
    unicode: печатаемый символ (если он есть у нажатой клавиши)

    ВАЖНО: эта функция обрабатывает только нажатие кнопки.
    Повторно срабатывает, только если клавишу отпустить и снова нажать.
    Обработку удержания клавиш нужно производить в функции update.
    """
    if key == keys.ESCAPE:
        if GAME_MODE == 1:
            end_game()
        elif GAME_MODE == 0:
            pgzero.game.exit()


def on_key_up(key, mod):
    """
    Вызывается при нажатии кнопки клавиатуры
    key: номер нажатой клавиши
    mod: битовая маска с нажатиями клавиш-модификаторов
    """
    pass


def on_music_end():
    """
    Вызывается при завершении музыкальной дорожки,
    если ее воспроизведение не зациклено
    """
    pass


def draw():
    for bg in bg_objects:
        screen.blit(bg[0], bg[1])
    if GAME_MODE == 0:
        button_start.draw()
        button_sound.draw()
        button_exit.draw()
        screen.draw.textbox('up, down, left, right => moving', (10, HEIGHT - 50, WIDTH, 20), color='black')
        screen.draw.textbox('space => shoot(reload = 3sec), ESC => exit', (10, HEIGHT - 25, WIDTH, 20), color='black')
    elif GAME_MODE == 1:
        for tracks in tracks_objects:
            tracks.draw()
        hero.draw()
        for wall in walls_objects:
            wall.draw()
        for box in box_objects:
            box.draw()
        for bull in bullet_objects:
            bull.draw()
        for enemy in enemy_objects:
            enemy.draw()
        for smoke in smoke_objects:
            smoke.draw()
        for explosion in explosion_objects:
            explosion.draw()
    screen.draw.textbox(f'Score: {SCORE}', (WIDTH - 150, 0, 150, 50), color='black')
    screen.draw.textbox(f'Sound: {"ON" if SOUND_ON else "OFF"}', (WIDTH - 150, 55, 150, 50), color='black')
    if LEVEL_NUM > WINNER_SCORE:
        screen.draw.textbox('YOU WIN!!!', (WIDTH / 2 - 100, 10, 200, 75), color='black')


def update():
    global GAME_MODE, LEVEL_NUM, WINNER_SCORE
    if GAME_MODE == 0:
        pass
    elif GAME_MODE == 1:
        if LEVEL_NUM > WINNER_SCORE:
            end_game()
        if len(enemy_objects) == 0:
            LEVEL_NUM += 1
            new_game(LEVEL_NUM)
        hero.process()
        for bull in bullet_objects:
            bull.process()
        for enemy in enemy_objects:
            enemy.process()


def end_game():
    global GAME_MODE
    bullet_objects.clear()
    enemy_objects.clear()
    smoke_objects.clear()
    tracks_objects.clear()
    GAME_MODE = 0


def new_game(enemies=1):
    global GAME_MODE, SOUND_ON, SCORE
    GAME_MODE = 1
    bullet_objects.clear()
    enemy_objects.clear()
    smoke_objects.clear()
    explosion_objects.clear()
    tracks_objects.clear()
    walls_objects.clear()
    box_objects.clear()
    hero.x = WIDTH / 2
    hero.y = HEIGHT - 100
    for _ in range(enemies):
        enemy = Enemy('enemy/tank_enemy_base', randint(0, WIDTH), randint(0, HEIGHT))
        while enemy.collidelist(enemy_objects) != -1 or \
                enemy.collidelist(walls_objects) != -1 or \
                enemy.collidelist(box_objects) != -1 or \
                enemy.colliderect(hero):
            enemy.x = randint(0, WIDTH)
            enemy.y = randint(0, HEIGHT)
        enemy_objects.append(enemy)
    for _ in range(randint(3, 7)):
        wall = Actor('staff/metal_box', (randint(0, WIDTH), randint(0, HEIGHT)))
        while wall.collidelist(enemy_objects) != -1 or \
                wall.collidelist(walls_objects) != -1 or \
                wall.collidelist(box_objects) != -1 or \
                wall.colliderect(hero):
            wall.x = randint(0, WIDTH)
            wall.y = randint(0, HEIGHT)
        walls_objects.append(wall)
    for _ in range(randint(3, 7)):
        box = Actor('staff/wood_box', (randint(0, WIDTH), randint(0, HEIGHT)))
        while box.collidelist(enemy_objects) != -1 or \
                box.collidelist(walls_objects) != -1 or \
                box.collidelist(box_objects) != -1 or \
                box.colliderect(hero):
            box.x = randint(0, WIDTH)
            box.y = randint(0, HEIGHT)
        box_objects.append(box)
    hero.reload()
    if SOUND_ON:
        sounds.start.play()


def animate_smoke():
    for smoke in smoke_objects:
        ind = smoke_animation.index(smoke.image) + 1
        if ind == len(smoke_animation):
            smoke_objects.remove(smoke)
            continue
        smoke.image = smoke_animation[ind]


def animate_explosion():
    for explosion in explosion_objects:
        ind = explosion_animation.index(explosion.image) + 1
        if ind == len(explosion_animation):
            explosion_objects.remove(explosion)
            continue
        explosion.image = explosion_animation[ind]


def animate_tracks():
    global tracks_objects
    if len(tracks_objects) > 0:
        tracks_objects.pop(0)


class Hero(Actor):
    def __init__(self, img):
        super().__init__(img)
        self.x = WIDTH / 2
        self.y = HEIGHT - 100
        self.angle = 0
        self.weapon_ready = True
        self.reloading_img = Actor('hero/reloading', self.center)
        clock.schedule_interval(self.smoke, 0.5)
        sounds.engine_no_move.set_volume(0.05)
        sounds.engine_move.set_volume(0.05)

    def process(self):
        global bullet_objects, tracks_objects, enemy_objects
        if self.collidelist(tracks_objects) == -1:
            tracks_objects.append(Actor('staff/tracks', self.center))
            tracks_objects[-1].angle = self.angle
            clock.schedule(animate_tracks, 3)
        if keyboard.left and self.x > 0:
            self.angle = 90
            self.x -= 2
        elif keyboard.right and self.x < WIDTH:
            self.angle = 270
            self.x += 2
        elif keyboard.up and self.y > 0:
            self.angle = 0
            self.y -= 2
        elif keyboard.down and self.y < HEIGHT:
            self.angle = 180
            self.y += 2
        if keyboard.space:
            if self.weapon_ready:
                self.weapon_ready = False
                if self.angle == 0:
                    x, y = self.x, self.top - 4
                elif self.angle == 90:
                    x, y = self.left - 4, self.y
                elif self.angle == 180:
                    x, y = self.x, self.bottom + 4
                elif self.angle == 270:
                    x, y = self.right + 4, self.y
                else:
                    x, y = self.x, self.y
                bullet_objects.append(Bullet('staff/bullet_base', x, y, self.angle))
                if SOUND_ON:
                    sounds.shot.play()
                clock.schedule_unique(self.reload, 3.0)
                self.animate_reloading()
        if self.collidelist(enemy_objects) != -1 or \
                self.collidelist(walls_objects) != -1 or \
                self.collidelist(box_objects) != -1:
            match self.angle:
                case 0:
                    self.y += 2
                case 90:
                    self.x += 2
                case 180:
                    self.y -= 2
                case 270:
                    self.x -= 2
                case _:
                    pass

    def animate_reloading(self):
        self.reloading_img.angle -= 90
        clock.schedule(self.animate_reloading, 0.1)

    def draw(self):
        super().draw()
        if not self.weapon_ready:
            match self.angle:
                case 0:
                    self.reloading_img.center = self.midtop
                case 90:
                    self.reloading_img.center = self.midleft
                case 180:
                    self.reloading_img.center = self.midbottom
                case 270:
                    self.reloading_img.center = self.midright
                case _:
                    self.reloading_img.center = self.center
            self.reloading_img.draw()

    def reload(self):
        self.weapon_ready = True
        clock.unschedule(self.animate_reloading)

    def smoke(self):
        global smoke_objects, smoke_animation
        smoke_objects.append(Actor(smoke_animation[0], self.center))


class Bullet(Actor):
    def __init__(self, img, gun_x, gun_y, gun_angle):
        super().__init__(img)
        self.x = gun_x
        self.y = gun_y
        self.angle = gun_angle

    def process(self):
        global GAME_MODE, LEVEL_NUM, SCORE, bullet_objects, enemy_objects, hero
        match self.angle:
            case 0:
                self.y -= 4
            case 90:
                self.x -= 4
            case 180:
                self.y += 4
            case 270:
                self.x += 4
            case _:
                bullet_objects.remove(self)
        if 0 < self.x < WIDTH and 0 < self.y < HEIGHT:
            collision = self.collidelist(enemy_objects)
            if collision != -1:
                dead_enemy = enemy_objects.pop(collision)
                try:
                    bullet_objects.remove(self)
                except ValueError:
                    pass
                explosion_objects.append(Actor(explosion_animation[0], dead_enemy.center))
                if SOUND_ON:
                    sounds.explosion_tank.play()
                SCORE += 1
            collision = self.collidelist(box_objects)
            if collision != -1:
                dead_box = box_objects.pop(collision)
                try:
                    bullet_objects.remove(self)
                except ValueError:
                    pass
                explosion_objects.append(Actor(explosion_animation[0], dead_box.center))
                if SOUND_ON:
                    sounds.explosion_tank.play()
            collision = self.collidelist(walls_objects)
            if collision != -1:
                try:
                    bullet_objects.remove(self)
                except ValueError:
                    pass
                explosion_objects.append(Actor(explosion_animation[0], self.center))
                if SOUND_ON:
                    sounds.explosion_tank.play()
            if len(self.collidelistall(bullet_objects)) > 1:
                if collision != bullet_objects.index(self):
                    bullet_objects.pop(collision)
                    try:
                        bullet_objects.remove(self)
                    except ValueError:
                        pass
                    explosion_objects.append(Actor(explosion_animation[0], self.center))
                    if SOUND_ON:
                        sounds.explosion_tank.play()
            if self.colliderect(hero):
                try:
                    bullet_objects.remove(self)
                except ValueError:
                    pass
                explosion_objects.append(Actor(explosion_animation[0], hero.center))
                if SOUND_ON:
                    sounds.explosion_tank.play()
                    sounds.lose.play()
                clock.schedule(end_game, 0.5)
        else:
            bullet_objects.remove(self)


class Enemy(Actor):
    def __init__(self, img, x, y):
        super().__init__(img)
        self.x = x
        self.y = y
        self.angle = 180
        self.weapon_ready = True
        self.choice = 5
        clock.schedule(self.think, 1)
        clock.schedule_interval(self.smoke, 0.5)
        sounds.engine_no_move.set_volume(0.05)
        sounds.engine_move.set_volume(0.05)

    def process(self):
        global hero, bullet_objects, tracks_objects
        if self.right < 0 or self.left > WIDTH or self.top > HEIGHT or self.bottom < 0:
            enemy_objects.remove(self)
            return
        if self.collidelist(tracks_objects) == -1:
            tracks_objects.append(Actor('staff/tracks', self.center, angle=self.angle))
            tracks_objects[-1].angle = self.angle
            clock.schedule(animate_tracks, 3)
        match self.choice:
            case 0:
                if self.weapon_ready:
                    self.weapon_ready = False
                    if self.angle == 0:
                        x, y = self.x, self.top - 4
                    elif self.angle == 90:
                        x, y = self.left - 4, self.y
                    elif self.angle == 180:
                        x, y = self.x, self.bottom + 4
                    elif self.angle == 270:
                        x, y = self.right + 4, self.y
                    else:
                        x, y = self.x, self.y
                    bullet_objects.append(Bullet('staff/bullet_base', x, y, self.angle))
                    if SOUND_ON:
                        sounds.shot.play()
            case 1:
                if self.y < HEIGHT and self.y < hero.y:
                    self.angle = 180
                    self.y += 1
                else:
                    if self.y == hero.y:
                        if self.x > hero.x:
                            self.choice = 4
                            self.angle = 90
                        else:
                            self.choice = 3
                            self.angle = 270
                    else:
                        self.choice = 2
                        self.angle = 0
                        self.y -= 1
            case 2:
                if self.y > 0 and self.y > hero.y:
                    self.angle = 0
                    self.y -= 1
                else:
                    if self.y == hero.y:
                        if self.x > hero.x:
                            self.choice = 4
                            self.angle = 90
                        else:
                            self.choice = 3
                            self.angle = 270
                    else:
                        self.choice = 1
                        self.angle = 180
                        self.y += 1
            case 3:
                if self.x < WIDTH and self.x < hero.x:
                    self.angle = 270
                    self.x += 1
                else:
                    if self.x == hero.x:
                        if self.y > hero.y:
                            self.choice = 0
                            self.angle = 0
                        else:
                            self.choice = 2
                            self.angle = 180
                    else:
                        self.choice = 4
                        self.angle = 90
                        self.x -= 1
            case 4:
                if self.x > 0 and self.x > hero.x:
                    self.angle = 90
                    self.x -= 1
                else:
                    if self.x == hero.x:
                        if self.y > hero.y:
                            self.choice = 0
                            self.angle = 0
                        else:
                            self.choice = 2
                            self.angle = 180
                    else:
                        self.choice = 3
                        self.angle = 270
                        self.x += 1
            case _:
                pass
        if len(self.collidelistall(enemy_objects)) > 1 or \
                self.colliderect(hero) or \
                self.collidelist(walls_objects) != -1 or \
                self.collidelist(box_objects) != -1:
            match self.angle:
                case 0:
                    self.y += 2
                    self.choice = random_choice([3, 4])
                case 90:
                    self.x += 2
                    self.choice = random_choice([1, 2])
                case 180:
                    self.y -= 2
                    self.choice = random_choice([3, 4])
                case 270:
                    self.x -= 2
                    self.choice = random_choice([1, 2])
                case _:
                    pass

    def think(self):
        self.weapon_ready = True
        if self.y == hero.y:
            if self.x > hero.x:
                self.angle = 90
                self.choice = 0
            else:
                self.angle = 270
                self.choice = 0
            clock.schedule(self.think, 3)
        elif self.x == hero.x:
            if self.y > hero.y:
                self.angle = 0
                self.choice = 0
            else:
                self.angle = 180
                self.choice = 0
            clock.schedule(self.think, 3)
        else:
            self.choice = randint(0, 5)  # 0 - shoot, 1, 2, 3, 4 - move, 5 - do nothing
            clock.schedule(self.think, randint(1, 5))

    def smoke(self):
        global smoke_objects, smoke_animation
        smoke_objects.append(Actor(smoke_animation[0], self.center))


class ImagedButton(Actor):
    def __init__(self, img, x, y, text='', margin=20, color='black'):
        super().__init__(img)
        self.x = x
        self.y = y
        self.text = text
        self.margin = margin
        self.color = color

    def draw(self):
        super().draw()
        screen.draw.textbox(self.text,
                            (self.left + self.margin/2, self.top + self.margin/2,
                             self.right - self.left - self.margin, self.bottom - self.top - self.margin),
                            color=self.color)


button_start = ImagedButton('menu/button_main_menu', WIDTH/2, HEIGHT/6, 'New game')
button_sound = ImagedButton('menu/button_main_menu', WIDTH/2, HEIGHT/2, 'Sound')
button_exit = ImagedButton('menu/button_main_menu', WIDTH/2, HEIGHT - HEIGHT/6, 'Exit')

hero = Hero('hero/tank_hero_base')
fill_bg('background/dirt')
clock.schedule_interval(animate_smoke, 0.2)
clock.schedule_interval(animate_explosion, 0.1)
music.set_volume(0.3)
music.play('soundtrack')
pgzrun.go()
