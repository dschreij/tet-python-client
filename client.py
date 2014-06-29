# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\Daniel\.spyder2\.temp.py
"""

import zmq
import socket
import select
import time
import json
import sys

class Tracker(object):
	
	def __init__(self, host="localhost", port=6555):
		self.port = port
		self.host = host
		#self.__init_network(host, port)
		self.__connect(host,port)
		
		
	def __connect(self, addr, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((addr, port))
		except socket.gaierror:
			try:
				s.connect((socket.gethostbyname(addr),port))
			except:
				raise Exception("Unable to find or connect to remote computer {0}:{1}".format(addr,port))
		print "connected to {0}:{1}".format(addr,port)
		self.socket = s

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

	def recv(self,timeout=5):
		start_time = time.time()
		while True:
			r, _, _ = select.select([self.socket], [], [], 0)
			do_read = bool(r)

			if do_read:
				data = self.socket.recv(1024)
				return data	
			
			if time.time() - start_time > timeout:
				break
		return None
		

	def listen(self):
		print "Starting listening"
		
		try:	
			request = {
				"category": "tracker",
				"request": "get",
				"values": "trackerstate"
			}	
			pkg = json.dumps(request)
			print "Sending data: "				
			print pkg
			self.socket.send(pkg)		
			
			data = self.recv(5)
			if data:
				print "Received:"
				print json.loads(data)
				
			request["values"] = ["iscalibrated","hearbeatinterval","version","framerate"]

			pkg = json.dumps(request)
			print "Sending data: "				
			print pkg
			self.socket.send(pkg)		
			
			data = self.recv(5)
			if data:
				print "Received:"
				data = json.loads(data)
				print type(data)
				print data			
				print "======"
				print data["values"]["iscalibrated"]
				

#			except zmq.ZMQError as e:
#				print e
			
		except socket.error as e:
			print "Socket error: ", e.strerror	
				
		self.socket.close()
		print "I have stopped listening"
			
			
if __name__ == "__main__":
	t = Tracker()
	t.listen()
	