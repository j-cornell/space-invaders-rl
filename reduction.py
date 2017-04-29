import vision
import math

PLAYER_BITS = 3
BULLET_BITS = 16

class ReducedState(object):
	def __init__(self, player_position, bullet_positions):
		self.player_position = reduce_player(player_position)
		self.bullet_positions = set(reduce_bullet(pos, player_position) for pos in bullet_positions)

	def __eq__(self, other):
		return self.player_position == other.player_position and self.bullet_positions == other.bullet_positions

	def __hash__(self):
		return hash((self.player_position, self.bullet_positions))

def reduce_player(position):
	return int((position - vision.PLAYER_X_MIN) / (vision.PLAYER_X_MAX - vision.PLAYER_X_MIN) * 2 ** PLAYER_BITS)

def reduce_bullet(position, player_x):
	resolution = int(math.sqrt(BULLET_BITS))

	def angle(position):
		(x, y) = position
		return int(math.atan2(y - vision.PLAYER_Y, x - player_x) / math.pi * resolution)

	def radius(position):
		(x, y) = position
		max_radius = math.sqrt((vision.BULLET_RIGHT - vision.BULLET_LEFT) ** 2 + (vision.BULLET_TOP - vision.BULLET_BOTTOM) ** 2)
		radius = math.sqrt((x - player_x) ** 2 + (y - vision.PLAYER_Y) ** 2)
		return int(math.log(radius) / math.log(max_radius) * resolution)
	
	return (radius(position), angle(position))
