import vision
import math

ANGLE_RESOLUTION = 6
DISTANCE_RESOLUTION = 3

class ReducedState(object):
	def __init__(self, player_position, bullet_positions):
		self.player_position = reduce_player(player_position)
		self.bullet_positions = frozenset(reduce_bullet(pos, player_position) for pos in bullet_positions)

	def __eq__(self, other):
		return self.player_position == other.player_position and self.bullet_positions == other.bullet_positions

	def __hash__(self):
		return hash((self.player_position, self.bullet_positions))

def reduce_player(position):
	if position < vision.PLAYER_X_MIN + 16:
		return -1
	elif position > vision.PLAYER_X_MAX - 16:
		return 1
	else:
		return 0
#	return int((position - vision.PLAYER_X_MIN) / (vision.PLAYER_X_MAX - vision.PLAYER_X_MIN) * 2 ** PLAYER_BITS)

def reduce_bullet(position, player_x):
	def angle(position):
		(x, y) = position
		return int(math.atan2(y - vision.PLAYER_Y, x - player_x) / math.pi * ANGLE_RESOLUTION)

	def radius(position):
		(x, y) = position
		max_radius = math.sqrt((vision.BULLET_X_MAX - vision.BULLET_X_MIN) ** 2 + (vision.BULLET_Y_MAX - vision.BULLET_Y_MIN) ** 2)
		radius = math.sqrt((x - player_x) ** 2 + (y - vision.PLAYER_Y) ** 2)
		return int(math.log(radius) / math.log(max_radius) * DISTANCE_RESOLUTION)
	
	return (radius(position), angle(position))
