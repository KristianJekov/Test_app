import re
from tqdm import tqdm
from colorama import Fore, init as colorama_init
from typing import Optional, Tuple, Any
import queue

colorama_init(autoreset=True)

GREEN = "\033[92m"
RESET = "\033[0m"

DIAGNOSTICS_PATTERN = "diagnostics-service: DIAGN_FirmwareDownload:"
UPDATE_USECASE_PATTERN = "eFoil-remote-receiver: remote_receiver_set_usecase - new usecase: 7 ota"
COMPONENTS_PATTERN = "eFoil-remote-receiver: remote_receiver_updater_callback -"
BATTERY_PATTERN = "btdevmng: btdevmng_updater_callback -"

class FirmwareUpdater:
    def __init__(self):
        self.update_counter = 0
        self.base_progress = 0
        self.last_progress = 0
        self.current_progress = 0  # Track the current component's progress
        self.progress_pattern = re.compile(r'\[(\d+)\s*/\s*(\d+)\]')
        self.ota_pattern = re.compile(r'progress (\d+)%')
        self.progress_started = False
        self.bar = None  # Initialize without tqdm bar

    def create_progress_bar(self) -> tqdm:
        """Create a tqdm progress bar."""
        if not self.bar:
            self.bar = tqdm(
                total=500,
                desc="Downloading",
                bar_format=f"{{l_bar}}{GREEN}{{bar}}{RESET} {{percentage:3.0f}}%| {{n_fmt}}/{{total_fmt}}",
                dynamic_ncols=True,
                leave=False,
                initial=0
            )
        return self.bar

    def parse_progress(self, line: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract current and total progress from a log line."""
        match = self.progress_pattern.search(line)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def print_loading_bar(self, iteration: int, total: int, length: int = 50) -> bool:
        """Print a custom loading bar to the console."""
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\r{bar} {percent}% Available', end='\r')

        if iteration == total:
            print()
            print(Fore.CYAN + "Update available for download")
            self.update_counter += 1
            if self.update_counter == 2:
                return True
        return False

    def check_if_update_available(self, line: str) -> bool:
        """Check for the presence of an update from the diagnostics log line."""
        if DIAGNOSTICS_PATTERN in line:
            current, total = self.parse_progress(line)
            if current is not None and total is not None:
                if self.print_loading_bar(current, total):
                    self.update_counter = 0
                    return True
        return False

    def update_board(self, line: str) -> bool:
        """Process OTA updates and update the tqdm progress bar."""
        if UPDATE_USECASE_PATTERN in line:
            print("Updating to selected version...")

        match = self.ota_pattern.search(line)
        if match:
            progress = int(match.group(1))  # Extract progress percentage
            cumulative_progress = progress + self.base_progress
            increment = cumulative_progress - self.last_progress

            # Start the progress bar if it hasn't started yet
            if not self.progress_started:
                print("Progress started...")
                self.progress_started = True
                self.create_progress_bar()  # Create bar only when progress starts

            # Update the bar if there's a positive increment
            if increment > 0:
                self.bar.update(increment)
                self.last_progress = cumulative_progress
                self.current_progress = progress

        # Check if the current component update is done
        if "updater_callback - done" in line:
            if self.current_progress < 100:  # If current progress is less than 100, complete it
                increment = (100 + self.base_progress) - self.last_progress
                if increment > 0:
                    self.bar.update(increment)  # Complete the current component's progress
                    self.last_progress += increment

            # Increment the base progress by 100% for the completed component
            self.base_progress += 100
            self.current_progress = 0  # Reset current progress for the next component

        # If total progress reaches or exceeds 500%, close the bar and signal completion
        if self.last_progress >= 500:
            self.base_progress = 0
            self.last_progress = 0
            self.current_progress = 0
            self.bar.close()
            self.bar.update(0)
            print(Fore.GREEN + "\nUpdate completed successfully!")
            return True

        return False

    def run_update_process(self, qq: queue.Queue, shutdown_flag: Any):
        """Handle the full update process using the tqdm progress bar."""
        while not shutdown_flag.is_set():
            try:
                line = qq.get(timeout=1)
                if self.update_board(line):
                    return  # Exit once the update completes
            except queue.Empty:
                continue  # If the queue is empty, continue the loop

    def show_detiled_update_info(self, qq: queue.Queue, shutdown_flag: Any):
        counter = 0
        while not shutdown_flag.is_set():
            try:
                line = qq.get(timeout=1)
                if counter >= 5:
                    counter = 0
                    return
                else:
                    if COMPONENTS_PATTERN in line or BATTERY_PATTERN in line:
                        print(line)

                    if "updater_callback - done" in line:
                        counter += 1   

            except queue.Empty:
                continue
