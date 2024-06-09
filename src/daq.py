import serial

class Arduino_Serial:

	def __init__(self, baud = 9600):
		self.baud = baud
		self.serial_port = serial.Serial(baudrate = self.baud, timeout = 1)
		self.serial_conn = False

	def set_connection(self, path):
		self.serial_port.port = path
		print('Reached')
		print('Saved path:', path)

	def open_connection(self):
		try:
			self.serial_port.open()
		except:
			return False
		else:
			self.serial_conn = True

			return True

	def close_connection(self):
		self.serial_port.close()
		self.serial_conn = False

	def get_data(self):
		if self.serial_conn:
			raw_string_data_binary = self.serial_port.readline()
			raw_string = raw_string_data_binary.decode('ascii')[:-2] # Takes a slice and removes the last two charaters (\r and \n) from the string.
			processed_string = raw_string.split(sep="\t")

			return processed_string

		else:
			return Exception('The port has not been opened.')


