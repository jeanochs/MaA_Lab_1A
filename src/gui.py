import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tk_file
from daq import Arduino_Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas import DataFrame
from datetime import datetime

threaded_identifiers = []

temp_cel_list = []
temp_kel_list = []
therm_res_list = []
time_list = []

min_temperature_limit = 0
max_temperature_limit = 0

error_logging_list = []

ser = Arduino_Serial()


def save_file():
	try:
		file = tk_file.asksaveasfile(parent = main_window, defaultextension = ".csv")
	except:
		pass
	else:

		data_dict = {'Time': time_list, 'Resistance, Ohms':therm_res_list, 'Temperature, Celsius': temp_cel_list}
		headers = DataFrame(data_dict)

		headers.to_csv(file.name, index = False)

def plot_voltage():
	temp_plot.cla()
	temp_plot.plot(temp_cel_list)

def print_to_labels(print_condition, save_condition, limit_condition = False):
	if print_condition:
		try:
			data = ser.get_data()
		except:
			log_to_error_list('Connection to port failed.')
		else:
			voltage_value.config(text = str(data[0]))
			resistance_value.config(text = str(data[1]))
			temp_cel_value.config(text = str(data[3]))
			temp_kel_value.config(text = str(data[2]))

			if save_condition:
				temp_cel_list.append(float(data[3]))
				temp_kel_list.append(float(data[2]))
				therm_res_list.append(float(data[1]))
				time_list.append(datetime.today())

				plot_voltage()
				if limit_condition:
					check_temp_limits(float(data[3]))

				else:
					thread_id = main_window.after(500, lambda: print_to_labels(True, True))
					threaded_identifiers.append(thread_id)

			else:
				thread_id = main_window.after(500, lambda: print_to_labels(True, False))
				threaded_identifiers.append(thread_id)

	else:
		voltage_value.config(text = "")
		resistance_value.config(text = "")
		temp_cel_value.config(text = "")
		temp_kel_value.config(text = "")

		for each in threaded_identifiers:
			main_window.after_cancel(each)

		threaded_identifiers.clear()

def log_to_error_list(message):
	time_format_string = '%m/%d/%Y, %H:%M:%S'
	current_time = datetime.today().strftime(time_format_string)

	error_logging_list.append((current_time, message))

def print_to_error_log(text_area, window):
	printing_string = ''
	for each in error_logging_list:
		printing_string += each[0]+'\t\t'+each[1]+'\n'

	if window.state() == 'normal':
		text_area.config(text = printing_string)

	window.after(200, lambda: print_to_error_log(text_area, window))

def clear_error_log(text_area):
	text_area.config(text = '')

	error_logging_list.clear()

def open_port_window():
	port_window = tk.Tk()
	port_window.title("Add the Arduino port here.")

	frame = ttk.Frame(port_window)
	frame.grid()

	label = ttk.Label(frame, text = 'Port Path')
	current_label = ttk.Label(frame, text = 'Current Path Used: ')
	current_path_label = ttk.Label(frame)
	port_entry = ttk.Entry(frame)

	current_path_label.config(text = ser.serial_port.port)

	label.grid(column = 0, row = 0)
	port_entry.grid(column = 1, row = 0)

	current_label.grid(column = 0, row = 1)
	current_path_label.grid(column = 1, row = 1)


	port_window.protocol('WM_DELETE_WINDOW', lambda: set_port(port_window, port_entry))
	port_window.mainloop()

def open_error_log_window():
	error_log_window = tk.Tk()
	error_log_window.title('Error Log')

	frame = ttk.Frame(error_log_window)
	frame.grid()

	text_area = ttk.Label(frame)
	clear_button = ttk.Button(frame, text = 'Clear Error Log', command = lambda: clear_error_log(text_area))

	text_area.grid(column = 0, row = 0)
	clear_button.grid(column = 0, row = 1)

	print_to_error_log(text_area, error_log_window)

	error_log_window.after(200, lambda: print_to_error_log(text_area, error_log_window))
	error_log_window.mainloop()

