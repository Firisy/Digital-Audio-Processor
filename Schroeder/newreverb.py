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
    
class SATREV:
    def __init__(self) -> None:    
        self.FBCF_delay=[901,778,1011,1123]
        self.FBCF_g=[0.8051,0.8277,0.7830,0.7643]
        self.b=[1]
        self.FBCF_a=[np.zeros(delay+1) for delay in self.FBCF_delay]
        for i in range(len(self.FBCF_a)):
            self.FBCF_a[i][0] = 1
            self.FBCF_a[i][-1] = -self.FBCF_g[i]

        self.FBCFLs =[filter(self.b,a) for a in self.FBCF_a]
        self.FBCFRs =[filter(self.b,a) for a in self.FBCF_a]


        self.AP_delay=[125,42,12]
        self.AP_g=[0.7,0.7,0.7]
        self.AP_b=[np.zeros(delay+1) for delay in self.AP_delay]
        self.AP_a=[np.zeros(delay+1) for delay in self.AP_delay]
        for i in range(len(self.AP_b)):
            self.AP_b[i][0] = -self.AP_g[i]
            self.AP_b[i][-1] = 1
        for i in range(len(self.AP_a)):
            self.AP_a[i][0] = 1
            self.AP_a[i][-1] = -self.AP_g[i]
        self.APLs=[filter(self.AP_b[i],self.AP_a[i])for i in range(len(self.AP_b))]
        self.APRs=[filter(self.AP_b[i],self.AP_a[i])for i in range(len(self.AP_b))]

    def process(self,input):
        output = np.zeros_like(input)

        for FBCFL in self.FBCFLs:
            output[:,0] +=FBCFL.process(input[:,0])
        for FBCFR in self.FBCFRs:
            output[:,1] +=FBCFR.process(input[:,1])

        for APL in self.APLs:
            output[:,0] =APL.process(output[:,0])
        for APR in self.APRs:
            output[:,1] =APR.process(output[:,1])

        return output
    
class JCREV:
    def __init__(self) -> None:    
        self.MM=np.array[[1,1,1,1],[-1,-1,-1,-1],[-1,1,-1,1],[1,-1,1,-1]]
        self.FBCF_delay=[1687,1601,2053,2251]
        self.FBCF_g=[0.773,0.802,0.753,0.733]
        self.b=[1]
        self.FBCF_a=[np.zeros(delay+1) for delay in self.FBCF_delay]
        for i in range(len(self.FBCF_a)):
            self.FBCF_a[i][0] = 1
            self.FBCF_a[i][-1] = -self.FBCF_g[i]

        self.FBCFLs =[filter(self.b,a) for a in self.FBCF_a]
        self.FBCFRs =[filter(self.b,a) for a in self.FBCF_a]


        self.AP_delay=[347,113,37]
        self.AP_g=[0.7,0.7,0.7]
        self.AP_b=[np.zeros(delay+1) for delay in self.AP_delay]
        self.AP_a=[np.zeros(delay+1) for delay in self.AP_delay]
        for i in range(len(self.AP_b)):
            self.AP_b[i][0] = -self.AP_g[i]
            self.AP_b[i][-1] = 1
        for i in range(len(self.AP_a)):
            self.AP_a[i][0] = 1
            self.AP_a[i][-1] = -self.AP_g[i]
        self.APLs=[filter(self.AP_b[i],self.AP_a[i])for i in range(len(self.AP_b))]
        self.APRs=[filter(self.AP_b[i],self.AP_a[i])for i in range(len(self.AP_b))]

    def process(self,input):
        output = np.zeros_like(input)

        for APL in self.APLs:
            input[:,0] =APL.process(input[:,0])
        for APR in self.APRs:
            input[:,1] =APR.process(input[:,1])

        for FBCFL in self.FBCFLs:
            output[:,0] +=FBCFL.process(input[:,0])
        for FBCFR in self.FBCFRs:
            output[:,1] +=FBCFR.process(input[:,1])

        return output
    
