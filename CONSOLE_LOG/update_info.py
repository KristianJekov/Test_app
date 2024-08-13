import re
import time
from filter import print_colored, colors

full_update_available = False
counter = 0

def parse_progress(line):
    # Regex to extract the numbers within the square brackets
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
        print_colored("Update available for download", colors["cyan"])       
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
            return True
        return False
