#!/usr/bin/python

import json

class PushData():

	def __init__(self):
		self.data = None
		self.collapse_key = 'push'
		self.delay_while_idle = False
		self.time_to_live = 86400

	def setData(self, data=None, collapse_key='push', delay_while_idle=False, time_to_live=86400):
		self.data = data
		self.collapse_key = collapse_key
		self.delay_while_idle = delay_while_idle
		self.time_to_live = time_to_live

	def readData(self, myfile):
		print "read push"
		in_file = open(myfile,"r")
		text = in_file.read()
		in_file.close()	
	
		mydecoder = json.JSONDecoder()
		push_data = mydecoder.decode(text)
		self.setData(push_data['data'], push_data['collapse_key'], push_data['delay_while_idle'], push_data['time_to_live'])
			

	def writeData(self, myfile, json_data_string=None):
		print "write push"
		out_file = open(myfile,"w")
		json_data = {}
		if(json_data_string==None):
			json_data['data'] = self.data
			json_data['collapse_key'] = self.collapse_key
			json_data['delay_while_idle'] = self.delay_while_idle
			json_data['time_to_live'] = self.time_to_live
			json_data = json.dumps(json_data)
		else:
			json_data = json_data_string

		out_file.write(json_data)
		out_file.close()

