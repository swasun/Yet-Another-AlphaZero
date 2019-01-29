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

from self_play import SelfPlay
from optimisation import Optimisation
from evaluator import Evaluator
from dataset import Dataset
from chess_model import ChessModel
from error_handling.console_logger import ConsoleLogger

import os


if __name__ == "__main__":
    epochs = 10
    dataset = Dataset(results_path='..' + os.sep + '..' + os.sep + 'results' + os.sep + 'chess')

    for epoch in range(epochs):
        ConsoleLogger.status('[MAIN] Epoch #{}'.format(epoch))

        # Get the best current model or create the first one
        ConsoleLogger.status('[MAIN] Loading best model...')
        model = dataset.load_best_model()
        if model is None:
            model = ChessModel()
        else:
            model = ChessModel(model=model)

        # Self play module
        ConsoleLogger.status('[MAIN] Starting self play...')
        SelfPlay(model, dataset).start()
        ConsoleLogger.success('[MAIN] Self play done')

        # Optimise (train) the model
        ConsoleLogger.status('[MAIN] Starting optimisation...')
        Optimisation(model, dataset).start()
        ConsoleLogger.success('[MAIN] Optimisation play done')

        # Evaluate the trained model with a copy. Evaluator will save it only if it's better
        ConsoleLogger.status('[MAIN] Starting evaluation...')
        Evaluator(dataset, model.clone(), environments_number=3).start()
        ConsoleLogger.success('[MAIN] Evaluation play done')
