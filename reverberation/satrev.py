import numpy as np  
import matplotlib.pyplot as plt  
import reverberation as rvb
  
# 创建单位冲激信号  
impulse = np.zeros(441000)  
impulse[0] = 1  # 在t=0时刻赋值为1  

impulse_do=rvb.Reverberation(impulse)
delay_samples = 4799  # 延迟100个样本
gain = 0.7  # 增益为0.5  
# 应用单位冲激信号到函数中  
impulse_do.SATREV()  # 假设feedback_combfilter是你的函数  
 
# 计算冲激响应  
impulse_response = impulse_do.delayed_samples 
# 计算频率响应  
frequency_response = np.fft.fft(impulse_response)  
  
# 计算幅度和相位  
magnitude = np.abs(frequency_response)  
phase = np.angle(frequency_response)  
  
# 绘制结果
plt.figure(figsize=(10, 8))  # 设置整体图的尺寸  

plt.figure()  
plt.subplot(3, 1, 1)  
plt.plot(impulse_response)  
plt.title('Impulse Response') 
plt.xlim(0, 6000) 
  
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