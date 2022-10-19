from random import randrange


class Apple:
    def __init__(self, position, size, color=(255, 0, 0)):
        self.position = position
        self.size = size
        self.collision_box = (
            position[1] + size,
            position[0],
            position[1],
            position[0] + size
        )
        self.color = color

    def update(self, position, color):
        self.position = position
        self.color = color
        self.collision_box = (
            position[1] + self.size,
            position[0],
            position[1],
            position[0] + self.size
        )

    def draw(self, pygame_obj, screen):
        pygame_obj.draw.rect(screen, self.color, (*self.position, self.size, self.size))


class FoodManager:
    def __init__(self, field, size, start_quantity=0):
        self.field = field
        self.size = size
        self.quantity = 0
        self.food = []
        for _ in range(start_quantity):
            self.add_apple()

    def add_apple(self):
        self.food.append(Apple(self.get_random_position(), self.size, self.get_random_color()))
        self.quantity += 1

    def rnd_apple_state(self, apple):
        apple.update(self.get_random_position(), self.get_random_color())

    def get_random_position(self):
        return (
            randrange(self.field[0], self.field[2], self.size),
            randrange(self.field[1], self.field[3], self.size)
        )

    def get_random_color(self):
        return (randrange(160, 255, 1), randrange(160, 255, 1), randrange(160, 255, 1))

    def draw_all(self, pygame_obj, screen):
        for apple in self.food:
            apple.draw(pygame_obj, screen)
