#!/usr/bin/python

## DATE: 2012-08-20
## AUTHOR: Marco Lijoi
## LICENSE: BSD http://www.opensource.org/licenses/bsd-license.php
## Copyright 2012-present Marco Lijoi

from __future__ import division
from socket import gethostname;
import threading
import sys
import os
import time
import MySQLdb
import math
from gcm_logic import GCMLogic

class threader(threading.Thread):
    def __init__(self,counter,mysqlconn,deviceIds):
        threading.Thread.__init__(self)
        self.counter = counter
        self.deviceIds = deviceIds
        self.mysqlconn = mysqlconn

    def run(self):
        push.sendPushToDevices(self.deviceIds)


def init_thread(): 
    devices = push.getDevices()

    backgrounds = []
    num_devices = len(devices)
    max_broadcast_devices = 4
    loop_number = 0

    for i in range(int(math.ceil(num_devices/max_broadcast_devices))):
        registration_ids = devices[loop_number*max_broadcast_devices:(loop_number+1)*max_broadcast_devices]

        mysql_conn = connections[loop_number % THREADS]

        background = threader(i,mysql_conn,registration_ids)
        background.start()
        backgrounds.append(background)
        loop_number = loop_number + 1

        if(loop_number%THREADS==0 or loop_number*max_broadcast_devices >= (num_devices-1)):
            print "JOIN THREADS...";
            for background in backgrounds:
                background.join()
            backgrounds = []

    push.update_check('off')
    closeAll()

def closeAll():
    push.closeAll()
    for connection in connections:
        connection.close()

def main():
    try:
        init_thread()
    except Exception, e:
        closeAll()
        print "failed to initiate threads"
        print e

    sys.exit(0)

if __name__ == "__main__":
    push = GCMLogic()
    THREADS = 5

    connections = []
    for thread in range(THREADS):
        try:
            connections.append(push.getConnection())
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            closeAll()
            sys.exit(1)

    main()
