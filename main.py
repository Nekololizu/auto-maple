"""The central program that ties all the modules together."""

import os
import sys
import time

# Add the utils folder to the system path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.notifier import Notifier
from src.modules.listener import Listener
from src.modules.gui import GUI

# Import the generate_structure script from utils
import generate_structure

# Generate folder structure before starting the main bot logic
try:
    generate_structure.generate_and_save_structure()  # Assuming you create this function
    print("Folder structure generated successfully.")
except Exception as e:
    print(f"Error generating folder structure: {e}")

bot = Bot()
capture = Capture()
notifier = Notifier()
listener = Listener()

bot.start()
while not bot.ready:
    time.sleep(0.01)

capture.start()
while not capture.ready:
    time.sleep(0.01)

notifier.start()
while not notifier.ready:
    time.sleep(0.01)

listener.start()
while not listener.ready:
    time.sleep(0.01)

print('\n[~] Successfully initialized Auto Maple')

gui = GUI()
gui.start()
