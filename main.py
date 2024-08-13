import sys

sys.path.insert(1,"Server_App")


from Server_App import pages, utils, config, main


def maina():
   main.main() 
    
if __name__ == '__main__':
    maina()