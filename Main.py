
#!/bin/python2
# -*- coding: utf-8 -*-

__author__ = "Skokov Stanislav"


import os
import sys
import getopt

import mydaemon

DAEMON_START = 0
DAEMON_STOP  = 1
DAEMON_RESTART = 2

def deamon_command(com):
    if com == DAEMON_START:
        mydaemon.start()
    elif com == DAEMON_STOP:
        mydaemon.stop()
    elif com == DAEMON_RESTART:
        mydaemon.start()
        mydaemon.stop()


if __name__ == '__main__':
    commands = [ 'start', 'stop', 'restart']
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:h', ['command', 'help'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    command = -1

    for o, a in  opts:
        if o in ('-c', '--command'):
            for i in xrange(len(commands)):
                if a == commands[i]:
                    command = i
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    
    if command == -1:
        print("Not command!")
        sys.exit(2)

    deamon_command(command)
    print commands[command]
