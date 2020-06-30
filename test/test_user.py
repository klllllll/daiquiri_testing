'''Unit test on donor starts and donor registration.'''
import os
import socket
import threading
#import psutil
#import platform
import time
import json
import click

class Donor:
	"""Define class Donor."""

	def __init__(self, port, time):
		"""Init."""

		self.host = socket.gethostbyname(socket.gethostname())
		self.port = port
		self.server_host = '18.166.56.143' # save this as a config later?
		self.server_port = 12345
		self.pid = os.getpid()


		# socket listen server
		self.socket_listen_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.socket_listen_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_listen_server.bind(('',self.port))
		self.socket_listen_server.listen(5)

		self.job = None
		self.task = None
		self.donate_time = time
		self.device = self.getDeviceInfo()



	def start(self):
		"""Start donor program."""

		# send registration message before everything starts
		self.sendRegistrationMessage()

		# start a new thread sending heartbeats message if registration
		# done message received 
		_thread = threading.Thread(target = self.sendHeartbeatsMessage)
		_thread.start()

		while True:
			# receive and handle message from the server and 
			# run job programs
			
			while True:
				conn, _ = self.socket_listen_server.accept()
				message = ''
				while True:
					data = conn.recv(1024)
					message += data.decode('utf-8')
					if len(data) < 1024:
						break
				conn.close()
				message = json.loads(message)
				print('currently received message type: ' + message['type'])
				handleMessage(message)

	def getDeviceInfo(self):
		"""Get device hardware information on this device."""

		device_info = {}
		# TODO: What else do we need here?
		'''
		try:
			# in case of permission being denied
			device_info['physical_cores'] = psutil.cpu_count(logical=False)
			device_info['total_cpu_usage'] = psutil.cpu_percent()
			device_info['virtual_memory'] = str(psutil.virtual_memory())
			device_info['platform'] = platform.system() + platform.release()
			device_info['disk_usage'] = psutil.disk_usage(os.getcwd())
			# for gpu machine only
			#device_info['gpu'] = gputil.getGPUS()
		except PermissionError:
			device_info['error'] = 'Permission Denied'
		'''

		device_info['info'] = 'aws failed installing psutil!!'
		return json.dumps(device_info)


	def sendRegistrationMessage(self):
		"""Send regitration message to the server.""" 
		message = {}
		message['type'] = 'registration'
		message['host'] = self.host
		message['port'] = self.port
		message['PID'] = self.pid
		message['device'] = self.device
		message['time'] = self.donate_time
		message = json.dumps(message)
		s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.server_host, self.server_port))
		s.sendall(message.encode('utf-8'))
		s.close()
	
	def sendHeartbeatsMessage(self):
		"""Send heartbeats message to the server."""

		'''
		heartbeat_message = {}
		heartbeat_message['type'] = 'heart beats'
		heartbeat_message['host'] = self.host
		heartbeat_message['port'] = self.port
		heartbeat_message['task'] = self.task
		heartbeat_message['job'] = self.job
		heartbeat_message['PID'] = self.pid
		heartbeat_message = json.dumps(heartbeat_message)

		while True:
			self.socket_heartbeats.sendto(message,(self.server_port,self.server_host))
			time.sleep(5) # time gap
		'''

		# do nothing currently
		while True:
			print("working on sending heartbeat thread!")
			time.sleep(5)

	def handleMessage(self, message):
		"""Handle message received from the server."""
		if message['type'] == 'registration_received':
			# TODO
			print("received!!!!!!!!!!!!!!!!!!!!!!!")
		if message['type'] == 'assign_job':
			# TODO
			pass


@click.command()
@click.argument("donate_time", nargs=1, type=float)
@click.argument("port", nargs=1, type=int)
def main(port, donate_time):
    """Starting Daiquiri master server"""
    donor = Donor(port, donate_time)
    donor.start()		


if __name__ == '__main__':
	main()
