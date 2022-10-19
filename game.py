import pygame as pg
from random import randrange
import config
from snake import Snake
from food import FoodManager


class Game:
    def __init__(self):
        self.sc = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.clock = pg.time.Clock()
        self.snake = Snake(
            (
                randrange(0, config.WINDOW_WIDTH, config.SIZE), 
                randrange(0, config.WINDOW_HEIGHT, config.SIZE)
            ),
            config.SIZE,
            config.STEP_LENGTH,
            config.SNAKE_COLOR
        )
        self.food_manager = FoodManager(
            (5, 5, config.WINDOW_WIDTH - 10, config.WINDOW_HEIGHT - 10),
            int(config.SIZE / 2),
            config.APPLES_QUANTITY
        )
        pg.display.set_caption('Snake')
        pg.init()
        self.font = pg.font.Font('Montserrat-Medium.ttf', 18)
        self.collect_sound = pg.mixer.Sound('sound/collect.mp3')
        self.game_over_sound = pg.mixer.Sound('sound/gameOver.wav')
        self.music = ('sound/track1.mp3', 'sound/track2.mp3', 'sound/track3.mp3', 'sound/track4.mp3')
        self.music_end_event = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.music_end_event)
        pg.mixer.music.load(self.music[0])
        pg.mixer.music.play()
        self.music_track = 1
    
    def render_score(self):
        score = self.font.render(f'score: {self.snake.length - 1}', 1, (255, 135, 68))
        self.sc.blit(score, (10, 5))

    def draw_frame(self):
        self.sc.fill(config.WINDOW_BACKGROUND)
        self.render_score()
        self.food_manager.draw_all(pg, self.sc)
        self.snake.draw(pg, self.sc)
        pg.display.update()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == ord('w'):
                    self.snake.set_direction('up')
                if event.key == ord('a'):
                    self.snake.set_direction('left')
                if event.key == ord('s'):
                    self.snake.set_direction('down')
                if event.key == ord('d'):
                    self.snake.set_direction('right')
            elif event.type == self.music_end_event:
                pg.mixer.music.load(self.music[self.music_track])
                pg.mixer.music.play()
                self.music_track = self.music_track + 1 if self.music_track < 3 else 0
            elif event.type == pg.QUIT:
                exit()

    def check_collision(self, actor, obstacle):
        top_side = actor[0] < obstacle[0]
        right_side = actor[1] > obstacle[1]
        bottom_side = actor[2] > obstacle[2]
        left_side = actor[3] < obstacle[3]
        return top_side and right_side and bottom_side and left_side

    def check_food(self):
        for apple in self.food_manager.food:
            if self.check_collision(self.snake.collision_box, apple.collision_box):
                self.food_manager.rnd_apple_state(apple)
                self.snake.grow()
                self.collect_sound.play()

    def check_tail_collision(self):
        if self.snake.length != len(set(self.snake.list)):
            self.game_over()

    def check_out_of_bounds(self):
        collision_box = self.snake.collision_box
        top_side = collision_box[0] < -5
        right_side = collision_box[1] > config.WINDOW_WIDTH + 5
        bottom_side = collision_box[2] > config.WINDOW_HEIGHT + 5
        left_side = collision_box[3] < -5
        if top_side or right_side or bottom_side or left_side:
            self.game_over()

    def screen_filter(self):
        sc_filter = pg.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        sc_filter.set_alpha(48)
        sc_filter.fill((67, 75, 96))
        self.sc.blit(sc_filter, (0, 0))

    def render_game_over_text(self):
        game_over_font = pg.font.Font('Montserrat-Medium.ttf', 30)
        text = game_over_font.render('Game Over', 1, (234, 83, 62))
        rect = text.get_rect(center=(config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2))
        self.sc.blit(text, rect)
        pg.display.update()
            
    def game_over(self):
        self.screen_filter()
        self.game_over_sound.play()
        pg.mixer.music.pause()
        self.render_game_over_text()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            self.clock.tick(config.FPS)

    def run(self):
        while True:
            self.snake.move()
            self.check_food()
            self.check_tail_collision()
            self.check_out_of_bounds()
            self.check_events()
            self.draw_frame()
            self.clock.tick(config.FPS)
