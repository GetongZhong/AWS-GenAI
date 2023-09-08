import pyaudio
import wave
import subprocess

# 配置音频流参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILENAME = "output.mp3"

# 初始化PyAudio
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("开始录制音频...")

# 创建一个WAV文件
frames = []

# 从音频流中读取数据并保存到frames列表中
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录制完成！")

# 停止音频流
stream.stop_stream()
stream.close()

# 终止PyAudio
p.terminate()

# 创建一个WAV文件并将frames中的音频数据写入其中
wf = wave.open("temp.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("保存临时WAV文件成功！")

# 使用subprocess调用LAME库将WAV文件转换为MP3文件
subprocess.call(['lame', '-V2', 'temp.wav', OUTPUT_FILENAME])

print("保存MP3文件成功！")