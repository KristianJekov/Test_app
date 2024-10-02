import serial
import time
import queue
import threading

def read_from_board(port: str, log_queue: queue.Queue, shutdown_event: threading.Event, retry_delay: float = 5.0):
    
    def initialize_serial_connection():
        try:
            ser = serial.Serial(port=port, baudrate=921600, timeout=1)
            ser.dtr = False
            ser.rts = True
            ser.dtr = True

            time.sleep(0.005)

            ser.dtr = False
            ser.rts = False

            ser.readline()
            return ser
        except serial.SerialException as e:
            print(f"\nSerial initialization failed on {port}: {e}")
            return None

    while not shutdown_event.is_set():
        ser = initialize_serial_connection()
        
        if ser:
            try:
                print(f"\nConnected to {port} and reading logs...")
                
                while not shutdown_event.is_set():
                    try:
                        line = ser.readline().decode('utf-8', errors='ignore').rstrip()
                        if line:
                            try:
                                log_queue.put(line, block=False)
                                
                            except queue.Full:
                                pass

                    except (serial.SerialException, UnicodeDecodeError) as e:
                        print(f"\nError during reading or decoding: {e}")
                        break 
                
            finally:
                ser.close() 
                print(f"\nDisconnected from {port}.")
        

        if not shutdown_event.is_set():
            print(f"\nRetrying connection in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print("\nShutdown signal received. Exiting read loop.")
