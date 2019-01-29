 #####################################################################################
 # MIT License                                                                       #
 #                                                                                   #
 # Copyright (C) 2019 Charly Lamothe                                                 #
 #                                                                                   #
 # This file is part of Yet-Another-AlphaZero.                                       #
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

class Edge(object):

    def __init__(self, a, p, previous_node, next_node):
        self._a = a
        self._n = 0
        self._w = 0
        self._q = 0
        self._p = p
        self._previous_node = previous_node
        self._next_node = next_node

    @property
    def n(self):
        return self._n

    def incremente_n(self):
        self._n += 1

    @property
    def w(self):
        return self._w

    def set_w(self, w):
        self._w = w

    @property
    def q(self):
        return self._q

    def set_q(self, q):
        self._q = q

    @property
    def p(self):
        return self._p

    @property
    def previous_node(self):
        return self._previous_node

    @property
    def next_node(self):
        return self._next_node

    def set_next_node(self, next_node):
        self._next_node = next_node

    def __repr__(self):
        return 'a: {} n: {} w: {} q: {} p: {}'.format(
            self._a, self._n, self._w, self._q, self._p
        )