def change_buttons(stage):

	match stage:
		case 1:
			read_button.grid()

			start_button.grid_forget()
			export_button.grid_forget()
			disconnect_button.grid_forget()

			temp_range_label.grid_forget()
			temp_range_checkbox.grid_forget()
			min_temp_label.grid_forget()
			min_temp_entry.grid_forget()
			max_temp_label.grid_forget()
			max_temp_entry.grid_forget()


		case 2:
			start_button.grid()
			export_button.grid()
			disconnect_button.grid()

			temp_range_label.grid()
			temp_range_checkbox.grid()

			read_button.grid_forget()
			stop_button.grid_forget()

			min_temp_entry.configure(state = 'enabled')
			max_temp_entry.configure(state = 'enabled')

		case 3:
			stop_button.grid()

			start_button.grid_forget()
			export_button.grid_forget()
			disconnect_button.grid_forget()
			temp_range_label.grid_forget()
			temp_range_checkbox.grid_forget()

			min_temp_entry.configure(state = 'disabled')
			max_temp_entry.configure(state = 'disabled')

		case 4:
			if min_temp_label.winfo_ismapped():
				min_temp_label.grid_forget()
				min_temp_entry.grid_forget()
				max_temp_label.grid_forget()
				max_temp_entry.grid_forget()


			else:
				min_temp_label.grid()
				min_temp_entry.grid()
				max_temp_label.grid()
				max_temp_entry.grid()

				min_temp_entry.configure(state = 'enabled')
				max_temp_entry.configure(state = 'enabled')

def check_temp_limits(num):
	min_temperature_limit = float(min_temp_entry.get())
	max_temperature_limit = float(max_temp_entry.get())

	if (num < min_temperature_limit or num > max_temperature_limit):
		end_recording()
	else:
		thread_id = main_window.after(500, lambda: print_to_labels(True, True, True))
		threaded_identifiers.append(thread_id)

def set_port(window, entry):
	path = entry.get()
	ser.set_connection(path)
	window.destroy()

# This function runs from the start function belowl handles the getting of data from the Arduino and prints it.
def start_reading():
	if ser.open_connection():
		change_buttons(2)
		main_window.after(500, lambda: print_to_labels(True, False))
	else:
		log_to_error_list('Connection failed.')

def stop_reading():
	change_buttons(1)
	ser.close_connection()
	main_window.after(1000, lambda: print_to_labels(False, False))

def begin_recording():
	temp_plot.cla()

	temp_cel_list.clear()
	temp_kel_list.clear()
	therm_res_list.clear()
	time_list.clear()

	if min_temp_label.winfo_ismapped():
		change_buttons(3)
		for each in threaded_identifiers:
			main_window.after_cancel(each)
		threaded_identifiers.clear()
		main_window.after(1000, lambda: print_to_labels(True, True, True))

	else:
		for each in threaded_identifiers:
			main_window.after_cancel(each)
		threaded_identifiers.clear()
		change_buttons(3)
		main_window.after(1000, lambda: print_to_labels(True, True))

def end_recording():
	change_buttons(2)
	for each in threaded_identifiers:
		main_window.after_cancel(each)
	threaded_identifiers.clear()
	main_window.after(1000, lambda: print_to_labels(True, False))

# Setting up of window and menubars starts here
main_window = tk.Tk()
main_window.title("ThermaLens")
main_window.configure(background = "grey")

menubar = tk.Menu(main_window)
config_menu = tk.Menu(menubar, tearoff=0)
config_menu.add_command(label='Add a port...', command = open_port_window)
config_menu.add_command(label='Show Error Log', command = open_error_log_window)
menubar.add_cascade(label="Configure", menu=config_menu)

master_frame = ttk.Frame(main_window)

graph_frame = ttk.Frame(master_frame, height = 300, width = 100)
values_frame = ttk.Frame(master_frame, height = 300, width = 100)
buttons_frame = ttk.Frame(master_frame, height = 300, width = 100)
ranging_frame = ttk.Frame(master_frame, height = 300, width = 100)

