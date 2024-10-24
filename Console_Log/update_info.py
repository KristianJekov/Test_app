import queue
import re
import sys
from typing import Any, Optional, Tuple

sys.path.extend("Server_App")

from Server_App.config import config
from colorama import Fore
from colorama import init as colorama_init
from tqdm import tqdm

colorama_init(autoreset=True)

GREEN = "\033[92m"
RESET = "\033[0m"


class FirmwareUpdater:
    def __init__(self):
        self.update_counter = 0
        self.base_progress = 0
        self.last_progress = 0
        self.current_progress = 0
        self.restarts = 0
        self.components_updated_list = []  # Track the current component's progress
        self.progress_pattern = re.compile(r"\[(\d+)\s*/\s*(\d+)\]")
        self.ota_pattern = re.compile(r"progress (\d+)%")
        self.progress_started = False
        self.bar = None  # Initialize without tqdm bar

    def create_progress_bar(self) -> tqdm:
        """Create a tqdm progress bar."""
        if not self.bar:
            self.bar = tqdm(
                total=config.COMPONETS_FOR_UPDATES * 100,
                desc="Downloading",
                bar_format=f"{{l_bar}}{GREEN}{{bar}}{RESET} {{percentage:3.0f}}%| {{n_fmt}}/{{total_fmt}}",
                dynamic_ncols=True,
                leave=False,
                initial=0,
            )
        return self.bar

    def parse_progress(self, line: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract current and total progress from a log line."""
        match = self.progress_pattern.search(line)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def print_loading_bar(self, iteration: int, total: int, length: int = 70) -> bool:
        """Print a custom loading bar to the console."""
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = "█" * filled_length + "-" * (length - filled_length)
        print(f"\r{bar} {percent}% Preparing files...", end="\r")

        if iteration == total:
            print()
            print(Fore.CYAN + "Update available for download")
            self.update_counter += 1
            if self.update_counter == 2:
                return True
        return False

    def check_if_update_available(self, line: str) -> bool:
        """Check for the presence of an update from the diagnostics log line."""
        if config.DIAGNOSTICS_PATTERN in line:
            current, total = self.parse_progress(line)
            if current is not None and total is not None:
                if self.print_loading_bar(current, total):
                    self.update_counter = 0
                    return True
        return False

    def update_board(self, line: str) -> bool:
        if config.UPDATE_USECASE_PATTERN in line:
            print("Updating to selected version...")

        match = self.ota_pattern.search(line)
        if match:

            progress = int(match.group(1))

            cumulative_progress = self.base_progress + progress

            increment = cumulative_progress - self.last_progress

            if not self.progress_started:
                print("Progress started...")
                self.progress_started = True
                self.create_progress_bar()  # Create the bar when the progress starts

            if increment > 0:
                self.bar.update(increment)
                self.last_progress = (
                    cumulative_progress  # Update last_progress to cumulative value
                )
                self.current_progress = progress

        if "updater_callback - progress 10%" in line:
            component_status = 0
            self.components_updated_list.append(component_status)

        if "updater_callback - done" in line:
            self.components_updated_list[-1] = 1

            if self.current_progress < 100:
                increment = (100 + self.base_progress) - self.last_progress
                if increment > 0:
                    self.bar.update(
                        increment
                    )  # Complete the current component's progress
                    self.last_progress += increment

            self.base_progress += 100
            self.current_progress = 0  # Reset current progress for the next component

        if "BT_HCI: hcif disc complete: hdl 0x1, rsn 0x13" in line:
            self.restarts += 1

        if self.restarts >= 3:
            config.CURRENT_UPDATE_COMPLETED = False
            self.reset_progress()
            print(Fore.RED + "\\UPDATE-FAILED!\\")
            print(
                Fore.YELLOW
                + f"{sum(self.components_updated_list)}/{config.COMPONETS_FOR_UPDATES} Updated..."
            )
            print(self.components_updated_list)
            self.components_updated_list = []
            return True

        if (
            self.last_progress >= config.COMPONETS_FOR_UPDATES * 100
            and sum(self.components_updated_list) == config.COMPONETS_FOR_UPDATES
        ):
            config.CURRENT_UPDATE_COMPLETED = True
            self.reset_progress()
            print(Fore.GREEN + "\n\\UPDATE-SUCCESSFUL!\\")
            print(self.components_updated_list)
            self.components_updated_list = []
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
        while not shutdown_flag.is_set():
            try:
                line = qq.get(timeout=1)
                if "BT_HCI: hcif disc complete: hdl 0x1, rsn 0x13" in line:
                    self.restarts += 1

                if "updater_callback - " in line:
                    print(line)

                if "updater_callback - progress 10%" in line:
                    component_status = 0
                    self.components_updated_list.append(component_status)

                if "updater_callback - done" in line:
                    self.components_updated_list[-1] = 1

                if sum(self.components_updated_list) >= config.COMPONETS_FOR_UPDATES:

                    print(Fore.GREEN + "\n\\UPDATE-SUCCESSFUL!\\")
                    print(self.components_updated_list)
                    return
                else:
                    if self.restarts >= 3:
                        print(Fore.RED + "\\UPDATE-FAILED!\\")
                        print(
                            Fore.YELLOW
                            + f"{sum(self.components_updated_list)}/{config.COMPONETS_FOR_UPDATES} Updated..."
                        )
                        print(self.components_updated_list)

                        self.restarts = 0
                        self.reset_progress()
                        return shutdown_flag.is_set()

            except queue.Empty:
                continue

    def reset_progress(self):
        """Reset all progress variables."""
        self.base_progress = 0
        self.last_progress = 0
        self.current_progress = 0
        # self.components_updated_list = []
        self.restarts = 0
        self.progress_started = False
        if self.bar:
            self.bar.close()
            self.bar = None
