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
