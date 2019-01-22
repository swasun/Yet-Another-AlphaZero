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