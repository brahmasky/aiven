#This module setups logging to be used for both console and file logging
#This module was developed based on code from:
# https://stackoverflow.com/questions/9321741/printing-to-screen-and-writing-to-a-file-at-the-same-time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                         datefmt='%Y/%m/%d %H:%M:%S', 
                        filename='logs/events.log',
                        level=logging.INFO)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console.setFormatter(console_formatter)

logging.getLogger().addHandler(console)

logger = logging.getLogger('events')

