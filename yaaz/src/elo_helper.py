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
