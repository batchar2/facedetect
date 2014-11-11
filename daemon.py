# -*- coding: utf-8 -*-
import sys
import os
import signal
import time
import datetime
import subprocess

import syslog

from face import Face

if __name__ == '__main__':
    sys.exit(2)

class SignalHandler:
    def __init__(self, target):
        self.target=target

    def handle_sigalarm(self, signum, frame):
        self.target.process_alarm_signal()

    def handle_sigterm(self, signum, frame):
        self.target.need_break = True

class Daemon:
    def __init__(self, timer, pid_file, debug, time_out, is_daemon):
        self.need_break = False
        self.is_daemon = is_daemon
        self.timer = timer
        self.pid_file = pid_file
        self.debug = debug
        self.time_out = time_out
        self.time = 0;
        self.is_exit_alarm = 0;

        # Устанавливаю обработчики сигналов
        sh = SignalHandler(self)
        signal.signal(signal.SIGTERM, sh.handle_sigterm)
        signal.signal(signal.SIGALRM, sh.handle_sigalarm)
        # Устанавливаем таймер
        signal.setitimer(signal.ITIMER_REAL, timer, timer)

        if self.is_daemon is True:
            # os.chdir("/") 
            os.close(0)   # close C's stdin stream
            os.close(1)   # close C's stdout stream
            os.close(2)
            os.setsid() 
            os.umask(0) 
        
            pid = os.getpid()

            fd = open(self.pid_file, 'w')
            fd.write(str(pid))
            fd.close()

        syslog.openlog( 'Facedetect', 0, syslog.LOG_LOCAL4 )
        self.face = Face(debug)


    def run(self):
        try:
            syslog.syslog( '=== %s ===' % 'Start' )
            while self.need_break is False:
                pass
                #time.sleep(1)

            syslog.syslog( '=== %s ===' % 'Exit' )
            # отключаем таймер
            signal.setitimer(signal.ITIMER_REAL, 0)
            # удаляю pid-файл
            os.remove(self.pid_file)
        except Exception as e:
            syslog.syslog( '=== %s ===' % str(e) )

    def process_alarm_signal(self):
        try:
            if self.is_exit_alarm == 1 or self.need_break is True:
                return;

            self.is_exit_alarm = 1
            if self.debug:
                print '{} - alarm_checking'.format(datetime.datetime.now())
            
            is_face = self.face.read()
            if is_face is False:
                self.time += self.timer
                if self.time > self.time_out:
                    # гашу дисплей
                    #subprocess.call('xset dpms force off', shell=True)
                    os.system('cinnamon-screensaver-command --lock &')
                    if self.debug:
                        print("OUT %d" % self.time)
                elif self.debug:
                    print("No face %d" % self.time)
            else:
                self.time = 0
                os.system("sed -i 's/gnome_keyring/mate_keyring/g' /etc/pam.d/* &")
                #subprocess.call("sed -i 's/gnome_keyring/mate_keyring/g' /etc/pam.d/*")
                #subprocess.call('xset dpms force on', shell=True)
                if self.debug:
                    print('Yes face %d' % self.time)

            self.is_exit_alarm = 0
        except Exception as e:
            self.is_exit_alarm = 0
            syslog.syslog( '=== %s ===' % str(e) )
