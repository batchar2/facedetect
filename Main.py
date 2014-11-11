# -*- coding: utf-8 -*-

__author__ = "Skokov Stanislav"

import os
import sys
import getopt
import time

from work import Work

DAEMON_START = 0
DAEMON_STOP  = 1
DAEMON_RESTART = 2


PID_FILE = '/tmp/facedetect.pid'

def deamon_command(command, timer, debug, time_out, is_daemon):
    wk = Work(timer=timer, pid_file=PID_FILE, debug=debug, time_out=time_out, is_daemon=is_daemon)
    if command == DAEMON_START:
        wk.start()
    elif command == DAEMON_STOP:
        wk.stop()
    elif command == DAEMON_RESTART:
        wk.stop()
        time.sleep(3)
        wk.start()


if __name__ == '__main__':
    commands = [ 'start', 'stop', 'restart']
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:t:c:hpd', ['out', 'time', 'command', 'help', 'print', 'daemon'])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    command, timer, debug, time_out, is_daemon = -1, 1, False, 60, True

    for o, a in  opts:
        if o in ('-c', '--command'):
            for i in xrange(len(commands)):
                if a == commands[i]:
                    command = i
        elif o in ('-h', '--help'):
            print '"-o <число>" Задает промежуток времени в течении которого происхоит ожидание пользователя'
            print '"-t <число>" Интервал через который будет происходить идентификация'
            print '"-d" Запустить не как демон(по-умолчанию включен запуск как демон)'
            print '"-p" Включить режим дебаг. Отображает изображение на экране.'
            sys.exit()
        # время вызова таймера
        elif o == '-t':
            timer = int(a)
        #  демонизировать
        elif o == '-d':
            is_daemon = False
        # дебаг
        elif o == '-p':
            debug = True
        # промежуток в течении которого пользователь может уходить
        elif o == '-o':
            time_out = int(a)
        else:
            assert False, "unhandled option"
    
    if command == -1:
        print("Not command!")
        sys.exit(2)

    deamon_command(command=command, timer=timer, debug=debug, time_out=time_out, is_daemon=is_daemon)
