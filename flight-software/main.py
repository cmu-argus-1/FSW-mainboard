
import sys

for path in ['/hal', '/apps']:
    if path not in sys.path:
        sys.path.append(path)


print("initializing the board...")
from hal.pycubed import hardware
from state_manager import state_manager


try:
    # should run forever
    #state_manager.start('NOMINAL')
    import file_t
except Exception as e:
    print(e)



#import file_sd_test