voltage_label = ttk.Label(values_frame, text="Voltage (V)")
resistance_label = ttk.Label(values_frame, text="Resistance (Ohms)")
temp_cel_label = ttk.Label(values_frame, text="Temperature, Celsius")
temp_kel_label = ttk.Label(values_frame, text="Temperature, Kelvin")

voltage_value = ttk.Label(values_frame, text="", style = 'ValueLabel.TLabel')
resistance_value = ttk.Label(values_frame, text="", style = 'ValueLabel.TLabel')
temp_cel_value = ttk.Label(values_frame, text="", style = 'ValueLabel.TLabel')
temp_kel_value = ttk.Label(values_frame, text="", style = 'ValueLabel.TLabel')

export_button = ttk.Button(buttons_frame, text="Export", command = save_file)
disconnect_button = ttk.Button(buttons_frame, text="Disconnect", command = stop_reading)
read_button = ttk.Button(buttons_frame, text="Begin Reading", command = start_reading)
start_button = ttk.Button(buttons_frame, text="Start Recording", command = begin_recording)
stop_button = ttk.Button(buttons_frame, text="Stop Recording", command = end_recording)

temp_range_label = ttk.Label(ranging_frame, text="Range")
temp_range_checkbox = ttk.Checkbutton(ranging_frame, command = lambda: change_buttons(4))
min_temp_label = ttk.Label(ranging_frame, text="Minimum Temperature, Celsius")
min_temp_entry = ttk.Entry(ranging_frame)
max_temp_label = ttk.Label(ranging_frame, text="Maximum Temperature, Celsius")
max_temp_entry = ttk.Entry(ranging_frame)

value_label_s = ttk.Style()
value_label_s.configure('ValueLabel.TLabel', background = 'red', foreground = 'red')

# The graph drawign starts here

# the figure that will contain the plot 
fig = Figure(figsize = (5, 5), dpi = 100)

# adding the subplot 
temp_plot = fig.add_subplot(1, 1, 1)
# resistance_plot = fig.add_subplot(1, 2, 2)

canvas = FigureCanvasTkAgg(fig,  master = graph_frame)
canvas.draw()

# placing the canvas on the Tkinter window 
canvas.get_tk_widget().grid()


def position_widgets():
	master_frame.grid()

	graph_frame.grid(column = 0, row = 0)
	values_frame.grid(column = 1, row = 0)
	buttons_frame.grid(column = 0, row = 1)
	ranging_frame.grid(column = 1, row = 1)

	voltage_label.grid(column = 0, row = 0)
	resistance_label.grid(column = 0, row = 1)
	temp_kel_label.grid(column = 0, row = 2)
	temp_cel_label.grid(column = 0, row = 3)

	voltage_value.grid(column = 1, row = 0)
	resistance_value.grid(column = 1, row = 1)
	temp_kel_value.grid(column = 1, row = 2)
	temp_cel_value.grid(column = 1, row = 3)


	export_button.grid(column = 0, row = 0)
	disconnect_button.grid(column = 1, row = 0)
	read_button.grid(column = 0, row = 1)
	start_button.grid(column = 0, row = 1)
	stop_button.grid(column = 0, row = 1)

	temp_range_label.grid(column = 0, row = 0)
	temp_range_checkbox.grid(column = 0, row = 1)
	min_temp_label.grid(column = 0, row = 2)
	min_temp_entry.grid(column = 0, row = 3)
	max_temp_label.grid(column = 0, row = 4)
	max_temp_entry.grid(column = 0, row = 5)

	export_button.grid_forget()
	disconnect_button.grid_forget()
	start_button.grid_forget()
	stop_button.grid_forget()

	temp_range_label.grid_forget()
	temp_range_checkbox.grid_forget()
	min_temp_label.grid_forget()
	min_temp_entry.grid_forget()
	max_temp_label.grid_forget()
	max_temp_entry.grid_forget()

# position_widgets()
# Run the window here.
main_window.config(menu=menubar)
main_window.after(100, position_widgets)
main_window.mainloop()
