import gym
import vision
import reduction
import qagent

def reduce_state(state):
	return reduction.ReducedState(vision.detect_player_x(state), vision.detect_bullets(state))

jim = gym.make('SpaceInvaders-v0')
state = jim.reset()
reduced_state = reduce_state(state)
jim.render()

agent = qagent.QAgent(state)
done = False

while not done:
	action = agent.act(reduced_state)
	(state, reward, done, _info) = jim.step(action)
	reduced_state = reduce_state(state)
	agent.update(reduced_state, action, reward)
	jim.render()

while True:
	pass
