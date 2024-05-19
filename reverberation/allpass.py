import numpy as np
from undenormalise import undenormalise

class allpass:
    def __init__(self,size,feedback,setbuffer=None):
        self.__feedback = feedback
        self.buffer = setbuffer if setbuffer is not None else np.zeros(size)
        self.__bufidx = 0
        self.__bufsize = size

    def process(self,input):
        bufout = self.buffer[self.__bufidx]
        bufout = undenormalise(bufout)
        
        output = -input + bufout
        
        self.buffer[self.__bufidx] = input + (bufout * self.__feedback)
        
        self.__bufidx = (self.__bufidx + 1) % self.__bufsize
        
        return output
    
    def setfeedback(self,feedback):
        self.__feedback = feedback