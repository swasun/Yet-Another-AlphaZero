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

from agent import Agent
from chess_env import ChessEnv
from environment import Environment
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
        current_best_model = self._dataset.load_best_model()
        agent1_victories = 0
        agent2_victories = 0
        draws = 0

        for epoch in range(self._environments_number):
            ConsoleLogger.status('[EVALUATOR] epoch #{}'.format(epoch))
            env = ChessEnv()
            agent1 = Agent(env, current_best_model)
            agent2 = Agent(env, self._new_model)
            environment = Environment(env, agent1, agent2)
            result = environment.run()
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
