#!/usr/bin/env python

import ConfigParser
import syslog
from pynotify.emailconsumer import EmailConsumer

class PyNotify:
    def __init__(self):
        syslog.openlog()
        syslog.syslog(syslog.LOG_INFO, "Reading configuration file.")
        self.config = ConfigParser.ConfigParser()
        self.config.read(['pynotify.ini'])
        
        self.consumers = [];
        
    def start(self):
        syslog.syslog("Starting.")
        notifications = self.config.get('main', 'enabled_notifications').split(',')
        
        for type in notifications:
            if type == "email":
                self.consumers.append(EmailConsumer().start())
                print "HELLO"
        
        
    def stop():
        syslog.closelog()
        
def main():
    pynotify = PyNotify()
    pynotify.start()
    
if __name__ == "__main__":
    main()