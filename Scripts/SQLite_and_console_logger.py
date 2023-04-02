#!/usr/bin/env python3
'''
@Python    :    3.11.2
@Author    :    mementoQuare
@Copyright :    Daniel Roy, 2023-04-02
@Contact   :    daniellmroy@gmail.com
@License   :    GNU GENERAL PUBLIC LICENSE
'''

import os
import re
import sqlite3
from datetime import datetime
from inspect import currentframe

from colorama import Fore, Style
from colorama import init as colorama_init

# =============================================================================
# [ GLOBAL VARIABLES ]
# =============================================================================
colorama_init()
G_ROOT_FPATH: str = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# [ CLASSES ]
# =============================================================================
class Log(object):
    '''Class to log messages to the console and database'''

    def __init__(self, p_err_lvl: str, p_message: str) -> None:
        '''Class to log messages to the console and database, if not exists,
                create one

        Args:
            p_err_lvl (str): error level
            p_message (str): message to log
        Example:
            >>> Log('info', 'Starting script').log_me()
            >>> Log('warn', 'This is a warning').log_me()
            >>> Log('error', 'This is an error').log_me()
            >>> Log('critical', 'This is a critical error').log_me()
        '''
        self._root_path = self._set_root_path()
        self._if_not_dir()
        self._make_db()
        self._make_table()
        self._err_lvl = p_err_lvl
        self._message = p_message
        self._file = os.path.basename(currentframe().f_back.f_code.co_filename)
        self._func = currentframe().f_back.f_code.co_name
        self._line_num = currentframe().f_back.f_lineno
        self._date_logged = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _set_root_path(self) -> str:
        '''sets root path'''
        v_root = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(v_root, 'logs')

    def _if_not_dir(self) -> None:
        '''creates directory if it doesn't exist'''
        if not os.path.isdir(self._root_path):
            os.mkdir(self._root_path)

    def _make_db(self) -> None:
        '''creates database if it doesn't exist'''
        v_db = os.path.join(self._root_path, 'LiteLog.db')
        if not os.path.isfile(v_db):
            self._conn = sqlite3.connect(v_db)

    def _make_table(self) -> None:
        '''creates database if it doesn't exist'''
        v_create_query = '''
                         CREATE TABLE IF NOT EXISTS LiteLog
                         (date_logged text,
                          err_lvl text,
                          file text,
                          func text,
                          line_num integer,
                          message text);
                         '''
        self._exec_query(v_create_query)

    def _log_to_console(self) -> None:
        '''logs to the console'''
        v_err_lvl = self._err_lvl.upper()
        v_message = self._message
        v_file = self._file
        v_func = self._func
        v_line_num = self._line_num
        v_date_logged = self._date_logged

        v_err_lvl = re.sub('INFO', f'{Fore.GREEN}INFO{Style.RESET_ALL}',
                           v_err_lvl)
        v_err_lvl = re.sub('WARN', f'{Fore.YELLOW}WARN{Style.RESET_ALL}',
                           v_err_lvl)
        v_err_lvl = re.sub('ERROR', f'{Fore.MAGENTA}ERROR{Style.RESET_ALL}',
                           v_err_lvl)
        v_err_lvl = re.sub('CRITICAL', f'{Fore.RED}CRITICAL{Style.RESET_ALL}',
                           v_err_lvl)

        print(f'{v_date_logged} - {v_err_lvl} - {v_file} - {v_func} - '
              f'{v_line_num} - {v_message}')

    def _log_to_db(self) -> None:
        '''logs to the database'''
        v_insert_query = f'''
                         INSERT INTO LiteLog
                         (date_logged, err_lvl, file, func, line_num, message)
                         VALUES('{self._date_logged}',
                                '{self._err_lvl.lower()}',
                                '{self._file.lower()}',
                                '{self._func.lower()}',
                                 {self._line_num},
                                '{self._message.lower()}');
                         '''
        self._exec_query(v_insert_query)

    def _exec_query(self, p_query: str) -> None:
        '''executes query'''
        v_conn = sqlite3.connect(os.path.join(self._root_path, 'LiteLog.db'))
        v_conn.execute(p_query)
        v_conn.commit()
        v_conn.close()

    def log_me(self) -> None:
        '''logs to the console and database'''
        self._log_to_console()
        self._log_to_db()


Log('INFO', 'Starting main routine for logger').log_me()
Log('WARN', 'This is a warning').log_me()
Log('ERROR', 'This is an error').log_me()
Log('CRITICAL', 'This is a critical error').log_me()
