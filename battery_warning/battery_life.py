# python script showing battery details
import psutil
import logging
from time import sleep

logger = logging.getLogger(__name__)

# function returning time in hh:mm:ss


def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


# returns a tuple
battery = psutil.sensors_battery()

# print("Battery percentage : ", battery.percent)
print("Power plugged in : ", battery.power_plugged)

# # converting seconds to hh:mm:ss
# print("Battery left : ", convertTime(battery.secsleft))


def main():
    # while(1):
    #     logger.info(f'{battery.percent}')
    #     sleep(15)
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler('battery_life.log', mode='a'),
                                  logging.StreamHandler()])

    main()
