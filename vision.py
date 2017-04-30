import numpy

FRAME_WIDTH = 160
FRAME_HEIGHT = 210

PLAYER_Y = 185
PLAYER_X_MIN = 37
PLAYER_X_MAX = 119
PLAYER_COLOR = numpy.array([50, 132, 50], numpy.uint8)

BULLET_HEIGHT = 8
BULLET_X_MIN = 24
BULLET_X_MAX = 135
BULLET_Y_MIN = 0
BULLET_Y_MAX = PLAYER_Y
BULLET_COLOR = numpy.array([142, 142, 142], numpy.uint8)

def detect_player_x(state):
	for x in range(PLAYER_X_MIN, PLAYER_X_MAX):
		if (state[PLAYER_Y][x] == PLAYER_COLOR).all():
			return x
	return PLAYER_X_MIN

def detect_bullets(state):
	bullets = set()
	for y in range(0, FRAME_HEIGHT, BULLET_HEIGHT):
		for x in range(FRAME_WIDTH):
			if (state[y][x] == BULLET_COLOR).all():
				bullets.add((x, y))
	return bullets
