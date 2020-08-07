from time import sleep
import subprocess

class ImageController:
    def __init__(self, init_imageLocation=None):
        self.location = init_imageLocation
        self.isDisplaying = False
        self.process = 0
    
    def setImage(self, newImageLocation):
        if not self.isDisplaying:
            self.location = newImageLocation
        return self.location
    
    def display(self, newImageLocation=None):
        if not self.isDisplaying:
            if newImageLocation != None:
                self.location = newImageLocation
            if self.location != None:
                self.process = subprocess.Popen(["feh", "--hide-pointer", "-x", "-Z", "-q", "-B", "black", "-F", self.location])
                self.isDisplaying = True
        return self.isDisplaying
    
    def stop(self):
        if self.isDisplaying:
            self.process.kill()
            self.isDisplaying = False
        return self.isDisplaying

