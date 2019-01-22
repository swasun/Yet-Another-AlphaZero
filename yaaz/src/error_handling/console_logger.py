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

from error_handling.color_print import ColorPrint

import sys
import traceback
import os


class ConsoleLogger(object):

    @staticmethod
    def status(message):
        if os.name == 'nt':
            print('[~] {message}'.format(message=message))
        else:
            ColorPrint.print_info('[~] {message}'.format(message=message))

    @staticmethod
    def success(message):
        if os.name == 'nt':
            print('[+] {message}'.format(message=message))
        else:
            ColorPrint.print_pass('[+] {message}'.format(message=message))

    @staticmethod
    def error(message):
        if sys.exc_info()[2]:
            line = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
            error_message = '[-] {message} with cause: {cause} (line {line})'.format( \
                message=message, cause=str(sys.exc_info()[1]), line=line)
        else:
            error_message = '[-] {message}'.format(message=message)
        if os.name == 'nt':
            print(error_message)
        else:
            ColorPrint.print_fail(error_message)

    @staticmethod
    def warn(message):
        if os.name == 'nt':
            print('[-] {message}'.format(message=message))
        else:
            ColorPrint.print_warn('[-] {message}'.format(message=message))

    @staticmethod
    def critical(message):
        if sys.exc_info()[2]:
            line = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
            error_message = '[!] {message} with cause: {cause} (line {line})'.format( \
                message=message, cause=str(sys.exc_info()[1]), line=line)
        else:
            error_message = '[!] {message}'.format(message=message)
        if os.name == 'nt':
            print(error_message)
        else:
            ColorPrint.print_major_fail(error_message)
