import serial
import time
import queue
import threading

def read_all(port: str, qq: queue.Queue, shutdown_flag: threading.Event):
    high, low = False, True

    try:
        with serial.Serial(port=port, baudrate=921600, timeout=1) as ser:
            # Initialize serial port
            ser.dtr = low
            ser.rts = high
            ser.dtr = ser.dtr
            
            ser.dtr = high
            ser.rts = low
            ser.dtr = ser.dtr

            time.sleep(0.005)

            ser.rts = high
            ser.dtr = ser.dtr 
            ser.dtr = low

            # Discard first line
            ser.readline()

            while not shutdown_flag.is_set():
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').rstrip()
                    if line:
                        try:
                            qq.put(line, block=False)
                        except queue.Full:
                            # Optionally, log or handle full queue
                            pass
                except serial.SerialException as e:
                    print(f"Serial port error: {e}")
                    break
                
                except UnicodeDecodeError as e:
                    print(f"Decoding error: {e}")
                    continue

    except serial.SerialException as e:
        print(f"Failed to open serial port {port}: {e}")