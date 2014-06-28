# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\Daniel\.spyder2\.temp.py
"""

import zmq
import time
import json
import sys

class Tracker(object):
	
	def __init__(self, host="127.0.0.1", port=6555):
		self.port = port
		self.host = host
		self.__init_network(host, port)
		

	def __init_network(self, host_ip, port):
		#network setup
		port = str(port)
		context = zmq.Context()
		self.socket = context.socket(zmq.PAIR)
		host_addr = host_ip + ":"+port
		print "Connecting to " + host_addr
		self.socket.connect("tcp://" + host_addr)
		#filter by messages by stating string 'STRING'. '' receives all messages
		#self.socket.setsockopt(zmq.SUBSCRIBE, '')

	def listen(self):
		keep_going = True
		start_time = time.time()

		print "Starting listening"
		while keep_going:
			# Receive pupil info
			
			try:
				request = {
					"category":"tracker",
					"request":"get",
					"values":"[version]"
				}	
				pkg = json.dumps(request)
				print pkg
				
				self.socket.send(pkg)		
				data = self.socket.recv()
				print data
				
			except zmq.ZMQError as e:
				print e
				
			if time.time() - start_time > 3:
				keep_going = False
				
			self.socket.close()
		print "I have stopped listening"
			
			
if __name__ == "__main__":
	t = Tracker()
	t.listen()
	