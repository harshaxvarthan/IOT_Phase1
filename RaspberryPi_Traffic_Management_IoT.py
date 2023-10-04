import RPi.GPIO as GPIO
import time
import threading

# GPIO Pins for sensors and LEDs
SENSOR1_TRIG = 17
SENSOR1_ECHO = 18
SENSOR2_TRIG = 23
SENSOR2_ECHO = 24
RED_LED = 25
GREEN_LED = 8

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR1_TRIG, GPIO.OUT)
GPIO.setup(SENSOR1_ECHO, GPIO.IN)
GPIO.setup(SENSOR2_TRIG, GPIO.OUT)
GPIO.setup(SENSOR2_ECHO, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

def measure_distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
    start_time = time.time()
    end_time = time.time()
    
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        end_time = time.time()
    
    pulse_duration = end_time - start_time
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    return round(distance, 2)

def traffic_lights_controller():
    while True:
        distance1 = measure_distance(SENSOR1_TRIG, SENSOR1_ECHO)
        distance2 = measure_distance(SENSOR2_TRIG, SENSOR2_ECHO)
        if distance1 < 30 or distance2 < 30:
            # Traffic is detected, stop one direction
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
        else:
            # No traffic, let one direction go
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(1)

try:
    # Create and start the traffic lights controller thread
    traffic_thread = threading.Thread(target=traffic_lights_controller)
    traffic_thread.start()

    # Main program loop
    while True:
        pass

except KeyboardInterrupt:
    # Cleanup on Ctrl+C
    GPIO.cleanup()

