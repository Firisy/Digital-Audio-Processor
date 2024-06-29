import pyaudio
import wave

p=pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))


for i in range(p.get_device_count()):  
    info = p.get_device_info_by_index(i)  
    if info["maxOutputChannels"] > 0:  
        print("Device index {} - {}".format(i, info))

# Select the device with sound
device_index = 1  # Replace i with the desired device index

# Set the desired audio parameters
format = pyaudio.paInt16
channels = 2
sample_rate = 44100
chunk_size = 1024

# Open the audio stream
stream = p.open(format=format,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size,
                input_device_index=device_index)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

with wave.open('output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK))
    print('Done')

    stream.close()
    p.terminate()