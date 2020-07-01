'''Unit test on server starts and donor registration.'''
import socket
import threading
import click
import json

class Server:
	"""Define class Server."""
	
	def __init__(self, port):
		"""Init."""

		self.registered_donors = []
		self.submitters = []
		self.tasks = []
		self.jobs = []
		self.donor_alive = []

		# create a TCP socket send and receive message from donor
		self.socket_donors = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_donors.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_donors.bind(('', port)) # current EC2 SG open port: 12345
		self.socket_donors.listen(5)
		



	def start(self):
		"""Daiquiri server starts."""

		# start a new thread to listen message from donor
		_thread = threading.Thread(target=self.listenDonorMessage)
		_thread.start()

		while True:
			a = 123 # do nothing

	def listenDonorMessage(self):
		"""Listen message from donor."""

		# executing all the life time
		print("listen thread start")
		while True:
			conn, _ = self.socket_donors.accept()
			message = ''
			while True:
				data = conn.recv(1024)
				message += data.decode('utf-8')
				if len(data) < 1024:
					break
			conn.close()
			message = json.loads(message)

			# handle donor message
			if message['type'] == 'registration':
				self.registerDonor(message)

	def registerDonor(self, message):
		"""Register donor on server."""

		donor = {
			'donorID': len(self.registered_donors),
			'host': message['host'],
			'port': message['port'],
			'localPro:cessID': message['PID'],
			'status': 'alive',
			'device': message['device'],
			'donate_time': message['time'],
			'task': None,
			'current_job_ID': None,
			'loss': 0		
		}
		self.registered_donors.append(donor)

		print("donor reg received, IP addr: " + donor['host'])
		print("1111111111111111111")
		# send an acknowledge message back to the donor
		response_message = {
			'type': 'registration_received',
			'host': message['host'],
			'port': message['port'],
			'PID': message['PID'],
			'device': message['device'],
			'time': message['time']
		}

		# donors open a TCP socket connection to listen message from the server
		response_message = json.dumps(response_message)
		print("2222222222222222222222")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("33333333333333333333")
		s.connect((message['host'], message['port']))
		print("44444444444444444444444")
		s.sendall(response_message)
		print(message['host'] + message['port'])
		s.close()

@click.command()
@click.argument("port_num", nargs=1, type=int)
def main(port_num):
    """Starting Daiquiri server"""
    server = Server(port_num)
    server.start()		


if __name__ == '__main__':
	main()