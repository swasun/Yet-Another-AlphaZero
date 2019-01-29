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

class ChessModelConfiguration(object):

    def __init__(self, input_dim=(119, 8, 8), output_dim=73*8*8, hidden_layers=[ \
        {'filters':256, 'kernel_size':(3, 3)}, \
        {'filters':256, 'kernel_size':(3, 3)}, \
        {'filters':256, 'kernel_size':(3, 3)}, \
        {'filters':256, 'kernel_size':(3, 3)}, \
        {'filters':256, 'kernel_size':(3, 3)}, \
        {'filters':256, 'kernel_size':(3, 3)}
    ], reg_const=0.0001, learning_rate=0.1, momentum=0.9):

        self._input_dim = input_dim
        self._output_dim = output_dim
        self._hidden_layers = hidden_layers
        self._reg_const = reg_const
        self._learning_rate = learning_rate
        self._momentum = momentum

    @property
    def input_dim(self):
        return self._input_dim

    @property
    def output_dim(self):
        return self._output_dim

    @property
    def hidden_layers(self):
        return self._hidden_layers

    @property
    def reg_const(self):
        return self._reg_const

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def momentum(self):
        return self._momentum
