 ###############################################################################
 # Copyright (C) 2019 Charly Lamothe                                           #
 #                                                                             #
 # This file is part of YetAnotherAlphaZero.                                   #
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

from error_handling.console_logger import ConsoleLogger

import chess
import numpy as np


class ChessEnv(object):

    _piece_values = {
        'p': 0, 'b': 1, 'n': 2, 'r': 3,
        'q': 4, 'k': 5, 'P': 6, 'B': 7,
        'N': 8, 'R': 9, 'Q': 10, 'K': 11
    }

    def __init__(self):
        self._board = chess.Board()

    def step(self, action):
        self._board.push_uci(action)

    def get_legal_actions(self):
        return list(self._board.legal_moves)

    def is_terminal(self):
        return self._board.is_game_over()

    def get_result(self):
        result = self._board.result()
        if result == '*':
            result = '1/2-1/2'
        return result

    def get_turn(self):
        return self._board.turn

    def is_almost_over(self):
        return self._board.fullmove_number > 80

    def get_action_stack(self):
        return self._board.move_stack

    def restore_and_get_actions(self):
        moves = []

        while len(self._board.move_stack) > 0:
            moves = [self._board.pop()] + moves
        
        return moves

    def get_last_action(self):
        return self._board.peek()

    def get_turn_number(self):
        return self._board.fullmove_number

    def backward(self):
        self._board.pop()

    def copy(self):
        new_env = ChessEnv()
        new_env._board = self._board.copy()
        return new_env

    def get_ending_reason(self):
        if self._board.is_checkmate():
            return "checkmate"
        elif self._board.is_stalemate():
            return "stalemate"
        elif self._board.is_insufficient_material():
            return "insufficient material"
        elif self._board.is_fivefold_repetition():
            return "fivefold repetition"
        else:
            return "unknown"

    def filter_illegal_probabilities(self, probabilies, is_training, q):
        probability = list()
        legal_moves = self.get_legal_actions()

        for move in legal_moves:
            fr = move.from_square
            to = move.to_square
            y1 = to // 8
            y2 = fr // 8
            x1 = to % 8
            x2 = fr % 8
            if self._board.san(move)[0].lower() == "n":
                if y1 - y2 == 2:
                    if x1 - x2 == 1:
                        z = 56
                    else:
                        z = 57
                elif y1 - y2 == 1:
                    if x1 - x2 == 2:
                        z = 58
                    else:
                        z = 59
                elif y1 - y2 == -1:
                    if x1 - x2 == 2:
                        z = 60
                    else:
                        z = 61
                else:
                    if x1 - x2 == 1:
                        z = 62
                    else:
                        z = 63
            elif self._board.san(move)[-1].lower() in ["n", "b", "r"]:
                promo = self._board.san(move)[-1].lower()
                if promo == "n":
                    z = 0
                elif promo == "b":
                    z = 3
                else:
                    z = 6
                if x1 > x2:
                    z += 64
                elif x1 < x2:
                    z += 65
                else:
                    z += 66     
            else:
                dist = chess.square_distance(fr, to)
                if y1 > y2:
                    if x1 > x2:
                        z = 7
                    elif x1 < x2:
                        z = 49
                    else:
                        z = 0
                elif y1 < y2:
                    if x1 > x2:
                        z = 21
                    elif x1 < x2:
                        z = 35
                    else:
                        z = 28
                else:
                    if x1 > x2:
                        z = 14
                    else:
                        z = 42
                z += dist
            if is_training:
                try:
                    probabilies[z][y2][x2] = q[legal_moves.index(move)]
                except:
                    ConsoleLogger.error('len(q): {} probabilies.shape: {} probabilies[z][y2][x2].shape: {} z: {} y2: {} x2: {}' \
                        'legal_moves.index(move): {}'.format( \
                        len(q), probabilies.shape, probabilies[z][y2][x2].shape, z, y2, x2, legal_moves.index(move) \
                    ))
            else:
                probability += [probabilies[z][y2][x2]]
        if is_training:
            return probabilies
        else:
            softmax = np.exp(probability)
            softmax = softmax / np.sum(softmax)
            return softmax

    def build_state(self, T=2):
        state = np.zeros((119, 8, 8))
        board2 = self._board.copy()
        for i in range(T):
            if len(board2.move_stack) > 0:
                move = board2.peek()
            else:
                move = None
            ChessEnv._build_state_plane(board2, i, state, move)
            if len(board2.move_stack) > 0:
                board2.pop()
            else: 
                break
        if self._board.turn:
            state[96] += 1
        else:
            state[96] += 2
        state[97] += self._board.fullmove_number
        if self._board.has_kingside_castling_rights(0):
            state[98] += 1
        if self._board.has_kingside_castling_rights(1):
            state[99] += 1
        if self._board.has_queenside_castling_rights(0):
            state[100] += 1
        if self._board.has_queenside_castling_rights(1):
            state[101] += 1
        if self._board.can_claim_fifty_moves():
            state[102] += 1
        
        return state.reshape(1, 119, 8, 8)

    @staticmethod
    def _build_state_plane(board, T, state, move):
        new_board = np.chararray([8, 8], unicode=True)
        pm = board.piece_map()
        for i in board.piece_map():
            new_board[i // 8][i % 8] = pm[i].symbol()
        for i in range(8):
            for j in range(8):
                if new_board[i][j] is not '':
                    layer = ChessEnv._piece_values[new_board[i][j]] + (12 * T)
                    state[layer][i][j] = 1.0
