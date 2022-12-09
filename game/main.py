import pyglet
from pyglet.window import Window, key
from pyglet.shapes import Rectangle

framerate = 60
step = 1 / framerate

width = 768
height = 576

gravity = 0.5
speed = 5
jump = 10

contentColor = (0, 191, 127)
playerColor = (255, 255, 0)

window = Window(width, height, "Platformer")
pyglet.gl.glClearColor(0.1, 0.125, 0.15, 1)
# window.set_mouse_visible(False)
keys = key.KeyStateHandler()
window.push_handlers(keys)


def rectangle(x, y, w, h, color=contentColor):
    return Rectangle(x, y, w, h, color)


player = rectangle(32, 32, 16, 16, playerColor)
player.vx = player.vy = 0

level = [
    # boundaries
    rectangle(0, -16, width, 16),
    rectangle(width, 0, 16, height),
    rectangle(0, height, width, 16),
    rectangle(-16, 0, 16, height),
    # borders
    rectangle(0, 0, 768, 16),
    rectangle(0, 560, 768, 16),
    rectangle(0, 0, 16, 576),
    rectangle(752, 0, 16, 576),
    # floors
    rectangle(336, 144, 16, 288),
    rectangle(352, 144, 336, 16),
    rectangle(418, 236, 336, 16),
    rectangle(352, 326, 336, 16),
    rectangle(464, 416, 112, 16),
    rectangle(640, 416, 112, 16),
    rectangle(576, 486, 64, 16),
    # platforms
    rectangle(80, 486, 64, 16),
    rectangle(208, 416, 64, 16),
    rectangle(80, 348, 64, 16),
    rectangle(208, 280, 64, 16),
    rectangle(80, 212, 64, 16),
    rectangle(208, 144, 64, 16),
    # stairs
    rectangle(448, 432, 16, 16),
    rectangle(432, 448, 16, 16),
    rectangle(416, 464, 16, 16),
    rectangle(400, 480, 16, 16),
    rectangle(384, 496, 16, 16),
    rectangle(368, 512, 16, 16),
    rectangle(352, 528, 16, 16),
    rectangle(336, 544, 16, 16),
    # walls
    rectangle(420, 80, 16, 64),
    rectangle(588, 80, 16, 64),
    rectangle(504, 16, 16, 64),
]


def intersect(a, b):
    return (
        a.x < b.x + b.width
        and b.x < a.x + a.width
        and a.y < b.y + b.height
        and b.y < a.y + a.height
    )


def translate(s, f):
    cx, cy = 0, 0
    dx, dy = s.vx, s.vy

    h = rectangle(s.x + dx, s.y, s.width, s.height)
    v = rectangle(s.x, s.y + dy, s.width, s.height)

    for t in f:

        if intersect(t, h):
            if dx < 0:
                dx = t.x + t.width - s.x
            else:
                dx = t.x - s.x - s.width

            cx = s.vx - dx

        if intersect(t, v):
            if dy < 0:
                dy = t.y + t.height - s.y
            else:
                dy = t.y - s.y - s.height

            cy = s.vy - dy

    return (dx, dy, cx, cy)


def update(dt):
    direction = 0

    if keys[key.F]:
        direction += 1
    if keys[key.S]:
        direction -= 1

    player.vx = speed * direction
    player.vy += gravity

    dx, dy, cx, cy = translate(player, level)

    player.vx = dx if cx == 0 else 0
    player.vy = dy if cy == 0 else 0

    if keys[key.E] and cy > 0:
        player.vy -= jump

    player.x += dx
    player.y += dy


def invert_draw(shape):
    y = shape.y
    shape.y = window.height - shape.height - shape.y
    shape.draw()
    shape.y = y


@window.event
def on_draw():
    window.clear()
    invert_draw(player)
    for tile in level:
        invert_draw(tile)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, step)
    pyglet.app.run()
