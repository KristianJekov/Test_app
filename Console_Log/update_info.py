import re
from tqdm import tqdm
import colorama
from colorama import Fore

colorama.init(autoreset=True)

full_update_available = False
counter = 0

def parse_progress(line):
    match = re.search(r'\[(\d+)\s*/\s*(\d+)\]', line)
    if match:
        current = int(match.group(1))
        total = int(match.group(2))
        return current, total
    return None, None

def print_loading_bar(iteration, total, length=100):
    global counter
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{bar} {percent}% Available', end='\r')
    if iteration == total:
        print()
        print(Fore.CYAN + "Update available for download")       
        counter += 1
        if counter == 2:
            
            return True
    return False

def process_line(line):
    current, total = parse_progress(line)
    if current is not None and total is not None:
        print_loading_bar(current, total)

def check_if_update_available(line):
    global counter
    if line.__contains__("diagnostics-service: DIAGN_FirmwareDownload:"):
        process_line(line)
        if counter % 2 == 0 and counter > 0:
            counter = 0
            return True
        return False

def update_board(line):
    #  print(line)
     if line.__contains__("eFoil-remote-receiver: remote_receiver_set_usecase - new usecase: 7 ota"):
        print("Updating to selected version...")
     loading_bar(4, line)
        

def loading_bar(components, line, msg = "Dowloading"):
    base_progress = 0

    with tqdm(total=components*100, desc=msg) as pbar:
        last_progress = 0  

        pattern = re.compile(r'progress (\d+)%')

        match = pattern.search(line)
        if match:
            progress = int(match.group(1))

            cumulative_progress = progress + base_progress

            increment = cumulative_progress - last_progress
            pbar.update(increment)
            last_progress = cumulative_progress

            if progress == 100:
                base_progress += 100

    if last_progress == components*100: 
        return True
    return False
    