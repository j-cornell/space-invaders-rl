import reduction
import vision
import math
import random


#ACTIONS = up:2, down:5, fire:1, noop:0

alpha = 0.9
gamma = -0.5
TAU = 0.1

class QAgent(object):
    def __init__(self, state):
        self.old_state = state
        self.actions = [0, 1, 2, 5] #let 0 = noop, 1 = fire, 3 = right, 4 = left
        self.qtab = dict()
    
    def update(self, state, action, reward):
        old_key = (self.old_state, action)
        new_key = (state, action)
        if old_key in self.qtab:
            top_act = max(self.qtab[(state, self.actions[0])], self.qtab[(state, self.actions[1])], self.qtab[(state, self.actions[2])], self.qtab[(state, self.actions[3])])
            self.qtab[old_key] = (1-alpha)*self.qtab[old_key] + alpha*(reward + gamma * top_act)
        else:
            self.qtab[old_key] = reward
            
        self.old_state = state
    
    def act(self, state):
        limit = 0
        for act in self.actions:
            limit += (math.e ** self.qtab[(state, act)]) / TAU
        remaining = random.uniform(0, limit)
        for act in self.actions:
            remaining -= (math.e ** self.qtab[(state, act)])/TAU
            if remaining <= 0:
                return act
        raise Error("Couldn't choose an action")
