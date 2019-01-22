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
