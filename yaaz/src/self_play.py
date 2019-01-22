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

from chess_env import ChessEnv
from environment import Environment
from agent import Agent
from error_handling.console_logger import ConsoleLogger
from chess_model import ChessModel
from dataset import Dataset

import os


class SelfPlay(object):

    def __init__(self, model, dataset, iterations=1, epochs=2):
        self._model = model
        self._dataset = dataset
        self._iterations = iterations
        self._epochs = epochs

    def start(self):
        for iteration in range(self._iterations):
            ConsoleLogger.status('[SELF-PLAY] iteration: {}'.format(iteration))
            environments = list()
            for epoch in range(self._epochs):
                ConsoleLogger.status('[SELF-PLAY] epoch: {}'.format(epoch))
                env = ChessEnv()
                agent1 = Agent(env, self._model)
                agent2 = Agent(env, ChessModel())
                environment = Environment(env, agent1, agent2)
                result = environment.run()
                environments.append(Dataset.environment_to_dict(result, agent1.policies, env.restore_and_get_actions()))
            self._dataset.record_environment(environments)

if __name__ == "__main__":
    dataset = Dataset(results_path='..' + os.sep + '..' + os.sep + 'results' + os.sep + 'chess')

    model = dataset.load_best_model()
    if model is None:
        model = ChessModel()

    self_play = SelfPlay(model, dataset)
    self_play.start()
