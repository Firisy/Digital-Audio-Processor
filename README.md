# Digital-Audio-Processor
 ZJU23-24SignalProcessCourseExperiment
## 文件解释
```
├─denoiser  # 使用meta的denoiser工具编写的降噪
├─reverberation # 2024-5-16前编写的无实时处理，时间复杂度较高的混响
│    └─freeverb.py # 时间复杂度较高的freeverb混响
│    └─reverberation.py # 梳状滤波器和基础的schroeder混响模型
└─Schroeder # 有实时功能
    └─newreverb.py # 2024-5-18 编写的有实时处理功能的混响模型，具体调用见剩余文件
```
