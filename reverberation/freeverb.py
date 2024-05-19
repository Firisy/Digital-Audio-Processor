import numpy as np
from comb import comb
from allpass import allpass

class Freeverb:
    def __init__(self):
        self.__numcombs = 8
        self.__numallpasses = 4
        self.__muted = 0
        self.__fixedgain = 0.015
        self.__scalewet = 3
        self.__scaledry = 2
        self.__scaledamp = 0.4
        self.__scaleroom = 0.28
        self.__offsetroom = 0.7
        
        self.__initialroom = 0.5
        self.__initialdamp = 0.5
        self.__initialwet = 1 / self.__scalewet
        self.__initialdry = 0
        self.__initialwidth = 1
        self.__initialmode = 0
        self.__freezemode = 0.5
        self.__stereospread = 23

        self.combsize = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
        self.allpasssize = [556, 441, 341, 225]

        self.__bufcombL = [None] * len(self.combsize)
        self.__bufcombR = [None] * len(self.combsize)
        for i in range(self.__numcombs):
            self.__bufcombL[i] = np.zeros(self.combsize[i])
            self.__bufcombR[i] = np.zeros(self.combsize[i]+self.__stereospread)
        
        self.__combLs = [comb(self.combsize[i], 0.84, 0.2,self.__bufcombL[i]) for i in range(self.__numcombs)]
        self.__combRs = [comb(self.combsize[i]+self.__stereospread, 0.84, 0.2,self.__bufcombR[i]) for i in range(self.__numcombs)]
        
        
        self.__bufallpassL = [None] * len(self.allpasssize)
        self.__bufallpassR = [None] * len(self.allpasssize)
        for i in range(self.__numallpasses):
            self.__bufallpassL[i] = np.zeros(self.allpasssize[i])
            self.__bufallpassR[i] = np.zeros(self.allpasssize[i]+self.__stereospread)
        
        self.__allpassLs = [allpass(self.allpasssize[i], 0.5, self.__bufallpassL[i]) for i in range(self.__numallpasses)]
        self.__allpassRs = [allpass(self.allpasssize[i]+self.__stereospread, 0.5, self.__bufallpassR[i]) for i in range(self.__numallpasses)]

        self.__gain = self.__fixedgain
        self.__roomsize = (self.__initialroom*self.__scaleroom)+self.__offsetroom
        self.__roomsize1 = self.__roomsize
        self.__damp = self.__initialdamp*self.__scaledamp
        self.__damp1 = self.__damp
        self.__wet = self.__scalewet*self.__initialwet
        
        self.__width = self.__initialwidth
        
        self.__wet1 = self.__wet * (self.__width / 2 + 0.5)
        self.__wet2 = self.__wet * ((1 - self.__width) / 2)
        
        self.__dry = self.__scaledry*self.__initialdry
        self.__mode = self.__initialmode

        self.output = []
    
    
    
    def set_roomsize(self, value):
        self.__roomsize = (value * self.__scaleroom) + self.__offsetroom
        self.update()

    def get_roomsize(self):
        return (self.__roomsize - self.__offsetroom) / self.__scaleroom

    def set_damp(self, value):
        self.__damp = value * self.__scaledamp
        self.update()

    def get_damp(self):
        return self.__damp / self.__scaledamp

    def set_wet(self, value):
        self.__wet = value * self.__scalewet
        self.update()

    def get_wet(self):
        return self.__wet / self.__scalewet

    def set_dry(self, value):
        self.__dry = value * self.__scaledry

    def get_dry(self):
        return self.__dry / self.__scaledry

    def set_width(self, value):
        self.__width = value
        self.update()

    def get_width(self):
        return self.__width
    
    def set_mode(self, value):
        self.__mode = value
        self.update()

    def get_mode(self):
        return 1 if self.__mode >= self.__freezemode else 0
    
    def update(self):
        # Recalculate internal values after parameter change
        self.__wet1 = self.__wet * (self.__width / 2 + 0.5)
        self.__wet2 = self.__wet * ((1 - self.__width) / 2)
    
        if self.__mode >= self.__freezemode:
            self.__roomsize1 = 1
            self.__damp1 = 0
            self.__gain = self.__muted
        else:
            self.__roomsize1 = self.__roomsize
            self.__damp1 = self.__damp
            self.__gain = self.__fixedgain
    
        for i in range(self.__numcombs):
            self.__combLs[i].setfeedback(self.__roomsize1)
            self.__combRs[i].setfeedback(self.__roomsize1)
    
        for i in range(self.__numcombs):
            self.__combLs[i].setdamp(self.__damp1)
            self.__combRs[i].setdamp(self.__damp1)


    def processmix(self, inputLR):
        # Process left and right channels
        self.output = np.zeros_like(inputLR)
        for i in range(inputLR.shape[0]):
            outL = 0
            outR = 0
            input = (inputLR[i,0]+inputLR[i,1])*self.__gain

            for j in range(self.__numcombs):
                outL += self.__combLs[j].process(input)
                outR += self.__combRs[j].process(input)

            for j in range(self.__numallpasses):
                outL = self.__allpassLs[j].process(outL)
                outR = self.__allpassRs[j].process(outR)
            
            self.output[i,0] += (input * self.__dry) + (outL * self.__wet1) + (outR * self.__wet2)
            self.output[i,1] += (input * self.__dry) + (outR * self.__wet1) + (outL * self.__wet2)
    
    def processreplace(self, inputLR):
        # Process left and right channels
        self.output = np.zeros_like(inputLR)
        for i in range(inputLR.shape[0]):
            outL = 0
            outR = 0
            input = (inputLR[i,0]+inputLR[i,1])*self.__gain

            for j in range(self.__numcombs):
                outL += self.__combLs[j].process(input)
                outR += self.__combRs[j].process(input)
                
            for j in range(self.__numallpasses):
                outL = self.__allpassLs[j].process(outL)
                outR = self.__allpassRs[j].process(outR)
            
            self.output[i,0] = (input * self.__dry) + (outL * self.__wet1) + (outR * self.__wet2)
            self.output[i,1] = (input * self.__dry) + (outR * self.__wet1) + (outL * self.__wet2)