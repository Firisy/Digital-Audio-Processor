import numpy as np
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt

# audio1 = ipd.Audio(input_filename)
# ipd.display(audio1)

# 定义FBCF滤波器
N=1000
b = [1]
a = np.zeros(N+1)
a[0], a[N] = 1, -0.8
sos=signal.tf2sos(b,a)

impulse = np.zeros(44100)  
impulse[0] = 1  # 在t=0时刻赋值为1  


# 计算冲激响应  
impulse_response =signal.sosfilt(sos, impulse)
# 计算频率响应  
frequency_response = np.fft.fft(impulse_response)  
  
# 计算幅度和相位  
magnitude = np.abs(frequency_response)  
phase = np.angle(frequency_response)  
  
# 绘制结果
plt.figure(figsize=(30, 8))  # 设置整体图的尺寸  

plt.subplot(3, 1, 1)  
plt.plot(impulse_response)  
plt.title('Impulse Response') 
plt.xlim(0, 10000) 
  
plt.subplot(3, 1, 2)  
plt.plot(magnitude)  
plt.title('Magnitude Response')  
plt.xlim(0, 1000) 
  
plt.subplot(3, 1, 3)  
plt.plot(phase)  
plt.title('Phase Response')  
plt.xlim(0, 1000) 

plt.tight_layout(pad=1.0)  # 增加子图之间的间距
plt.show()  

print(sos.shape)