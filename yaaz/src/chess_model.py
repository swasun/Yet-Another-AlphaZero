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

from chess_model_configuration import ChessModelConfiguration

from keras.optimizers import SGD
from keras.layers import Conv2D, Flatten, Input, Dense, BatchNormalization, ReLU, add
from keras.models import Model
from keras import regularizers

import numpy as np


class ChessModel(object):
    """
    Inspired from :
    https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning/blob/master/model.py
    http://discovery.ucl.ac.uk/10045895/1/agz_unformatted_nature.pdf (Mastering the Game of Go without Human Knowledge, DeepMind, 2017)
    """

    def __init__(self, configuration=ChessModelConfiguration()):
        self._configuration = configuration
        self._model = self._build()

    def predict(self, state):
        return self._model.predict_on_batch(state)

    def fit(self, state, labels):
        return self._model.fit(state, labels, epochs=1, verbose=1, validation_split=0, batch_size=1) 

    def save(self, path):
        self._model.save(path)

    def _residual_layer(self, input_block, filters, kernel_size):
        # 1. 2. 3.
        x = self._conv_layer(input_block, filters, kernel_size)

        # 4. A convolution of 256 filters of kernel size 3 x 3 with stride 1
        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format='channels_first',
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const)
        )(x)

        # 5. Batch normalisation
        x = BatchNormalization()(x)

        # 6. A skip connection that adds the input to the block
        x = add([input_block, x])

        # 7. A rectifier non-linearity
        x = ReLU()(x)

        return (x)

    def _conv_layer(self, x, filters, kernel_size):
        # 1. A convolution of 256 filters of kernel size 3 x 3 with stride 1
        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format="channels_first",
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const)
        )(x)

        # 2. Batch normalisation
        x = BatchNormalization()(x)

        # 3. A rectifier non-linearity
        x = ReLU()(x)

        return (x)

    def _value_head(self, x):

        # 1. A convolution of 1 filter of kernel size 1 x 1 with stride 1
        x = Conv2D(
            filters=1,
            kernel_size=(1, 1),
            data_format='channels_first',
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const)
        )(x)

        # 2. Batch normalisation
        x = BatchNormalization()(x)

        # 3. A rectifier non-linearity
        x = ReLU()(x)

        x = Flatten()(x)

        # 4. A fully connected linear layer to a hidden layer of size 256
        x = Dense(
            20,
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const)
        )(x)

        # 5. A rectifier non-linearity
        x = ReLU()(x)

        # 6. A fully connected linear layer to a scalar
        x = Dense(
            1,
            use_bias=False,
            activation='tanh', # 7. A tanh non-linearity outputting a scalar in the range [-1, 1]
            kernel_regularizer=regularizers.l2(self._configuration.reg_const),
            name='value_head',
        )(x)

        return (x)

    def _policy_head(self, x):

        # 1. A convolution of 2 filters of kernel size 1 x 1 with stride 1
        x = Conv2D(
            filters=2,
            kernel_size=(1, 1),
            data_format='channels_first',
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const)
        )(x)

        # 2. Batch normalization
        x = BatchNormalization()(x)

        # 3. A rectifier non-linearity
        x = ReLU()(x)

        x = Flatten()(x)

        """
        4. A fully connected linear layer that outputs a vector
        of size 8 * 8 * 73
        """
        x = Dense(
            self._configuration.output_dim,
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self._configuration.reg_const),
            name = 'policy_head'
        )(x)

        return (x)

    def _build(self):
        main_input = Input(shape=self._configuration.input_dim, name='main_input')

        x = self._conv_layer(
            main_input,
            self._configuration.hidden_layers[0]['filters'],
            self._configuration.hidden_layers[0]['kernel_size']
        )

        if len(self._configuration.hidden_layers) > 1:
            for h in self._configuration.hidden_layers[1:]:
                x = self._residual_layer(x, h['filters'], h['kernel_size'])

        ph = self._policy_head(x)
        vh = self._value_head(x)

        model = Model(inputs=[main_input], outputs=[ph, vh])
        model.compile(
            loss={'value_head': 'mean_squared_error', 'policy_head': 'categorical_crossentropy'},
            optimizer=SGD(lr=self._configuration.learning_rate, momentum=self._configuration.momentum),
            loss_weights={'value_head': 0.5, 'policy_head': 0.5}
        )

        return model
