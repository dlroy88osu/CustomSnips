#!/usr/bin/env python3
'''
@Python    :    3.11.2
@Author    :    mementoQuare
@Copyright :    Daniel Roy, 2023-04-02
@Contact   :    daniellmroy@gmail.com
@License   :    GNU GENERAL PUBLIC LICENSE
'''

import logging as log

from github import Github

# =============================================================================
# [ GLOBAL VARIABLES ]
# =============================================================================
G_ASSIGNEE = 'mementoQuare'
G_PROJECT_REPO = 'mementoQuare/WhatTheFailure'
G_TOKEN = 'EDRFTGYHUJIKO987654FGYHUJ'


# =============================================================================
# [ CLASSES ]
# =============================================================================
class WTF(object):  # What The Failure!!!
    '''What The Failure! --> Automated error issue writer for github'''

    def __init__(self, p_title: str, p_msg: str, p_label: str) -> None:
        '''Automated error issue writer for github

        Args:
            p_title (str): title of issue
            p_msg (str): message to include in issue
            p_label (str): label to apply to issue
        Example:
            >>> WTF('report_name', 'error message', 'W.T.F. bug').seriously()
        '''

        log.info('Initializing WTF')
        self._title = f'W.T.F. => {p_title.title()}'
        self._msg = p_msg.lower()
        self._who = G_ASSIGNEE
        self._lbl = p_label
        self._repo = G_PROJECT_REPO
        self._gh = None
        self._rpx = None
        self.seriously()

    # [I get my token from auth class and set to self._gh - not supplied]
    def _get_gh(self):
        '''initializes github'''
        log.info('Getting token')
        # v_keys = GateKeeper('api_github').let_me_in()
        # self._gh = Github(v_keys['pass'])
        self._gh = Github(G_TOKEN)

    def _get_repo(self):
        '''gets repo'''
        log.info('Getting repo')
        self._rpx = self._gh.get_repo(self._repo)

    def _create_issue(self):
        '''creates issue'''
        log.info('Creating issue')
        self._rpx.create_issue(title=self._title, body=self._msg,
                               assignee=self._who, labels=[self._lbl])
        return

    def seriously(self):
        '''Public method to create the issue in desired location'''
        log.info('Creating issue')
        self._get_gh()
        self._get_repo()
        self._create_issue()


WTF('report_name', 'error message', 'W.T.F. bug').seriously()
