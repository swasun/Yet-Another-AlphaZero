 ###############################################################################
 # Copyright (C) 2019 Charly Lamothe                                           #
 #                                                                             #
 # This file is part of YetAnotherAlphaZero.                                   #
 #                                                                             #
 #   Licensed under the Apache License, Version 2.0 (the "License");           #
 #   you may not use this file except in compliance with the License.          #
 #   You may obtain a copy of the License at                                   #
 #                                                                             #
 #   http://www.apache.org/licenses/LICENSE-2.0                                #
 #                                                                             #
 #   Unless required by applicable law or agreed to in writing, software       #
 #   distributed under the License is distributed on an "AS IS" BASIS,         #
 #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
 #   See the License for the specific language governing permissions and       #
 #   limitations under the License.                                            #
 ###############################################################################

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
