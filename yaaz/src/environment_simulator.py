 ###############################################################################
 # Copyright (C) 2019 Charly Lamothe                                           #
 #                                                                             #
 # This file is part of Yet-Another-AlphaZero.                                 #
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

from node import Node
from error_handling.console_logger import ConsoleLogger

import time


class EnvironmentSimulator(object):

    def __init__(self, env, agent1, agent2):
        self._env = env
        self._agent1 = agent1
        self._agent2 = agent2

    def run(self):
        start = time.clock()

        while not self._env.is_terminal():
            if self._env.is_almost_over():
                self._agent1.reduce_exploration_level()
                self._agent2.reduce_exploration_level()
                break
            
            if self._env.get_turn():
                action, policy = self._agent1.next_action()
                self._env.step(action)
                self._agent1.append_policy(policy)

                """
                Update the MCTS so that it still has the relevant
                part of the game tree for the next action.
                """
                if self._agent2.mcts.root.edges is not None:
                    if action in self._agent2.mcts.root.edge_actions:
                        self._update_mcts_root(self._agent2, action)
                    else:
                        self._agent2.mcts.set_root(Node(None, action, None))
                else:
                    self._agent2.mcts.set_root(Node(None, action, None))
            else:
                action, policy = self._agent2.next_action()
                self._agent2.append_policy(policy)
                self._env.step(action)

                if action in self._agent1.mcts.root.edge_actions:
                    self._update_mcts_root(self._agent1, action)
                else:
                    self._agent1.mcts.set_root(Node(None, action, None))

        result = self._env.get_result()

        ConsoleLogger.success("The epoch ended in {}s with the score {} at turn {} due to reason '{}'.".format(
            time.clock() - start, result, self._env.get_turn_number(), self._env.get_ending_reason()))

        return result

    def _update_mcts_root(self, agent, action):
        agent.mcts.set_root(agent.mcts.root.edges[agent.mcts.root.edge_actions.index(action)].next_node)
        agent.mcts.root.previous_edge.set_next_node(None)
        agent.mcts.root.set_previous_edge(None)
