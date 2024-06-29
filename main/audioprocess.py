import pyaudio  
import numpy as np   
import time  
# 其他的PyAudio设置...    
  
import numpy as np 
import sys 
  
def callback(in_data, frame_count, time_info, status_flags):   
    # 处理音频数据
    out_data = process(in_data)
    return (out_data, pyaudio.paContinue)  

  
# 其他设置...  
p=pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
device_index = 0

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        if 'default' in p.get_device_info_by_host_api_device_index(0, i).get('name'):
            device_index = i

# Set the desired audio parameters
format = pyaudio.paInt16
channels = 2
sample_rate = 44100
chunk_size = 10000

# Open the audio stream
stream = p.open(format=format,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                start=True,
                frames_per_buffer=chunk_size,
                input_device_index=device_index,
                stream_callback=callback)

print("开始录音和播放...")    
  
try:  
    while stream.is_active(): 
        time.sleep(0.1)  
except KeyboardInterrupt:  
    pass  
  
print("停止录音和播放...")  
  
# 停止录音和播放流  
stream.stop_stream()  
stream.close()  
  
p.terminate()  
sys.exit(0)