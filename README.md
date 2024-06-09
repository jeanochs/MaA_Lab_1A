# Measurements and Analysis Projected Experiment 1A: Thermistor DAQ

This repository contains the material and codebase for the projected thermistor DAQ teaching experiment. 

Currently in this repo is the codebase only; the lab overview has not been added yet. It contains these files:

MaA_Lab_1A_DAQ.ino
├── MaA_Lab_1A_DAQ.ino
├── sketch.yaml
├── src
│   ├── __pycache__
│   │   └── daq.cpython-312.pyc
│   ├── daq.py
│   └── gui.py
└── thermistor_daq.py

MaA_Lab_1A_DAQ.ino and sketch.yaml are the files relating to the Arduino sketch. This is the file used by the CLI to install the .ino sketch onto the board. *Note that the default port and FQBN can be changed either by hand, or the YAML can be deleted and regenerated using the CLI.*

The src directory contains the source code for the ThermaLens Python application. 

THe thermistor_daq.py is a standalone script that uses the pySerial Library to read the values directly from the Arduino. Note that it uses the USB serial, so ensure that the CLI or the IDE is not reading from the Arduino at the same time. 

Currently, there will be updates to the repo, including the full lab handout, a list of dependencies, and gradual updates to the ThermaLens GUI. 

