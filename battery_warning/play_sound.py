from playsound import playsound
import pygame
from tkinter import * 
from tkinter.messagebox import askyesno
import logging
import psutil
from time import sleep
from datetime import datetime

BATTERY_THRESHOLD = 99

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers=[logging.FileHandler('battery_life.log', mode='a'),
                            logging.StreamHandler()])
#Tkinter interface
root = Tk()
root.title("Battery level warning")
root.geometry("400x200")
# Create text widget and specify size.
T = Text(root, height = 5, width = 52)

# Pygame music  
pygame.mixer.init()
pygame.mixer.music.load(r'C:\Users\HP\Python_For_Spyder\mini_projects\battery_warning\Tornado_Siren.mp3')

# Battery Stats
battery = psutil.sensors_battery()
START_BATTERY_PERCENT = battery.percent
START_TIME = datetime.now()

logger.info(f"Program started with battery percent {battery.percent}")

def low_batter_sound_stop():
    pygame.mixer.music.stop()
    # quiting the program
    print("quiting")
    quit()

def low_batter_sound_start():
    global START_TIME
    backup_time=(datetime.now()-START_TIME).total_seconds()/3600
    Fact=f"The battery has run for {backup_time} hours"
    logger.info(f"The battery has run for {backup_time} hours")
    T.pack()
    T.insert(END, Fact)
    pygame.mixer.music.play(loops=9)
    my_button = Button(root,text='Exit',command=low_batter_sound_stop,width='20')
    my_button.pack(pady=20)

while(1):
    sleep(5)
    if START_BATTERY_PERCENT > battery.percent:
        START_BATTERY_PERCENT=battery.percent
        logger.info(f"{battery.percent}")
    if START_BATTERY_PERCENT<=BATTERY_THRESHOLD:
        root.after(1,low_batter_sound_start)
        root.mainloop()