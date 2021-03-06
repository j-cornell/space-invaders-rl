import sys
import gym
import vision
import reduction
import qagent
import pickle

def reduce_state(state):
	return reduction.ReducedState(vision.detect_player_x(state), vision.detect_bullets(state))

[filename_in, filename_out] = sys.argv[1].split(':')
rounds = 1
if len(sys.argv) > 2:
	rounds = int(sys.argv[2])

flags = set()
if len(sys.argv) > 3:
	flags = set(sys.argv[3])
flag_draw = 'd' in flags
flag_score = 'r' in flags
flag_freq = 'f' in flags
flag_impotent = 'i' in flags

table = None
freq = None
if filename_in:
	with open(filename_in, 'rb') as f:
		table = pickle.load(f)
		freq = pickle.load(f)

jim = gym.make('SpaceInvaders-v0')
initial_state = jim.reset()
if flag_draw:
	jim.render()

agent = qagent.QAgent(reduce_state(initial_state), table=table, freq=freq)

def do_round():
	total_reward = 0
	n_frames = 0
	done = False
	reduced_state = reduce_state(jim.reset())
	while not done:
		action = agent.act(reduced_state)
		real_action = action
		if flag_impotent:
			if action == 5:
				real_action = 3
			elif action == 1:
				real_action = 0
		(state, reward, done, _info) = jim.step(real_action)
		if flag_impotent:
			reward = n_frames/100.0
		reduced_state = reduce_state(state)
		agent.update(reduced_state, action, reward)
		total_reward += reward
		if flag_draw:
			jim.render()
		n_frames += 1
	return total_reward

def print_freq():
	freq = agent.get_freq()
	for f in sorted(freq, key=freq.__getitem__, reverse=True):
		print('{}\t{}'.format(freq[f], f))

for i in range(rounds):
	score = do_round()
	if flag_score:
		print(score)
	if filename_out:
		with open(filename_out, 'wb') as f:
			pickle.dump(agent.get_table(), f)
			pickle.dump(agent.get_freq(), f)

if flag_freq:
	print_freq()
