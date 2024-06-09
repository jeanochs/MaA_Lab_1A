import serial

ser = serial.Serial('/dev/cu.usbmodem143401', 9600, timeout=1)



while (True):
	raw_string_data_binary = ser.readline()
	raw_string = raw_string_data_binary.decode('ascii')[:-2] # Takes a slice and removes the last two charaters (\r and \n) from the string.
	processed_string = raw_string.split(sep="\t")

	print(processed_string)

