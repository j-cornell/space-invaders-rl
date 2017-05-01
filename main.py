import sys
import gym
import vision
import reduction
import qagent
import pickle

draw = True

def reduce_state(state):
	return reduction.ReducedState(vision.detect_player_x(state), vision.detect_bullets(state))

jim = gym.make('SpaceInvaders-v0')
initial_state = jim.reset()
if draw:
	jim.render()

table = None
[filename_in, filename_out] = sys.argv[1].split(':')
rounds = 1
if len(sys.argv) > 2:
	rounds = int(sys.argv[2])

if filename_in:
	with open(filename_in, 'rb') as f:
		table = pickle.load(f)

agent = qagent.QAgent(reduce_state(initial_state), table=table)

def do_round():
	total_reward = 0
	done = False
	reduced_state = reduce_state(jim.reset())
	while not done:
		action = agent.act(reduced_state)
		(state, reward, done, _info) = jim.step(action)
		reduced_state = reduce_state(state)
		agent.update(reduced_state, action, reward)
		total_reward += reward
		if draw:
			jim.render()
	return total_reward

for i in range(rounds):
	score = do_round()
	print(score)
	if filename_out:
		with open(filename_out, 'wb') as f:
			pickle.dump(agent.get_table(), f)
