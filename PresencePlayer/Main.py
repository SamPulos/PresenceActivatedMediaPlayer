import os
import sys
import time
import random
import signal
from Arduino import Arduino
from MediaDisplayManager import MediaDisplayManager
from ImageController import ImageController
from ConfigParser import ConfigParser
from math import ceil
from system_hotkey import SystemHotkey

# ---------- Read in config ----------
configData = ConfigParser().configData

# ---------- Order media and convert to clips for playing ---------- 
if len(configData['displayable_media']) is 0:
    sys.exit("no displayable media found in config")
    
mediaPaths = configData['displayable_media']
if configData['media_order'] == 'alphabetic':
    mediaPaths.sort()
elif configData['media_order'] == 'shuffle':
    random.shuffle(mediaPaths)

displayableMedia = []
for mediaPath in configData['displayable_media']:
    displayableMedia.append(mediaPath)
print(displayableMedia)


# ---------- Setup arduino connection ----------
arduino = Arduino(targetDistance = configData['distance_threshold'], historySize = ceil(1000 * configData['reset_wait_duration'] / configData['poll_rate']))

# ---------- Setup background image display ---------------
backgroundImage = configData['background_image'] #"/home/pi/python_games/4row_humanwinner.png"
backgroundImageDisplay = ImageController(backgroundImage)
backgroundImageDisplay.display()

# ---------- Setup MediaDisplayManager ---------------
mediaDisplayManager = MediaDisplayManager(configData['image_display_duration'] / configData['poll_rate'])
    
# ---------- Helper functions ---------------
currentMediaIndex = -1
def selectNextMedia():
    global currentMediaIndex
    if configData['media_order'] == 'random':        
        currentMediaIndex = random.randint(0, len(displayableMedia) - 1)
    else:
        currentMediaIndex = ((currentMediaIndex + 1) % len(displayableMedia))
    return displayableMedia[currentMediaIndex]

triggerCondition = configData['trigger_condition']
def checkTrigger():
    if triggerCondition == 'motion':
        return (arduino.detectingMotion())
    elif triggerCondition == 'proximity':
        return (arduino.detectedProximityRecently())
    elif triggerCondition == 'motion and proximity':
        return (arduino.detectingMotion() and arduino.detectedProximityRecently())
    elif triggerCondition == 'motion or proximity':
        return (arduino.detectingMotion() or arduino.detectedProximityRecently())
    else:
        print('WARNING: trigger condition is undefined')
        return (True)

resetCondition = configData['reset_condition']
def checkReset():
    if resetCondition == 'no motion':
        return (not arduino.detectingMotion())
    elif resetCondition == 'no distance':
        return (not arduino.detectedProximityRecently())
    elif resetCondition == 'no motion and no proximity':
        return ((not arduino.detectingMotion()) and (not arduino.detectedProximityRecently()))
    elif resetCondition == 'no motion or no proximity':
        return ((not arduino.detectingMotion()) or (not arduino.detectedProximityRecently()))
    else:
        print('WARNING: reset condition is undefined')
        return (True)

looping = True

def quitApp():
    print("quitting app")
    global looping
    looping = False
    os.kill(os.getpid(), signal.SIGINT)
    
# ---------- Main loop ----------
try:
    hotKeys = SystemHotkey()
    hotKeys.register(['escape'], callback = lambda event: quitApp())
    resetConditionMet = False
    triggerConditionMet = False
    
    while looping:
        time.sleep(configData['poll_rate'] / 1000)
        arduino.update()
        mediaDisplayManager.update()
        triggerConditionMet = checkTrigger()
        resetConditionMet = checkReset()        
        if (triggerConditionMet and not mediaDisplayManager.isDisplaying()):
            print("Trigger condition met, displaying media")
            currentMedia = selectNextMedia();
            mediaDisplayManager.display(currentMedia)
        elif (resetConditionMet and mediaDisplayManager.isDisplaying()):
            print("reset condition met, stopping media")
            mediaDisplayManager.stop();
    
    if backgroundImageDisplay.isDisplaying:
        backgroundImageDisplay.stop()
    if mediaDisplayManager.isDisplaying():
        mediaDisplayManager.stop()
                
except KeyboardInterrupt:
    print("handling interrupt")
    backgroundImageDisplay.stop()
    mediaDisplayManager.stop()
    sys.exit(0)

"""

# NEXTODO:
# Use proper distance units
# Fail elegantly

"""