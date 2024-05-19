import numpy as np  
import matplotlib.pyplot as plt  
from freeverb import Freeverb
  
# 创建单位冲激信号  
impulse = np.zeros((44100, 2))
impulse[0,0] = 1  # 在t=0时刻赋值为1  
impulse[0,1] = 1

# 创建Freeverb对象
freeverb = Freeverb()
freeverb.processmix(impulse)
 
# 计算冲激响应  
impulse_response = freeverb.output[:,0]
# 计算频率响应  
frequency_response = np.fft.fft(impulse_response)  
  
# 计算幅度和相位  
magnitude = np.abs(frequency_response)  
phase = np.angle(frequency_response)  
  
# 绘制结果
plt.figure()  # 设置整体图的尺寸  

plt.figure()  
plt.subplot(3, 1, 1)  
plt.plot(impulse_response)  
plt.title('Impulse Response') 
plt.xlim(0, 10000) 
  
plt.subplot(3, 1, 2)  
plt.plot(magnitude)  
plt.title('Magnitude Response')  
plt.xscale('log')
plt.xlim(20, 20000)
  
plt.subplot(3, 1, 3)  
plt.plot(phase)  
plt.title('Phase Response')  
plt.xscale('log')
plt.xlim(20, 20000) 

plt.tight_layout(pad=1.0)  # 增加子图之间的间距
plt.show()  