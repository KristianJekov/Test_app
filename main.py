from utils.update_device import update_to_last_version
from utils.mode_select import registerate_device_in_mode
from config import config


def main():
    # update_to_last_version()
    registerate_device_in_mode(config.CURRENT_MODE)
    
 
if __name__ == '__main__':
    main()