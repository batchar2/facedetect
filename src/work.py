# -*- coding: utf-8 -*-
import sys
import os
import signal

from daemon import Daemon
if __name__ == '__main__':
    sys.exit(2)

class Work:
    def __init__(self, timer, pid_file, debug, time_out, is_daemon):
        self.timer = timer
        self.pid_file = pid_file
        self.debug = debug
        self.time_out = time_out
        self.is_daemon = is_daemon
    
    def start(self):
        if self.is_daemon is True:
            if os.path.exists(self.pid_file) is True:
                print('Error: daemon running!')
                sys.exit(2)
            try:
                pid = os.fork()
                # close parent
                if pid > 0:
                    print('Runign daemon!')
                    sys.exit(0)
            except OSError as e:
                print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
                sys.exit(1)
           
        dm = Daemon(self.timer, self.pid_file, self.debug, self.time_out, self.is_daemon)
        dm.run()
        
    def stop(self):
        if os.path.exists(self.pid_file) is True:
            fd =open(self.pid_file, 'r')
            pid = int(fd.read())
            os.kill(pid, signal.SIGTERM)
            print('Stoped daemon!')
        else:
            print('Not runing daemon!')
    