#!/usr/bin/env python3
'''
@Python    :    3.11.2
@Author    :    mementoQuare
@Copyright :    Daniel Roy, 2023-04-10
@Contact   :    daniellmroy@gmail.com
@License   :    GNU GENERAL PUBLIC LICENSE
'''

import queue
import threading

# =============================================================================
# [ GLOBAL CONSTANTS ]
# =============================================================================
G_RUN_MANUAL: bool = False


# =============================================================================
# [ MAIN FUNCTIONS ]
# =============================================================================
def auto_vs_manual():
    '''Wait for user input and return it as bool'''
    global G_RUN_MANUAL

    def get_input(message, channel):
        response = input(message)
        channel.put(response)

    channel = queue.Queue()
    thread = threading.Thread(target=get_input, args=('', channel))
    thread.daemon = True
    thread.start()

    try:
        v_response = channel.get(True, 0.1)
        if v_response != '':
            G_RUN_MANUAL = False
            print('Input received, running in auto mode')
            return
    except queue.Empty:
        print('No input received, running in manual mode')
    G_RUN_MANUAL = True
    return


# =============================================================================
# [ CONTROLLER ]
# =============================================================================
auto_vs_manual()
