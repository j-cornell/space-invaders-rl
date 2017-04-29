import numpy

frame_width = 160
frame_height = 210f

player_y = 185

player_x_min = 37
player_x_max = 119
player_x_range = player_x_max - player_x_min - 1

player_color = numpy.array([50, 132, 50], numpy.uint8)

bullet_height = 8
bullet_color = numpy.array([142, 142, 142], numpy.uint8)

def detect_player_x(state):
	for x in range(player_x_min, player_x_range):
		if (state[player_y][x] == player_color).all():
			return x
	return None

def detect_bullets(state):
	bullets = set()
	for y in range(0, frame_height, bullet_height):
		for x in range(frame_width):
			if (state[y][x] == bullet_color).all():
				bullets.add((x, y))
	return bullets
