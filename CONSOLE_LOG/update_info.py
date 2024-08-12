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

def print_loading_bar(iteration, total, length=70):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{bar} {percent}% Available', end='\r')
    if iteration == total:
        print()
        print_colored("Update available for download", colors["cyan"])

def process_line(line):
    current, total = parse_progress(line)
    if current is not None and total is not None:
        print_loading_bar(current, total)

def check_if_update_available(line):
    if line.__contains__("diagnostics-service: DIAGN_FirmwareDownload:"):

        process_line(line)

    # if line.__contains__("diagnostics-service: Target sw version :"):
    #     pass
    # if line.__contains__("diagnostics-service: get Software Version :"):
    #     print_colored("Update available for download", colors['cyan'])
    # diagnostics-service: DIAGN_SurfReport
    #  diagnostics-service: DIAGN_FirmwareDownload: [520] 
    # diagnostics-service: DIAGN_SessionEnd
    # I (11:59:33.097) diagnostics-service: DIAGN_FirmwareDownload: