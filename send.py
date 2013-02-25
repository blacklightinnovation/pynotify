#!/usr/bin/env python

import argparse
import json
import pika
import sys

desc = '''Test sending notification messages into the queue.  Use this to 
          validate if your notification consumers are enabled and configured
          properly.'''
parser = argparse.ArgumentParser(description=desc,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('type', help='The type of notification')
parser.add_argument('recipient', 
                    help='The recipient of the notification')
parser.add_argument('message', 
                    nargs='?',
                    help='The message to send to the recipient',
                    default='Hello World!')
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_pynotify',
                         type='topic')

body = json.dumps({'recipient': args.recipient,
                   'message': args.message})
channel.basic_publish(exchange='topic_pynotify',
                      routing_key=args.type,
                      body=body)
print " [x] Sent %r" % (body)
connection.close();

