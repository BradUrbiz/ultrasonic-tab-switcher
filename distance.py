import RPi.GPIO as GPIO
import bluetooth
import time

GPIO.setmode(GPIO.BCM)
trig = 23
echo = 24
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

change_threshold = 10 # trigger amount needed
sample_interval  = 0.5 # seconds between readings
cooldown = 2.0 # cooldown
receiver = "XX:XX:XX:XX:XX:XX" # Bluetooth MAC
port = 1


def get_distance():
    GPIO.output(trig, False)
    time.sleep(0.05)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    timeout = time.time() + 0.1
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    timeout = time.time() + 0.1
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    duration = pulse_end - pulse_start
    return round(duration * 17150, 2)


def send_signal(msg="SWITCH"):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((reciever_address, port))
        sock.send(msg)
        sock.close()
        print(f"Sent {msg}")
    except bluetooth.BluetoothError as e:
        print(f"BT error: {e}")


def main():
    prev = None
    last_trigger = 0

    print("Active")
    try:
        while True:
            dist = get_distance()

            if dist is None:
                print("Invalid?!?")
                time.sleep(sample_interval)
                continue

            print(f"{dist} cm")

            if prev is not None:
                change = abs(dist - prev)
                now = time.time()

                if change >= change_threshold and (now - last_trigger) > cooldown:
                    print(f"Change of: {change:.1f} cm detected")
                    send_signal("SWITCH")
                    last_trigger = now

            prev = dist
            time.sleep(sample_interval)

    except KeyboardInterrupt:
        print("Terminated")
    finally:
        GPIO.cleanup()
