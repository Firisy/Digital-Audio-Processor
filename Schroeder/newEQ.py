import numpy as np
import scipy.signal as signal

class filter:
    def __init__(self,b,a) -> None:
        self.b=b
        self.a=a
        self.zi = signal.lfiltic(self.b,self.a,[0])
    
    def process(self,input):
        output,self.zi=signal.lfilter(self.b,self.a,input,axis=-1,zi=self.zi)
        return output
    
    def update_filter(self,b,a):
        self.b = b
        self.a = a

class BandPass:
    def __init__(self,lowpass=20,highpass=20000,order=5, samplerate=44100) -> None:
        self.lowpass = lowpass
        self.highpass = highpass
        self.order = order
        self.samplerate = samplerate
        self.b,self.a=signal.butter(self.order, [self.lowpass,self.highpass], btype='bandpass', fs=self.samplerate)
        self.bandpass = filter(self.b,self.a)
    
    def process(self,input):
        return self.bandpass.process(input)
    
    def update_bandpass(self,lowpass,highpass):
        self.lowpass = lowpass
        self.highpass = highpass
        self.b,self.a=signal.butter(self.order, [self.lowpass,self.highpass], btype='bandpass', fs=self.samplerate)
        self.bandpass.update_filter(self.b,self.a)