class Freeverb:
    def __init__(self,dry=0.,damp=0.5,wet=1/3.0,roomsize=0.5,stereospread=23,gain=0.015,width=1,AP_g=0.5) -> None:    
        """
        参数:
        - dry (float): 干信号的级别。默认值为0。
        - damp (float): 阻尼因子。默认值为0.5。
        - wet (float): 湿信号的级别。默认值为1/3.0。
        - roomsize (float): 房间大小因子。默认值为0.5。
        - stereospread (int): 立体声扩展值。默认值为23。
        - gain (float): 增益因子。默认值为0.015。
        - width (int): 宽度因子。默认值为1。
        """
        self.roomsize=roomsize*0.28+0.7
        self.damp=damp*0.4
        self.stereospread=stereospread
        self.AP_g=AP_g
        self.gain=gain
        self.dry=dry*2
        self.width=width
        self.wet=wet*3
        self.wet1 = self.wet*(self.width/2+0.5)
        self.wet2 = self.wet*((1-self.width)/2)
        self.wetmat = np.array([[self.wet1, self.wet2], [self.wet2, self.wet1]])  

        self.LBCF_delay=[1557,1617,1491,1422,1277,1356,1188,1116]

        self.LBCFL_b=[np.zeros(delay+2) for delay in self.LBCF_delay]
        self.LBCFL_a=[np.zeros(delay+1) for delay in self.LBCF_delay]
        for i in range(8):
            self.LBCFL_b[i][-2] = 1
            self.LBCFL_b[i][-1] = -self.damp
        for i in range(8):
            self.LBCFL_a[i][0] = 1
            self.LBCFL_a[i][1] = -self.damp
            self.LBCFL_a[i][-1] = -self.roomsize*(1-self.damp)

        self.LBCFLs =[filter(self.LBCFL_b[i],self.LBCFL_a[i]) for i in range(8)]
        
        self.LBCFR_b=[np.zeros(delay+2+stereospread) for delay in self.LBCF_delay]
        self.LBCFR_a=[np.zeros(delay+1+stereospread) for delay in self.LBCF_delay]
        
        for i in range(8):
            self.LBCFR_b[i][-2] = 1
            self.LBCFR_b[i][-1] = -self.damp
        for i in range(8):
            self.LBCFR_a[i][0] = 1
            self.LBCFR_a[i][1] = -self.damp
            self.LBCFR_a[i][-1] = -self.roomsize*(1-self.damp)
        
        self.LBCFRs =[filter(self.LBCFR_b[i],self.LBCFR_a[i]) for i in range(8)]


        self.AP_delay=[556, 441, 341, 225]

        self.APL_b=[np.zeros(delay+1) for delay in self.AP_delay]
        self.APL_a=[np.zeros(delay+1) for delay in self.AP_delay]
        for i in range(4):
            self.APL_b[i][0] = -self.AP_g
            self.APL_b[i][-1] = 1
        for i in range(4):
            self.APL_a[i][0] = 1
            self.APL_a[i][-1] = -self.AP_g

        self.APLs =[filter(self.APL_b[i],self.APL_a[i]) for i in range(4)]
        
        self.APR_b=[np.zeros(delay+1+stereospread) for delay in self.AP_delay]
        self.APR_a=[np.zeros(delay+1+stereospread) for delay in self.AP_delay]
        
        for i in range(4):
            self.APR_b[i][0] = -self.gain
            self.APR_b[i][-1] = 1
        for i in range(4):
            self.APR_a[i][0] = 1
            self.APR_a[i][-1] = -self.gain
        
        self.APRs =[filter(self.APR_b[i],self.APR_a[i]) for i in range(4)]
    
    def process(self,input):
        output = np.zeros_like(input)
        deal_input = np.array([input[i][0] + input[i][1] for i in range(len(input))])*self.gain
        for LBCFL in self.LBCFLs:
            output[:,0] += LBCFL.process(deal_input)
        for LBCFR in self.LBCFRs:
            output[:,1] += LBCFR.process(deal_input)

        for APL in self.APLs:
            output[:,0] = APL.process(output[:,0])
        for APR in self.APRs:
            output[:,1] = APR.process(output[:,1])
        self.output = (input * self.dry) + np.dot(output,self.wetmat) 
        return output


        

