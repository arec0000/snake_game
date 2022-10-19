class Snake:
    def __init__(self, start_position, cell_size, step_length, color):
        self.list = [start_position]
        self.size = cell_size
        self.step_length = step_length
        self.color = color
        self.length = 1
        self._grow = False
        self._new_cell = None
        self.collision_box = (
            start_position[1], 
            start_position[0] + cell_size,
            start_position[1] + cell_size,
            start_position[0]
        )
        self._speed_x = 0
        self._speed_y = 0
        
    def set_direction(self, direction):
        if direction == 'up' and not self._speed_y == self.step_length:
            self._speed_x = 0
            self._speed_y = -self.step_length
        elif direction == 'right' and not self._speed_x == -self.step_length:
            self._speed_x = self.step_length
            self._speed_y = 0
        elif direction == 'down' and not self._speed_y == -self.step_length:
            self._speed_x = 0
            self._speed_y = self.step_length
        elif direction == 'left' and not self._speed_x == self.step_length:
            self._speed_x = -self.step_length
            self._speed_y = 0

    def move(self):
        # проходимся с конца до второго элемента и смещаем координаты
        for i in range(self.length - 1, 0, -1):
            self.list[i] = self.list[i - 1]
        # если нужно добавляем новый элемент
        if self._grow:
            self._grow = False
            self.length += 1
            self.list.append(self._new_cell)
        # смещаем голову
        head = self.list[0]
        x = head[0] + self._speed_x
        y = head[1] + self._speed_y
        self.list[0] = (x, y)
        # меняем кортеж для расчёта столкновений
        self.collision_box = (y, x + self.size, y + self.size, x)

    def grow(self):
        self._grow = True
        self._new_cell = (self.list[-1])

    def draw(self, pygame_obj, sc):
        for x, y in self.list:
            pygame_obj.draw.rect(sc, self.color, (x, y, self.size, self.size))
