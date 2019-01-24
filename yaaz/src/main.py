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
