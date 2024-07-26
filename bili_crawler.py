# 导入requests库，用于发送HTTP请求
import requests
# 导入BeautifulSoup库，用于解析HTML文档
from bs4 import BeautifulSoup
# 导入json库，用于处理JSON格式的数据
import json
# 导入re库，用于正则表达式匹配
import re
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
video_name = input('请输入视频名称')
# 定义目标视频的URL
url = input('请输入你要下载视频的网址，例如“https://www.bilibili.com/video/BV1CF411L7PD”')
#url = 'https://www.bilibili.com/video/BV1CF411L7PD'这是一个例子

# 定义请求头，模拟浏览器访问
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Referer':'https://www.bilibili.com/'
}


# 发送GET请求，获取视频页面内容
res = requests.get(url,headers=header)


# 使用正则表达式匹配页面中包含视频信息的JavaScript变量
obj = re.compile(r'<script>window\.__playinfo__=(.*?)</script>',re.S)

# 从页面源码中提取视频信息JSON字符串
html_data = obj.findall(res.text)[0]



# 将JSON字符串解析为Python对象
json_data = json.loads(html_data)


# 从解析后的数据中获取视频流的URL
videos = json_data['data']['dash']['video']
video_url = videos[0]['baseUrl']
print('视频下载完成')

# 从解析后的数据中获取音频流的URL
audios = json_data['data']['dash']['audio']
audio_url = audios[0]['baseUrl']
print('音频下载完成')

# 发送GET请求，下载视频流
res1 = requests.get(video_url,headers=header)

# 将视频流内容写入本地文件
with open(video_name+'.mp4','wb') as f:
    f.write(res1.content)

# 发送GET请求，下载音频流
res2 = requests.get(audio_url,headers=header)

# 将音频流内容写入本地文件
with open(video_name+'.mp3','wb') as f:
    f.write(res2.content)

video_clip = VideoFileClip(video_name+'.mp4')
audio_clip = AudioFileClip(video_name+'.mp3')
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile(video_name+ "_merged.mp4", codec='libx264', audio_codec='aac')
