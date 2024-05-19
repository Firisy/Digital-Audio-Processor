import numpy as np
from undenormalise import undenormalise
class comb:
    def __init__(self,size,feedback,damp,setbuffer=None):
        self.__feedback = feedback
        self.__filterstore = 0
        self.__damp1=damp
        self.__damp2=1-damp
        self.buffer = setbuffer if setbuffer is not None else np.zeros(size)
        self.__bufidx = 0
        self.__bufsize = size
    
    def process(self,input):
        output = self.buffer[self.__bufidx]
        output = undenormalise(output)
        
        self.__filterstore = (output * self.__damp2) + (self.__filterstore * self.__damp1)
        self.__filterstore = undenormalise(self.__filterstore)

        self.buffer[self.__bufidx] = input + (self.__filterstore * self.__feedback)
        
        self.__bufidx = (self.__bufidx + 1) % self.__bufsize
        
        return output
    
    def setfeedback(self,feedback):
        self.__feedback = feedback
    
    def setdamp(self,damp):
        self.__damp1 = damp
        self.__damp2 = 1-damp