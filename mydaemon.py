# -*- coding: utf-8 -*-
import sys
import os

PID_FILE = '/tmp/facedetect.pid'

if __name__ == '__main__':
    sys.exit(2)

def start():
    if os.path.exists(PID_FILE) is True:
        print('Error: daemon running!')
        sys.exit(2)
    try:
        pid = os.fork()
        # close parent
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    pid = os.getpid()

    fd = open(PID_FILE, 'w')
    fd.write(str(pid))
    fd.close()

    while(1):
        pass

def stop():
    pass

