#include <math.h>

float series_res = 100000;
float source_voltage = 5;
float ref_res = 100000;
float ref_temp = 298.15; // 25 centigrade in Kelvin
float beta = 4000; // In Kelvin

int output_pin = A1;
int ground_pin = A0;

// This handles the pretty printing of the lines.
bool pretty_print = false;

float map_f(float value, float raw_low, float raw_high, float process_low, float process_high) {
	float multi = (process_high-process_low)/(raw_high-raw_low);
	return value*multi;
}

float res_T(float voltage) {
	return (series_res*voltage)/(source_voltage-voltage);
}

float temp_from_res(float res) {
	float x_1 = log(res/ref_res);
	float x_2 = 1/beta;
	float x_3 = 1/ref_temp;

	return pow((x_2*x_1)+x_3, -1);

}	 

void setup() {
	pinMode(output_pin, INPUT);

	Serial.begin(9600);
}

void loop() {
	int raw_value = analogRead(output_pin);
	float voltage = map_f(raw_value, 0, 1023, 0, 5);
	float real_volt = (5 - voltage);

	float therm_res = res_T(real_volt);
	float temperature_kelvin = temp_from_res(therm_res);
	float temperature_celsius = temperature_kelvin - 273.15;

	// Pretty Print lines
	// This should be disabled for actual usage with Python script.
	if (pretty_print) {
		Serial.println("Voltage of thermistor: "+String(real_volt));
		Serial.println("Resistance of thermistor: "+String(therm_res));
		Serial.println("Temperature (Kelvin): "+String(temperature_kelvin));
		Serial.println("Temperature (Celsius): "+String(temperature_celsius));
		Serial.println("-------------------------------");
		Serial.println();
	}
	else {
		String sending_string = String(real_volt)+"\t"+String(therm_res)+"\t"+String(temperature_kelvin)+"\t"+String(temperature_celsius);
		Serial.println(sending_string);
	}

	delay(500);
	
}
