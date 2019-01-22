class Node(object):

    def __init__(self, edges, action, previous_edge):
        self._edges = edges
        self._action = action
        self._previous_edge = previous_edge
        self._edge_actions = list()

    @property
    def edges(self):
        return self._edges

    def set_edges(self, edges):
        self._edges = edges

    @property
    def action(self):
        return self._action

    @property
    def previous_edge(self):
        return self._previous_edge

    def set_previous_edge(self, previous_edge):
        self._previous_edge = previous_edge

    @property
    def edge_actions(self):
        return self._edge_actions

    def set_edge_actions(self, edge_actions):
        self._edge_actions = edge_actions

    def __repr__(self):
        return 'edges: {} action: {} previous_edge: {} edge_actions: {}'.format(
            self._edges, self._action, self._previous_edge, self._edge_actions
        )