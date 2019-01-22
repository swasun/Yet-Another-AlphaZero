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

from chess_model import ChessModel
from dataset import Dataset
from error_handling.console_logger import ConsoleLogger
from chess_env import ChessEnv

import os
import numpy as np
import random


class Optimisation(object):

    def __init__(self, model, dataset):
        self._model = model
        self._dataset = dataset

    def start(self):
        environment_batches = self._dataset.load_n_last_environment_batches(1)
        losses = list()

        for environment_batch in environment_batches:
            mini_batch = []
            values = []
            policies = []
            actual_policies = []
            for environment in environment_batch:
                env = ChessEnv()
                result = environment['result']
                if result == '1/2-1/2':
                    values += [[-1.0]]
                elif result == '1-0':
                    values += [[1.0]]
                else:
                    values += [[-1.0]]
                policies += environment['policies']
                actions = environment['actions']
                if len(actions) % 2 > 0:
                    action = random.randint(0, (len(actions) - 3) / 2)
                else:
                    action = random.randint(0, (len(actions) - 2) / 2)
                for i in range(0, action):
                    env._board.push(actions[2 * i])
                    env._board.push(actions[(2 * i) + 1])
                state = env.build_state(T=8)
                mini_batch += [state]
                probabilities = np.zeros((73, 8, 8))
                actual_probabilities = env.filter_illegal_probabilities(probabilities, is_training=True, q=policies[action])
                actual_probabilities = np.ndarray.flatten(actual_probabilities)
                actual_policies += [actual_probabilities]

            for i in range(len(environment_batch)):
                labels = {'policy_head': np.reshape(actual_policies[i], (1, 4672)), 'value_head': np.array(values[i])} 
                history = self._model.fit(mini_batch[i], labels)
                losses += [history.history['loss']]
            print(np.mean(losses))
            self._dataset.record_model(self._model)

if __name__ == "__main__":
    dataset = Dataset(results_path='..' + os.sep + '..' + os.sep + 'results' + os.sep + 'chess')
    model = dataset.load_best_model()
    if model is None:
        model = ChessModel()

    optimisation = Optimisation(model, dataset)
    optimisation.start()
    