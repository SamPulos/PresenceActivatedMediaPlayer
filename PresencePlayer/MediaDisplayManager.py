from ImageController import ImageController
from VideoPlayer import Clip, Player

class MediaDisplayManager:
    def __init__(self, init_imageDisplayDuration):
        # note: image display duration is in number of updates (should be proportional to pollrate and display duration in config
        self.imageDisplayDuration = init_imageDisplayDuration * 1000
        self.countdown = self.imageDisplayDuration * 1000
        self.videoDisplay = Player(init_layer=1)
        self.imageDisplay = ImageController()
        self.currMedia = None
        self.mediaRequiresCountdown = False # used to remove repeated string check in update()
        
    def update(self):
        if (self.mediaRequiresCountdown):
            if (self.countdown > 0):
                self.countdown = self.countdown - 1
            if (self.countdown <= 0):
                self.stop()

    def isVideo(self, path):
        return path.endswith(".mp4")

    def isImage(self, path):
        return (path.endswith(".jpg") or path.endswith(".png"))
    
    def isDisplaying(self):
        return (self.videoDisplay.isPlaying() or self.imageDisplay.isDisplaying)
        
    def display(self, newMedia):
        print("Attempting to display " + newMedia)
        self.currMedia = newMedia
        self.countdown = self.imageDisplayDuration
        self.mediaRequiresCountdown = self.isImage(self.currMedia)
        if (self.isVideo(self.currMedia)):
            self.videoDisplay.play(Clip(self.currMedia, False))
        elif (self.isImage(self.currMedia)):
            self.imageDisplay.display(self.currMedia)
        else:
            print("Tried to play invalid media " + newMedia)
        
    def stop(self):
        self.videoDisplay.stop()
        self.imageDisplay.stop()
        self.currMedia = None
        self.mediaRequiresCountdown = False
        
        
        
        
        