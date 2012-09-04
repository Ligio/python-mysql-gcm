#!/usr/bin/python

import MySQLdb
import sys
import re
import pycurl
import StringIO
import time
import os
from gcm import GCM
from gcm_setup import AllSetup
from gcm_push_data import PushData

class GCMLogic():

    def __init__(self, debug=None):
	setup = AllSetup()
        self.push_debug = setup.push_debug
        self.host = setup.host
        self.port = setup.port
        self.user = setup.user
        self.passwd = setup.passwd
        self.db = setup.db
        self.gcm_api_key = setup.gcm_api_key
        self.auth = ""
        self.gcm = None
        self.push = None

        try:
            self.conn = self.getConnection()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
	    if(debug==1):
	        self.update_check('on')
            self.must_goon();
            self.gcm = GCM(self.gcm_api_key)
	    self.push = PushData()
	    self.push.readData(setup.push_file)

        except MySQLdb.Error, e:
            print "Error 1 %d: %s" % (e.args[0], e.args[1])
            self.closeAll()
            sys.exit(1)

    def getConnection(self):
        return MySQLdb.connect (host = self.host, port = self.port, user = self.user, passwd = self.passwd, db=self.db)

    def must_goon(self):
        if (self.conn):
            try:
                cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
                q1 = "SELECT * FROM Push_Android_Check WHERE status = 'on' AND service_type = 'gcm'";
                cursor.execute(q1)
                arr_q1 = cursor.fetchall()
                cursor.close()
                if(arr_q1):
                    print "OK... GO ON"
                    #self.update_check('sending')
                    return;
                else:
                    print "NO ACTION..."
                    self.closeAll()
                    exit(1)
            except MySQLdb.Error, e:
                print "Error 2 %d: %s" % (e.args[0], e.args[1])
                self.closeAll()
                sys.exit(1)

    def sendPushToDevices(self, deviceIds):
        response = self.gcm.json_request( registration_ids=deviceIds, data=None, collapse_key='push', delay_while_idle=False, time_to_live=86400 )

        #print response

        # Handle responses. This raises exceptions when GCM servers return errors
        if 'errors' in response:
            for error, reg_ids in response['errors'].items():
                # Check for errors and act accordingly
                '''
                if error is 'NotRegistered':
                    # Remove reg_ids from database
                    for reg_id in reg_ids:
                        #entity.filter(registration_id=reg_id).delete()
                        self.update_status('NotRegistered', reg_id)
                '''
                for reg_id in reg_ids:
                    self.update_status('NotRegistered', reg_id)

        if 'canonical' in response:
            for canonical_id, reg_id in response['canonical'].items():
                # Repace reg_id with canonical_id in your database
                '''
                entry = entity.filter(registration_id=reg_id)
                entry.registration_id = canonical_id
                entry.save()
                '''
                self.update_regid(canonical_id, reg_id)


    def update_status(self, send_status, reg_id):
        conn = self.conn
        if (conn):
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            if(send_status == 'NotRegistered'):
                q1 = "UPDATE Push_Android SET status = '%s', enabled = 'off' WHERE idRegistration = '%s'" % (send_status, reg_id)
            else:
                q1 = "UPDATE Push_Android SET status = '%s' WHERE idRegistration = '%s'" % (send_status, reg_id)
            try:
                self.cursor.execute(q1)
            except MySQLdb.Error, e:
                self.closeAll()
                print "Error 3 %d: %s" % (e.args[0], e.args[1])
        else:
            print "NO CONNECTION"


    def update_regid(self, canonical_id, reg_id):
        conn = self.conn
        if (conn):
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            q1 = "UPDATE Push_Android SET idRegistration = '%s' WHERE idRegistration = '%s'" % (canonical_id, reg_id)
            try:
                self.cursor.execute(q1)
            except MySQLdb.Error, e:
                self.closeAll()
                print "Error 4 %d: %s" % (e.args[0], e.args[1])
        else:
            print "NO CONNECTION"


    def update_check(self, newstatus):
        if (self.conn):
            try:
                cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
                q1 = "UPDATE Push_Android_Check SET status = '%s' WHERE service_type = 'gcm'" % newstatus;
                cursor.execute(q1)
                cursor.close()
            except MySQLdb.Error, e:
                self.closeAll()
                print "Error 5 %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)

    def closeAll(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


    ### Reading Devices id ###
    def getDevices(self):
        print "process item..."

        conn = self.conn

        if(self.auth == None):
            print "Error: NO AUTH"
            exit(1)

        if (conn):
            try:
                q1 = "DELETE FROM Push_Android WHERE status = 'Error=NotRegistered' OR (enabled = 'off' AND lastSend < NOW() - INTERVAL 7 DAY)";
                self.cursor.execute(q1)

                q1 = 'SELECT id,idRegistration FROM Push_Android WHERE enabled="on" AND service_type = "gcm" ORDER BY id'
                self.cursor.execute(q1)
                arr_q1 = self.cursor.fetchall()

                devices = []
                for d in arr_q1:
                    devices.append(d['idRegistration'])

                print '*** Read devices table'

                return devices;

            except MySQLdb.Error, e:
                self.closeAll()
                print "Error 6 %d: %s" % (e.args[0], e.args[1])


