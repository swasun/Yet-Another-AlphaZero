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
