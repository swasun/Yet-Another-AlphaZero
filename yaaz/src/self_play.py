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

from chess_env import ChessEnv
from environment_simulator import EnvironmentSimulator
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
                environment_simulator = EnvironmentSimulator(env, agent1, agent2)
                result = environment_simulator.run()
                environments.append(Dataset.environment_to_dict(result, agent1.policies, env.restore_and_get_actions()))
            self._dataset.record_environment(environments)

if __name__ == "__main__":
    dataset = Dataset(results_path='..' + os.sep + '..' + os.sep + 'results' + os.sep + 'chess')

    model = dataset.load_best_model()
    if model is None:
        model = ChessModel()

    self_play = SelfPlay(model, dataset)
    self_play.start()
