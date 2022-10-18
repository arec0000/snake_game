class SnakeCell:
    def __init__(self, x, y, grow_steps = 0):
        self.x = x
        self.y = y
        self.grow_steps = grow_steps
        self.next = None


    def update_position(self, x, y):
        if self.grow_steps:
            self.grow_steps -= 1
            return self.x, self.y
        prev_x, prev_y = self.x, self.y
        self.x = x
        self.y = y
        return prev_x, prev_y


class SkeletonNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None


class Snake:
    def __init__(self, start_position, cell_size, step_length):
        self.head = SnakeCell(*start_position)
        self.size = cell_size
        self.step_length = step_length
        self.tail = self.head
        self.collision_actor = (
            start_position[1], 
            start_position[0] + cell_size,
            start_position[1] + cell_size,
            start_position[0]
        )
        self.length = 1
        self.dir_x = 0
        self.dir_y = 0
        self.skeleton_head = None
        self.skeleton_tail = None


    def set_direction(self, direction):
        if direction == 'up' and not self.dir_y == 1:
            self.dir_x = 0
            self.dir_y = -1
        elif direction == 'right' and not self.dir_x == -1:
            self.dir_x = 1
            self.dir_y = 0
        elif direction == 'down' and not self.dir_y == -1:
            self.dir_x = 0
            self.dir_y = 1
        elif direction == 'left' and not self.dir_x == 1:
            self.dir_x = -1
            self.dir_y = 0


    def move(self):
        cell = self.head
        x = cell.x + self.dir_x * self.step_length
        y = cell.y + self.dir_y * self.step_length
        self.collision_actor = (y, x + self.size, y + self.size, x)
        while cell != None:
            x, y = cell.update_position(x, y)
            cell = cell.next


    def grow(self):
        for i in range(1, 11):
            new_cell = SnakeCell(self.tail.x, self.tail.y, i)
            self.tail.next = new_cell
            self.tail = new_cell
        self.length += 1


    def skeleton_add(self):
        if self.head:
            self.tail = SkeletonNode(self.head.x, self.head.y)
        else:
            self.head = SkeletonNode(self.head.x, self.head.y)
            self.tail = self.head


    def draw(self, pg, sc):
        cell = self.head
        while cell != None:
            img = pg.image.load('circle.svg')
            rect = (cell.x, cell.y, self.size, self.size)
            sc.blit(img, rect)
            cell = cell.next
