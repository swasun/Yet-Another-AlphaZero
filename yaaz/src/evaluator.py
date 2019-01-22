from agent import Agent
from chess_env import ChessEnv
from environment import Environment
from error_handling.console_logger import ConsoleLogger


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

        for epoch in self._environments_number:
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
            ConsoleLogger.status('[EVALUATOR] agent1 it still has the best model')