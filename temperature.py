import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from datetime import datetime
import csv
csv_file = "temperature.csv"
with open(csv_file, mode="a", newline="") as file:
  writer = csv.writer(file)
  if file.tell() == 0:
    writer.writerow(["Time","Celsius","Fahrenheit"])
sensor = adafruit_dht.DHT11(board.D16) # Change the pin number to the data pin of your DHT11 

print("time,celsius,fahrenheit")

def to_fahrenheit(c):
    # TODO: Assign f where f represents the Farienheit equivalent to the input Celcius c
    f = (c*1.8)+32
    return f

while True:
    try:
        celsius = sensor.temperature # Get the temperature in Celcius from the sensor
        fahrenheit = to_fahrenheit(celsius)
        current_time = datetime.now()
        print("{0},{1:0.1f},{2:0.1f}".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit))
# TODO: Light up the red light when the temperature is above 72, and blue when it is below 72.
        with open(csv_file, mode="a", newline="") as file:
          writer = csv.writer(file)
          writer.writerow([current_time, celsius, fahrenheit])
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        if fahrenheit > 72:
          GPIO.output(21, GPIO.HIGH)
          GPIO.output(20, GPIO.LOW)
        elif fahrenheit < 72:
          GPIO.output(20, GPIO.HIGH)
          GPIO.output(21, GPIO.LOW)
        time.sleep(3.0)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as error:
        sensor.exit()
        raise error
