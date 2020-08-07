import os
import sys
import time
import psutil
from math import log10, ceil
from subprocess import Popen
from omxplayer import OMXPlayer

class Clip:
    def __init__(self, clipLocation, clipIsLooping):
        self.location = clipLocation
        self.isLooping = clipIsLooping
        
class Player:
    def __init__(self, init_layer=1, init_idleClip=None, init_autoIdle=False, init_volume=0.5):
        self.omx = None
        self.clip = None
        self.isStopping = False
        self.layer = init_layer
        self.setIdleClip(init_idleClip)
        self.autoIdle = init_autoIdle
        self.volumeSetting='--vol -6000'
        if init_volume == 0:
            self.volumeSetting=('--vol ' + str(ceil(2000 * (log10(init_volume)))))
        print(self.volumeSetting)
    
    # pre:
    # post: returns true if omx is not None
    def isPlaying(self):
        return self.omx is not None
    
    # pre: expects desired is of type Clip
    # post: sets the idle clip to be a looping version of the desired clip
    def setIdleClip(self, desired):
        if desired is not None:
            self.idleClip = Clip(desired.location, True) # TODO: ensure this doesnt pile up clips over time
        else:
            self.idleClip = None
        return self.idleClip
    
    # pre: expects desired to be of type boolean
    # post: sets the auto idle option to the desired value
    def setAutoIdle(self, desired):
        self.autoIdle = desired
        return self.autoIdle
    
    def isIdle(self):
        return (self.clip == self.idleClip)
    
    def playIdle(self):
        self.play(self.idleClip)
        
    # pre:
    # post: stops the current clip and plays the desired clip
    def play(self, desiredClip):
        if (desiredClip is not None):
            if self.isPlaying():
                self.stop()
            self.clip = desiredClip
            if (self.clip.isLooping == False):
                self.omx = OMXPlayer(self.clip.location, args=['--layer', str(self.layer), '--no-osd', '--no-keys'])
            else:
                self.omx = OMXPlayer(self.clip.location, args=['--layer', str(self.layer), '--no-osd', '--no-keys', '--loop'])
            if (self.idleClip is not desiredClip):
                self.omx.exitEvent += lambda a, b: self.clipEndEvent() # will this assign multiple times?

    # pre: 
    # post: starts idling on the idleClip if autoIdle is true, otherwise stops playing the current clip
    def endClip(self):
        self.stop()
        if (self.autoIdle and self.idleClip is not None):
            self.play(self.idleClip)
                
    # pre: 
    # post: stops playing the current clip
    def stop(self):
        self.isStopping = True
        if self.isPlaying():
            self.omx.quit()
        self.clip = None
        self.omx = None
        self.isStopping = False
        
    # pre: 
    # post: resets the current position of the clip to its start
    def reset(self):
        self.omx.set_position(0)
        
    def clipEndEvent(self):
        print("clip end")
        self.omx = None
        if (self.isStopping is False):
            self.play(self.idleClip)
        