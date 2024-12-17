"""The central program that ties all the modules together."""
from src.common import logger
import os
import sys
import time

# Try importing the generate_structure script directly
try:
    from src.common.generate_structure import generate_and_save_structure
except ImportError as e:
    print(f"Error importing generate_structure: {e}")

# Generate folder structure before starting the main bot logic
try:
    generate_and_save_structure()  # Generate the folder structure and comments
except Exception as e:
    print(f"Error generating folder structure: {e}")

from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.notifier import Notifier
from src.modules.listener import Listener
from src.modules.gui import GUI

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
