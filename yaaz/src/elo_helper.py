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

import math

def calculate_elo(rating1, rating2, result, k_factor=40):
    expectation = (1.0 / (1.0 + pow(10, ((rating1 - rating2) / 400))))
    return round(rating1 + k_factor * (result - expectation), 2)

def update_elo_score(white_elo, black_elo, winner):
    if winner == 'white':
        new_white_elo = calculate_elo(white_elo, black_elo, 1)
        new_black_elo = calculate_elo(black_elo, white_elo, 0)
    elif winner == 'black':
        new_white_elo = calculate_elo(white_elo, black_elo, 0)
        new_black_elo = calculate_elo(black_elo, white_elo, 1)
    else:
        new_white_elo = calculate_elo(white_elo, black_elo, 0.5)
        new_black_elo = calculate_elo(black_elo, white_elo, 0.5)

    return new_white_elo, new_black_elo
