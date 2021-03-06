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

from chess_model_configuration import ChessModelConfiguration

from keras.optimizers import SGD
from keras.layers import Conv2D, Flatten, Input, Dense, BatchNormalization, ReLU, add
from keras.models import Model, load_model
from keras import regularizers
from keras.callbacks import TensorBoard
import numpy as np
from time import time


class ChessModel(object):
    """
    Inspired from :
    https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning/blob/master/model.py
    http://discovery.ucl.ac.uk/10045895/1/agz_unformatted_nature.pdf (Mastering the Game of Go without Human Knowledge, DeepMind, 2017)
    """

    def __init__(self, model=None, configuration=ChessModelConfiguration(), build_model=True):
        self._configuration = configuration
        if model:
            self._model = model
        elif build_model:
            self._model = self._build()
        else:
            self._model = None

    def predict(self, state):
        return self._model.predict_on_batch(state)

    def fit(self, state, labels):
        return self._model.fit(
            state,
            labels,
            epochs=1,
            verbose=1,
            validation_split=0,
            batch_size=1,
            callbacks=[TensorBoard(log_dir="./model_logs", histogram_freq=0)]
        )

    def save(self, path):
        self._model.save(path)

    def clone(self):
        new_chess_model = ChessModel(build_model=False)
        self._model.save('temp.h5')
        new_chess_model._model = load_model('temp.h5')
        new_chess_model._configuration = self._configuration
        return new_chess_model

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
