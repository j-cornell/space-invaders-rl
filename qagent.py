import math
import random
import collections

#ACTIONS = up:2, down:5, fire:1, noop:0

alpha = 0.9
gamma = -0.5
TAU = 0.1

class QAgent(object):
	def __init__(self, state, table=None, freq=None):
		self.old_state = state
		self.actions = [0, 1, 2, 5] #let 0 = noop, 1 = fire, 3 = right, 4 = left
		if not table:
			table = collections.defaultdict(float)
		self.qtab = table
		if not freq:
			freq = collections.defaultdict(int)
		self.freq = freq

	def update(self, state, action, reward):
		old_key = (self.old_state, action)
		new_key = (state, action)
		top_act = max(self.qtab[(state, self.actions[0])], self.qtab[(state, self.actions[1])], self.qtab[(state, self.actions[2])], self.qtab[(state, self.actions[3])])
		self.qtab[old_key] = (1-alpha)*self.qtab[old_key] + alpha*(reward + gamma * top_act)
		self.old_state = state
		self.freq[state] += 1

	def act(self, state):
		# Softmax action choice
		limit = 0
		for act in self.actions:
			limit += (math.e ** self.qtab[(state, act)]) / TAU
		remaining = random.uniform(0, limit)
		for act in self.actions:
			remaining -= (math.e ** self.qtab[(state, act)])/TAU
			if remaining <= 0:
				return act
		raise Error("Couldn't choose an action")

	def get_table(self):
		return self.qtab
	
	def get_freq(self):
		return self.freq
