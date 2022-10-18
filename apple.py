from random import randrange

class Apple:
    def __init__(self, position, size, color = (255, 0, 0)):
        self.position = position
        self.size = size
        self.collision_obstacle = (
            position[1] + size,
            position[0],
            position[1],
            position[0] + size
        )
        self.color = color


    def draw(self, pygame_obj, screen):
        pygame_obj.draw.rect(screen, self.color, (*self.position, self.size, self.size))


    def update_position(self, position):
        self.position = position
        self.collision_obstacle = (
            position[1] + self.size,
            position[0],
            position[1],
            position[0] + self.size
        )

class FoodManager:
    def __init__(self, field, size, color, start_quantity = 0):
        self.field = field
        self.size = size
        self.color = color
        self.quantity = 0
        self.food = []
        for _ in range(start_quantity):
            self.add_apple()


    def add_apple(self):
        self.food.append(Apple(self.get_random_position(), self.size, self.color))
        self.quantity += 1
    

    def rnd_apple_position(self, apple):
        apple.update_position(self.get_random_position())


    def draw_all(self, pygame_obj, screen):
        for apple in self.food:
            apple.draw(pygame_obj, screen)

    
    def get_random_position(self):
        return (
            randrange(self.field[0], self.field[2], self.size), 
            randrange(self.field[1], self.field[3], self.size)
        )
