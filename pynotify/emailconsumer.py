#!/usr/bin/env python

import ConfigParser
import json
import pika
import smtplib
import syslog

class EmailConsumer:
    def callback(self, ch, method, properties, body):
        print " [x] %r:%r" % (method.routing_key, body)
        
        data = json.loads(body);
        
        try:
            self.mailserver.sendmail(self.config.get('email', 'from'),
                                    data['recipient'],
                                    data['message'])
        except:
            self.connect()
            self.mailserver.sendmail(self.config.get('email', 'from'),
                                    data['recipient'],
                                    data['message'])
        

    def __init__(self):
        syslog.syslog("Starting Email Consumer")
        
        # parse configuration
        self.config = ConfigParser.ConfigParser()
        self.config.read(['pynotify.ini', '../pynotify.ini'])
        
        self.connect()
        
        # connect to queue
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config.get('main', 'ampq_host')))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='topic_pynotify',
                                      type='topic')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        
        self.channel.queue_bind(exchange='topic_pynotify',
                                queue=queue_name,
                                routing_key='email')
        self.channel.basic_consume(self.callback,
                                   queue=queue_name)                  
        
        
        
    def start(self):
        self.channel.start_consuming()
        
    def stop(self):
        self.connection.close()
        
    def connect(self):
        syslog.syslog("Connecting to email server")
        #connect to mail server
        self.mailserver = smtplib.SMTP(self.config.get('email', 'host'),
                                       self.config.get('email', 'port'))
                                       

def main():
    consumer = EmailConsumer()
    consumer.start()
    
if __name__ == '__main__':
    main()
