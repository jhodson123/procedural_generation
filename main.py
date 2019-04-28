import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

FILL_PERCENT = 45

FPS_LIMIT = 20


class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        if block_sight is None: block_sight = blocked
        self.block_sight = blocked


class Actor:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not map[self.x+dx][self.y+dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)


def make_map():
    global map

    map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if x == 0 or x == MAP_WIDTH-1 or y == 0 or y == MAP_HEIGHT-1:
                map[x][y].blocked = True
                map[x][y].block_sight = True
            else:
                num = tcod.random_get_int(0, 0, 100)
                if num <= FILL_PERCENT:
                    map[x][y].blocked = True
                    map[x][y].block_sight = True

    for i in range(5):
        reduce_noise()


def reduce_noise():
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if i+1 != MAP_WIDTH and j+1 != MAP_HEIGHT:
                wall_sum = 0
                if map[i-1][j-1].block_sight: wall_sum += 1
                if map[i-1][j].block_sight: wall_sum += 1
                if map[i-1][j+1].block_sight: wall_sum += 1
                if map[i][j-1].block_sight: wall_sum += 1
                if map[i][j+1].block_sight: wall_sum += 1
                if map[i+1][j-1].block_sight: wall_sum += 1
                if map[i+1][j].block_sight: wall_sum += 1
                if map[i+1][j+1].block_sight: wall_sum += 1

                if not map[i][j].block_sight:
                    if wall_sum >= 5:
                        map[i][j].block_sight = True
                        map[i][j].blocked = True
                else:
                    if wall_sum < 4:
                        map[i][j].block_sight = False
                        map[i][j].blocked = False


def render_all():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                tcod.console_set_char_background(con, x, y, tcod.dark_blue, tcod.BKGND_SET)
                tcod.console_put_char(con, x, y, '#', tcod.BKGND_NONE)
            else:
                tcod.console_set_char_background(con, x, y, tcod.black, tcod.BKGND_SET)
                tcod.console_put_char(con, x, y, '.', tcod.BKGND_NONE)

    for obj in objects:
        obj.draw()

    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def handle_keys():
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_ESCAPE:
        return True

    if key.vk == tcod.KEY_ENTER:
        make_map()

    if key.vk == tcod.KEY_UP:
        player.move(0, -1)
    elif key.vk == tcod.KEY_DOWN:
        player.move(0, 1)
    elif key.vk == tcod.KEY_LEFT:
        player.move(-1, 0)
    elif key.vk == tcod.KEY_RIGHT:
        player.move(1, 0)


player_x = SCREEN_WIDTH//2
player_y = SCREEN_HEIGHT//2

font_path = 'resources/arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font_path, font_flags)

window_title = 'Map Gen'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)

con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Actor(player_x, player_y, '@', tcod.white)
objects = [player]

make_map()

while not tcod.console_is_window_closed():
    render_all()

    tcod.console_flush()

    for obj in objects:
        obj.clear()
    exit = handle_keys()
    if exit:
        break
