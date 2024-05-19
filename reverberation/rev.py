import numpy as np
import scipy.signal as signal


class Reverberation:
    # 定义延迟线函数，处理立体声信号
    def __init__(self, samples, samplerate=44100):
        self.samples = samples
        self.samplerate = samplerate
        self.num_channels = 1 if len(self.samples.shape) == 1 else self.samples.shape[1]
        self.delay_line = []
        self.delayed_samples = []
        self.dealing_samples = samples

    # FeedForward Comb Filter
    def echo(self, delay_samples, gain):
        self.delay_line = np.zeros((delay_samples, self.num_channels))
        self.delayed_samples = np.zeros_like(self.dealing_samples)
        ptr = 0
        for i in range(self.dealing_samples.shape[0]):
            self.delayed_samples[i] = self.dealing_samples[i] + gain * self.delay_line[ptr]
            self.delay_line[ptr] = self.dealing_samples[i]
            ptr = (ptr + 1) % delay_samples
        # if ptr != 0:
        #    self.delayed_samples = np.append(self.delayed_samples, self.delay_line[ptr:],axis=0)

    
    def feedback_combfilter(self, delay_samples, gain):
        self.delay_line = np.zeros((delay_samples, self.num_channels))
        self.delayed_samples = np.zeros_like(self.dealing_samples)
        ptr = 0
        for i in range(self.dealing_samples.shape[0]):
            self.delayed_samples[i] = self.dealing_samples[i] + gain * self.delay_line[ptr]
            self.delay_line[ptr] = self.delayed_samples[i]
            ptr = (ptr + 1) % delay_samples
        # if ptr != 0:
        #    self.delayed_samples = np.append(self.delayed_samples, self.delay_line[:ptr],axis=0)
    def FFCF(self,N,gain):
        self.delayed_samples = np.zeros_like(self.dealing_samples)
        b = np.zeros(N+1)
        b[0], b[N] = 1, gain
        a = [1]
        if self.num_channels == 1:
            self.delayed_samples = signal.lfilter(b,a,self.dealing_samples)
        else:
            for i in range(self.num_channels):
                self.delayed_samples[:,i] = signal.lfilter(b,a,self.dealing_samples[:,i])
    
    def FBCF(self,N,gain):
        self.delayed_samples = np.zeros_like(self.dealing_samples)
        b = [1]
        a = np.zeros(N+1)
        a[0], a[N] = 1, -gain
        if self.num_channels == 1:
            self.delayed_samples = signal.lfilter(b,a,self.dealing_samples)
        else:
            for i in range(self.num_channels):
                self.delayed_samples[:,i] = signal.lfilter(b,a,self.dealing_samples[:,i])
    
    def allpass_filter(self,N,g):
        self.echo(N,-1/g)
        self.dealing_samples=(-g)*self.delayed_samples
        self.feedback_combfilter(N,g)

    def AP(self,N,g):
        self.delayed_samples = np.zeros_like(self.dealing_samples)
        b = np.zeros(N+1)
        b[0], b[N] = -g, 1
        a = np.zeros(N+1)
        a[0], a[N] = 1, -g
        if self.num_channels == 1:
            self.delayed_samples = signal.lfilter(b,a,self.dealing_samples)
        else:
            for i in range(self.num_channels):
                self.delayed_samples[:,i] = signal.lfilter(b,a,self.dealing_samples[:,i])
    def HP(self):
        order = 4  # 滤波器阶数 
        # 采样频率  
        fs = self.samplerate  # 44.1 kHz  
        # 截止频率  
        fc = 5 # 10 Hz 
        b, a = signal.butter(order, fc/(0.5*fs), btype='high', analog=False)  
        self.delayed_samples = signal.lfilter(b, a, self.dealing_samples)       