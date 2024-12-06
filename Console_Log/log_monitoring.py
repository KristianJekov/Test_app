import serial
import time
import threading
import queue


# Function to initialize the serial connection
def initialize_serial_connection(port: str):
    try:
        ser = serial.Serial(port=port, baudrate=921600, timeout=1)
        ser.dtr = False
        ser.rts = True
        ser.dtr = True

        time.sleep(0.005)

        ser.dtr = False
        ser.rts = False

        ser.readline()  # Flush initial data
        return ser
    except serial.SerialException as e:
        print(f"\nSerial initialization failed on {port}: {e}")
        return None


# Function to read from the board
def read_from_board(
    port: str,
    log_queue: queue.Queue,
    shutdown_event: threading.Event,
    retry_delay: float = 5.0,
):

    while not shutdown_event.is_set():
        ser = initialize_serial_connection(port)

        if ser:
            try:
                print(f"\nConnected to {port} and reading logs...")

                while not shutdown_event.is_set():
                    try:
                        # Read raw data from the serial port
                        raw_data = ser.readline()

                        if raw_data:
                            try:
                                # Attempt to decode the data
                                decoded_data = raw_data.decode(
                                    "utf-8", errors="ignore"
                                ).strip()

                                if decoded_data:
                                    # Print decoded data to terminal
                                    print(decoded_data)

                                    # Add decoded data to the log queue if it is not empty
                                    try:
                                        log_queue.put(decoded_data, block=False)
                                    except queue.Full:
                                        pass  # If the queue is full, ignore

                            except UnicodeDecodeError:
                                # If decoding fails, log raw hex data and print to terminal
                                hex_data = raw_data.hex()
                                print(f"Non-UTF-8 data: {hex_data}")

                    except (serial.SerialException, UnicodeDecodeError) as e:
                        print(f"\nError during reading or decoding: {e}")
                        break  # Break the loop if an error occurs during reading

            finally:
                ser.close()  # Ensure the serial connection is closed
                print(f"\nDisconnected from {port}.")

        if not shutdown_event.is_set():
            # Retry the connection if not shutdown
            print(f"\nRetrying connection in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("\nShutdown signal received. Exiting read loop.")


# Function to log the data to a file from the queue
def log_data_to_file(
    log_queue: queue.Queue, log_file: str, shutdown_event: threading.Event
):
    with open(log_file, "a") as file:  # Open in append mode
        while not shutdown_event.is_set():
            try:
                log_entry = log_queue.get(
                    timeout=1
                )  # Wait for a log entry in the queue
                file.write(log_entry + "\n")  # Write the log entry to the file
                file.flush()  # Ensure data is written to disk immediately
            except queue.Empty:
                continue  # If no logs, continue


# Main function to start the reading and logging threads
def main():
    port = "COM17"  # Replace with your COM port
    log_file = "device_logs.txt"  # File to save the logs
    log_queue = queue.Queue(maxsize=100)  # Log queue with max size
    shutdown_event = threading.Event()  # Event to signal shutdown

    print("1: Read\n2: Read and Save")
    mode = input("Select mode (1 or 2): ").strip()

    if mode not in {"1", "2"}:
        print("Invalid mode. Please restart and select 1 or 2.")
        return

    # Start the reading thread
    reading_thread = threading.Thread(
        target=read_from_board, args=(port, log_queue, shutdown_event), daemon=True
    )
    reading_thread.start()

    # If mode 2, start the logging thread
    if mode == "2":
        logging_thread = threading.Thread(
            target=log_data_to_file,
            args=(log_queue, log_file, shutdown_event),
            daemon=True,
        )
        logging_thread.start()

    try:
        # Run the program indefinitely until a shutdown signal is sent
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutdown signal received. Stopping the threads...")
        shutdown_event.set()  # Set the shutdown event to stop the threads
        reading_thread.join()
        if mode == "2":
            logging_thread.join()
        print("Program terminated.")


if __name__ == "__main__":
    main()
