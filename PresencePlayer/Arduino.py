import serial
import RPi.GPIO as GPIO
import time

class Arduino:
    def __init__(self, targetDistance=100, historySize=1):
        self.targetDistance = targetDistance
        self.distanceHistory = [False] * historySize
        self.historySize = historySize
        self.currHistoryIndex = 0
        self.prevMotion = 0
        self.currMotion = 0
        self.currProximity = 0
        self.establishConnection()
        print(historySize)
        
    def establishConnection(self):
        self.ser = serial.Serial("/dev/ttyACM0",9600)
        self.ser.baudrate = 9600
        
    def update(self):
        self.ser.write(b'3')
        time.sleep(0.1)
        while self.ser.inWaiting() > 0:
            pir_line = self.ser.readline()
            dist_line = self.ser.readline()
            try:
                pir_read = int(pir_line.decode().strip('\r\n'))
                dist_read = int(dist_line.decode().strip('\r\n'))
            except:
                pritnt("Error decoding arduino values, likely ValueError: invalid literal for int() with base 10")
            self.prevMotion = self.currMotion
            self.currMotion = pir_read
            self.currProximity = dist_read
            self.distanceHistory[self.currHistoryIndex] = (self.detectingProximity())
            self.currHistoryIndex = ((self.currHistoryIndex + 1) % self.historySize)
            ## the following were used for debugging
            #print(self.distanceHistory)
            #print(str(self.prevMotion) + " " + str(self.currMotion) + " " + str(self.currProximity))
            
    def detectingMotion(self):
        return (self.currMotion is not 0)
    
    def detectedNewMotion(self):
        return ((self.currMotion is not 0) and (self.prevMotion is 0))
    
    def detectingProximity(self):
        return (self.currProximity > self.targetDistance)
    
    def detectedProximityRecently(self):
        return (True in self.distanceHistory)