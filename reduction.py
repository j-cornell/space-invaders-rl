import vision
import math

ANGLE_RESOLUTION = 6
DISTANCE_RESOLUTION = 3

class ReducedState(object):
	"""
	A state reduced for use in Q-learning.
	Implements hashing and equality comparison for use as part of a dictionary key.
	"""

	def __init__(self, player_position, bullet_positions):
		self.player_position = reduce_player(player_position)
		positions = [DISTANCE_RESOLUTION] * ANGLE_RESOLUTION
		for pos in bullet_positions:
			radius, angle = reduce_bullet(pos, player_position)
			if angle != None:
				positions[angle] = min(positions[angle], radius)
		self.bullet_positions = tuple(positions)

	def __eq__(self, other):
		return self.player_position == other.player_position and self.bullet_positions == other.bullet_positions

	def __hash__(self):
		return hash((self.player_position, self.bullet_positions))

	def __str__(self):
		return str(tuple((self.player_position, self.bullet_positions)))

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
		"""
		Determines the standard position angle of a position with respect to the player (rounded)
		"""

		(x, y) = position
		x -= player_x
		y -= vision.PLAYER_Y
		quantized_angle = int((math.atan2(y, x) - math.pi/6) / (2*math.pi/3) * ANGLE_RESOLUTION)
		if quantized_angle < 0 or quantized_angle >= ANGLE_RESOLUTION:
			return None
		return quantized_angle

	def radius(position):
		"""
		Determines the radius separating the player and a position (scaled logarithmically and rounded)
		"""

		(x, y) = position
		max_radius = math.sqrt((vision.BULLET_X_MAX - vision.BULLET_X_MIN) ** 2 + (vision.BULLET_Y_MAX - vision.BULLET_Y_MIN) ** 2)
		radius = math.sqrt((x - player_x) ** 2 + (y - vision.PLAYER_Y) ** 2)
		return int(math.log(radius) / math.log(max_radius) * DISTANCE_RESOLUTION)
	
	return (radius(position), angle(position))
