 #####################################################################################
 # MIT License                                                                       #
 #                                                                                   #
 # Copyright (C) 2019 Charly Lamothe                                                 #
 #                                                                                   #
 # This file is part of YetAnotherAlphaZero.                                         #
 #                                                                                   #
 #   Permission is hereby granted, free of charge, to any person obtaining a copy    #
 #   of this software and associated documentation files (the "Software"), to deal   #
 #   in the Software without restriction, including without limitation the rights    #
 #   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       #
 #   copies of the Software, and to permit persons to whom the Software is           #
 #   furnished to do so, subject to the following conditions:                        #
 #                                                                                   #
 #   The above copyright notice and this permission notice shall be included in all  #
 #   copies or substantial portions of the Software.                                 #
 #                                                                                   #
 #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
 #   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
 #   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     #
 #   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          #
 #   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
 #   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   #
 #   SOFTWARE.                                                                       #
 #####################################################################################

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