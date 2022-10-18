import pygame as pg
from random import randrange as rnd
import config
from snake import Snake
from apple import FoodManager

sc = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption('Snake')

pg.init()

snake = Snake(
    (rnd(0, config.WINDOW_WIDTH, config.SIZE), rnd(0, config.WINDOW_HEIGHT, config.SIZE)),
    config.SIZE,
    config.STEP_LENGTH
)

food_manager = FoodManager(
    (5, 5, config.WINDOW_WIDTH - 10, config.WINDOW_HEIGHT - 10),
    config.SIZE / 2,
    config.FOOD_COLOR,
    2
)

snake.grow()

def check_collision(actor, obstacle):
    top_side = actor[0] < obstacle[0]
    right_side = actor[1] > obstacle[1]
    bottom_side = actor[2] > obstacle[2]
    left_side = actor[3] < obstacle[3]
    return top_side and right_side and bottom_side and left_side



while True:
    sc.fill(config.WINDOW_BACKGROUND)
    food_manager.draw_all(pg, sc)
    snake.draw(pg, sc)
    
    pg.display.update()

    snake.move()

    for apple in food_manager.food:
        if check_collision(snake.collision_actor, apple.collision_obstacle):
            food_manager.rnd_apple_position(apple)
            snake.grow()


    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == ord('w'):
                snake.set_direction('up')
            if event.key == ord('a'):
                snake.set_direction('left')
            if event.key == ord('s'):
                snake.set_direction('down')
            if event.key == ord('d'):
                snake.set_direction('right')
        elif event.type == pg.QUIT:
            exit()

    clock.tick(config.FPS)
