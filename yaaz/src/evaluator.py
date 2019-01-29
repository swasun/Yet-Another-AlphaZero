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

from agent import Agent
from chess_env import ChessEnv
from environment_simulator import EnvironmentSimulator
from error_handling.console_logger import ConsoleLogger
from chess_model import ChessModel
from dataset import Dataset

import os


class Evaluator(object):

    def __init__(self, dataset, new_model, environments_number=10):
        self._dataset = dataset
        self._new_model = new_model
        self._environments_number = environments_number

    def start(self):
        agent1_victories = 0
        agent2_victories = 0
        draws = 0

        # Load the best model or record the first one
        current_best_model = self._dataset.load_best_model()
        if current_best_model is None:
            self._dataset.record_model(self._new_model)
            return

        for epoch in range(self._environments_number):
            ConsoleLogger.status('[EVALUATOR] epoch #{}'.format(epoch))
            env = ChessEnv()
            agent1 = Agent(env, current_best_model)
            agent2 = Agent(env, self._new_model)
            environment_simulator = EnvironmentSimulator(env, agent1, agent2)
            result = environment_simulator.run()
            if result == "1-0":
                agent1_victories += 1
            elif result == "0-1":
                agent2_victories += 1
            else:
                draws += 1
            
        ConsoleLogger.success('[EVALUATOR] agent1 victories: {} agent2 victories: {} draws: {}'.format(
            agent1_victories, agent2_victories, draws
        ))

        if agent2_victories > agent1_victories:
            ConsoleLogger.success("[EVALUATOR] agent2's model is better - erase the previous one")
            self._dataset.erase_best_model(self._new_model)
        else:
            ConsoleLogger.status('[EVALUATOR] agent1 it still the best model')

if __name__ == "__main__":
    dataset = Dataset(results_path='..' + os.sep + '..' + os.sep + 'results' + os.sep + 'chess')
    new_model = ChessModel()

    evaluator = Evaluator(dataset, new_model, environments_number=3)
    evaluator.start()
