import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np
from newreverb import Freeverb

# 初始化pygame的混音器
pygame.mixer.init()

# 音频文件路径
audio_file = "E:/Olly Murs-That Girl.mp3"

# 创建Freeverb类的实例
freeverb_instance = Freeverb()

# 定义播放音频的函数
def play_audio():
    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"无法播放音频: {e}")

# 定义暂停音频的函数
def pause_audio():
    pygame.mixer.music.pause()

# 定义继续播放音频的函数
def unpause_audio():
    pygame.mixer.music.unpause()

# 更新UI背景颜色的函数
def update_background_color():
    try:
        r = int(red_scale.get())
        g = int(green_scale.get())
        b = int(blue_scale.get())
        color = f'#{r:02x}{g:02x}{b:02x}'
        settings_frame.config(bg=color)
        main_frame.config(bg=color)
        reverb_frame.config(bg=color)  # 更新新加的混响界面背景颜色
    except ValueError:
        messagebox.showerror("Error", "请输入有效的RGB值")

# 更新字体大小的函数
def update_font_size():
    try:
        size = int(font_size_entry.get())
        for frame in (main_frame, settings_frame, reverb_frame):
            for widget in frame.winfo_children():
                widget.config(font=("Arial", size))
    except ValueError:
        messagebox.showerror("Error", "请输入有效的字体大小")

# 切换到设置面板
def show_settings():
    settings_frame.pack(fill="both", expand=True)
    main_frame.pack_forget()

# 切换到混响面板
def show_reverb():
    reverb_frame.pack(fill="both", expand=True)
    main_frame.pack_forget()

# 返回初始面板
def show_main():
    main_frame.pack(fill="both", expand=True)
    settings_frame.pack_forget()
    reverb_frame.pack_forget()

# 更新Freeverb参数
def update_freeverb():
    freeverb_instance.update_Freeverb(
        dry=slider1.get(),
        damp=slider3.get(),
        wet=slider2.get(),
        roomsize=slider4.get(),
        stereospread=slider5.get(),
        gain=slider6.get(),
        width=slider7.get()
    )
    print("Parameters updated")

# 创建主窗口
root = tk.Tk()
root.title("音频播放器")
root.geometry("800x600")

# 创建主面板
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# 创建播放按钮
play_button = tk.Button(main_frame, text="播放", command=play_audio)
play_button.pack(pady=10)

# 创建暂停按钮
pause_button = tk.Button(main_frame, text="暂停", command=pause_audio)
pause_button.pack(pady=10)

# 创建继续播放按钮
unpause_button = tk.Button(main_frame, text="继续", command=unpause_audio)
unpause_button.pack(pady=10)

# 创建设置按钮
settings_button = tk.Button(main_frame, text="设置", command=show_settings)
settings_button.pack(pady=10)

# 创建混响按钮
reverb_button = tk.Button(main_frame, text="混响", command=show_reverb)
reverb_button.pack(pady=10)

# 创建设置面板
settings_frame = tk.Frame(root)

# 创建RGB颜色调节器
red_label = tk.Label(settings_frame, text="Red:")
red_label.pack()
red_scale = tk.Scale(settings_frame, from_=0, to=255, orient='horizontal', command=lambda x: update_background_color())
red_scale.pack()

green_label = tk.Label(settings_frame, text="Green:")
green_label.pack()
green_scale = tk.Scale(settings_frame, from_=0, to=255, orient='horizontal', command=lambda x: update_background_color())
green_scale.pack()

blue_label = tk.Label(settings_frame, text="Blue:")
blue_label.pack()
blue_scale = tk.Scale(settings_frame, from_=0, to=255, orient='horizontal', command=lambda x: update_background_color())
blue_scale.pack()

# 创建字体大小调节器
font_size_label = tk.Label(settings_frame, text="Font Size:")
font_size_label.pack()
font_size_entry = tk.Entry(settings_frame)
font_size_entry.pack()

update_font_button = tk.Button(settings_frame, text="Update Font Size", command=update_font_size)
update_font_button.pack(pady=10)

# 创建返回按钮
back_button = tk.Button(settings_frame, text="返回", command=show_main)
back_button.pack(pady=10)

# 创建混响面板
reverb_frame = tk.Frame(root)

# 创建7个滑轨
slider1_label = tk.Label(reverb_frame, text="dry")
slider1_label.grid(row=0, column=0, padx=5, pady=5)
slider1 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider1.grid(row=1, column=0, padx=5, pady=5)

slider2_label = tk.Label(reverb_frame, text="wet")
slider2_label.grid(row=0, column=1, padx=5, pady=5)
slider2 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider2.grid(row=1, column=1, padx=5, pady=5)

slider3_label = tk.Label(reverb_frame, text="damp")
slider3_label.grid(row=0, column=2, padx=5, pady=5)
slider3 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider3.grid(row=1, column=2, padx=5, pady=5)

slider4_label = tk.Label(reverb_frame, text="roomsize")
slider4_label.grid(row=0, column=3, padx=5, pady=5)
slider4 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider4.grid(row=1, column=3, padx=5, pady=5)

slider5_label = tk.Label(reverb_frame, text="stereospread")
slider5_label.grid(row=0, column=4, padx=5, pady=5)
slider5 = tk.Scale(reverb_frame, from_=0, to=100, orient='vertical')
slider5.grid(row=1, column=4, padx=5, pady=5)

slider6_label = tk.Label(reverb_frame, text="gain")
slider6_label.grid(row=0, column=5, padx=5, pady=5)
slider6 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider6.grid(row=1, column=5, padx=5, pady=5)

slider7_label = tk.Label(reverb_frame, text="width")
slider7_label.grid(row=0, column=6, padx=5, pady=5)
slider7 = tk.Scale(reverb_frame, from_=0, to=1, orient='vertical', resolution=0.01)
slider7.grid(row=1, column=6, padx=5, pady=5)

# 创建返回按钮
back_button_reverb = tk.Button(reverb_frame, text="返回", command=show_main)
back_button_reverb.grid(row=2, columnspan=7, pady=10)

# 创建播放处理后音频按钮
play_processed_button = tk.Button(reverb_frame, text="播放处理后音频", command=play_audio)
play_processed_button.grid(row=3, columnspan=7, pady=10)

# 创建更新按钮
update_freeverb_button = tk.Button(reverb_frame, text="Update", command=update_freeverb)
update_freeverb_button.grid(row=4, columnspan=7, pady=10)

# 运行主循环
main_frame.pack(fill="both", expand=True)
root.mainloop()
