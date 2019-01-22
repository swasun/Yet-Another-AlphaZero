from mcts import MCTS


class Agent(object):

    def __init__(self, env, model):
        self._env = env
        self._model = model
        self._mcts = MCTS(self._env, 100, 0, self._model)
        self._policies = list()

    @property
    def mcts(self):
        return self._mcts

    def next_action(self):
        return self._mcts.search()

    def reduce_exploration_level(self):
        self._mcts.set_temperature(0.5)

    @property
    def policies(self):
        return self._policies

    def append_policy(self, policy):
        self._policies.append(policy)
