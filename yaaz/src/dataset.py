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

import os
import re
import numpy as np
from keras.models import load_model


class Dataset(object):

    def __init__(self, results_path):
        self._results_path = results_path
        self._environments_path = self._results_path + os.sep + 'environments'
        self._models_path = self._results_path + os.sep + 'models'

    def record_environment(self, environments):
        record_id = self._resolve_new_id(self._environments_path)
        np.save(self._environments_path + os.sep + 'environments_' + record_id, np.asarray(environments))
    
    def record_model(self, model):
        record_id = self._resolve_new_id(self._models_path)
        model.save(self._models_path + os.sep + 'model_' + record_id + '.h5')

    def load_best_model(self):
        last_id = self._get_last_id(self._models_path)
        if last_id == -1:
            return None
        return load_model(self._models_path + os.sep + 'model_' + str(last_id) + '.h5')

    def erase_best_model(self, new_model):
        last_id = self._get_last_id(self._models_path)
        new_model.save(self._models_path + os.sep + 'model_' + str(last_id) + '.h5')

    def load_n_last_environment_batches(self, n):
        environments = list()
        file_names = sorted(
            self._list_files(self._environments_path),
            key=lambda x: int(re.sub('\D', '', x)),
            reverse=True)[:n]
        for file_name in file_names:
            environments.append(np.load(self._environments_path + os.sep + file_name))
        return np.asarray(environments)

    @staticmethod
    def environment_to_dict(result, policies, actions):
        environment = dict()
        environment['result'] = result
        environment['policies'] = policies
        environment['actions'] = actions
        return environment

    def _get_last_id(self, path):
        file_names = self._list_files(path)
        if len(file_names) == 0:
            return -1
        file_names = sorted(file_names, key=lambda x: int(re.sub('\D', '', x)), reverse=True)
        return int(file_names[0].split('_')[1].split('.')[0])

    def _resolve_new_id(self, path):
        last_id = self._get_last_id(path)
        if last_id == -1:
            return '0'
        return str(last_id + 1)

    def _list_files(self, path):
        file_names = list()
        for _, _, files in os.walk(path):
            for file in files:
                file_names.append(file)
        return file_names
