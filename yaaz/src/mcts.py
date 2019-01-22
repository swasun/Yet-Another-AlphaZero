from node import Node
from edge import Edge
from error_handling.console_logger import ConsoleLogger

import time
import numpy as np
from math import sqrt


class MCTS(object):

    def __init__(self, env, simulations, turn, model, temperature=1):
        self._env = env
        self._simulations = simulations
        self._turn = turn
        self._model = model
        self._temperature = temperature
        if self._env.get_action_stack() != []:
            self._root = Node(None, self._env.get_last_action(), None)
        else:
            self._root = Node(None, "", None)
    
    def set_temperature(self, temperature):
        self._temperature = temperature

    @property
    def root(self):
        return self._root

    def set_root(self, root):
        self._root = root

    def search(self):
        start = time.clock()
        env = self._env.copy()

        for _ in range(self._simulations):
            current_node = self._root
            depth = 0
            turn = 1
            # Search until an unexplored node is found or depth is reached
            while current_node.edges is not None and current_node.edges != [] and depth < 6:
                depth += 1
                turn *= -1
                action = self._select(current_node)
                current_node = self._expand(env, current_node, action)
            probabilities, value = self._evaluate(env)
            turn = self._backup(env, current_node, probabilities, value, turn)

            while depth != 0:
                turn *= -1
                depth -= 1
                env.backward()

        best_action = self._compute_best_action()
        
        ConsoleLogger.status('[MCTS SEARCH] Elapsed time: {}s to select action {}'.format(time.clock() - start, best_action[0]))

        return best_action

    def _select(self, current_node, c_puct=1):
        noise = np.random.dirichlet([.03] * len(current_node.edges))
        actions = []
        visit_count = 0

        for i in range(len(current_node.edges)):
            visit_count += current_node.edges[i].n
        
        for i in range(len(current_node.edges)):
            visit_proportion = sqrt(visit_count) / (1 + current_node.edges[i].n)
            q = current_node.edges[i].q # Exploitation
            if current_node is self._root:
                u = c_puct * ((current_node.edges[i].p * .66) + (.33 * noise[i])) * visit_proportion # Exploration
            else:
                u = c_puct * current_node.edges[i].p * visit_proportion # Exploration
            actions += [q + u]
        
        return actions.index(max(actions))

    def _expand(self, env, current_node, action):
        next_edge = current_node.edges[action]
        current_node = next_edge.next_node
        env.step(current_node.action)
        return current_node

    def _evaluate(self, env):
        state = env.build_state()
        probabilities, value = self._model.predict(state)
        value = value[0][0]
        probabilities = probabilities[0].reshape(73, 8, 8)
        
        probabilities = env.filter_illegal_probabilities(probabilities, is_training=False, q=None)
        return probabilities, value

    def _backup(self, env, current_node, probabilities, value, turn):
        edges = list()
        legal_actions = env.get_legal_actions()

        for i in range(len(legal_actions)):
            edges += [Edge(legal_actions[i], probabilities[i], current_node, None)]
            next_action = str(legal_actions[i])
            edges[i].set_next_node(Node(None, next_action, edges[i]))
            current_node.set_edge_actions([str(action) for action in legal_actions])
        current_node.set_edges(edges)
        
        # Update edges
        while current_node.previous_edge is not None:
            turn = turn * -1
            edge = current_node.previous_edge
            edge.incremente_n()
            edge.set_w(edge.w + (value * turn))
            edge.set_q(edge.w / edge.n)
            current_node = edge.previous_node

        return turn

    def _compute_best_action(self):
        policy = []
        edges = self._root.edges
        visit_count = 0

        for i in range(len(edges)):
            visit_count += edges[i].n ** (1 / self._temperature)

        for i in range(len(edges)):
            policy += [(edges[i].n ** (1 / self._temperature)) / visit_count]

        next_root = edges[policy.index(max(policy))].next_node
        action = next_root.action
        self._root = next_root
        self._root.previous_edge.set_next_node(None)
        self._root.set_previous_edge(None)

        return action, policy
