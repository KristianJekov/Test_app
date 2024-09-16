import re
from tqdm import tqdm
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

class FirmwareUpdater:
    def __init__(self):
        self.update_counter = 0
        self.base_progress = 0
        self.last_progress = 0
        self.progress_pattern = re.compile(r'\[(\d+)\s*/\s*(\d+)\]')
        self.ota_pattern = re.compile(r'progress (\d+)%')

    def parse_progress(self, line: str) -> tuple[int, int]:
        match = self.progress_pattern.search(line)
        return (int(match.group(1)), int(match.group(2))) if match else (None, None)

    def print_loading_bar(self, iteration: int, total: int, length: int = 50) -> bool:
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
        if "diagnostics-service: DIAGN_FirmwareDownload:" in line:
            current, total = self.parse_progress(line)
            if current is not None and total is not None:
                if self.print_loading_bar(current, total):
                    self.update_counter = 0
                    return True
        return False

    def update_board(self, pbar: tqdm, line: str) -> bool:
        if "eFoil-remote-receiver: remote_receiver_set_usecase - new usecase: 7 ota" in line:
            print("Updating to selected version...")
        
        match = self.ota_pattern.search(line)
        if match:
            progress = int(match.group(1))
            cumulative_progress = progress + self.base_progress
            increment = cumulative_progress - self.last_progress
            pbar.update(increment)
            self.last_progress = cumulative_progress

            if progress == 100:
                self.base_progress += 100

            if self.last_progress >= 400:
                pbar.close()
                print(Fore.GREEN + "\nUpdate completed successfully!")
                return True

        return False