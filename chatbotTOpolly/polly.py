from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
import boto3, requests, base64, os, fnmatch, sys, subprocess

class TextToVideo:
    def __init__(self, bucket_name, webui_url, voice_id):
        self.bucket_name = bucket_name
        self.webui_url = webui_url
        self.voice_id = voice_id
        self.s3 = boto3.client("s3")
        self.polly = boto3.client("polly")
    
    def download(self, file_name, output_path):
        try:
            self.s3.download_file(self.bucket_name, file_name, output_path)
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)
        print(f"Download to {output_path}")
    
    def download_to_tmp(self, file_name, output_file_name):
        output_path = os.path.join(gettempdir(), output_file_name)
        try:
            self.s3.download_file(self.bucket_name, file_name, output_path)
            return output_path
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)
        print(f"Download to {output_path}")
    
    def tts(self, txt, output_file_name):
        try:
            response = self.polly.synthesize_speech(Text=txt, OutputFormat="mp3", VoiceId=self.voice_id)
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), output_file_name)
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        self.s3.upload_file(output, self.bucket_name, output_file_name)
                        s3_output_link = f"s3://{self.bucket_name}/{output_file_name}"
                        print(f"Written to {s3_output_link}")
                        return output_file_name
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        else:
            print("could not stream audio")
            sys.exit(-1)

    def gen_img(self, prompt, neg_prompt, output_file_name):
        # webui example: https://346f3750a6a0bc47f8.gradio.live/
        url = self.webui_url + 'sdapi/v1/txt2img'
        data = '{"prompt":"' + prompt + '", "negative_prompt":"' + neg_prompt + '", "width":256, "height":256}'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=data)
        img_64 = response.json()['images'][0]
        img_data = base64.b64decode(img_64)
        # output = os.path.join(gettempdir(), output_file_name)
        try:
            with open(output_file_name, "wb") as file:
                file.write(img_data)
                # self.s3.upload_file(output, self.bucket_name, output_file_name)
                # s3_output_link = f"s3://{self.bucket_name}/{output_file_name}"
                # print(f"Written to {s3_output_link}")
                print(f"Written to {output_file_name}")
                return output_file_name
        except IOError as error:
            print(error)
            sys.exit(-1)
            
    def find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def gen_sad_talker(self, audio_path, img_path, output_file_name):
        # 绝对路径
        output_dir = os.path.join(gettempdir(), "result/")
        os.chdir('/root/stable-diffusion-webui/extensions/SadTalker')
        ret = os.system('python inference.py --enhancer gfpgan --driven_audio ' + audio_path + ' --source_image ' + img_path + ' --result_dir ' + output_dir)
        if ret == 0:
            mp4_list = self.find('*.mp4', output_dir)
            if len(mp4_list) == 0:
                print('output mp4 file not found')
                sys.exit(-1)
            else:
                output = mp4_list[0]
                print(output)
                self.s3.upload_file(output, self.bucket_name, output_file_name)
                s3_output_link = f"s3://{self.bucket_name}/{output_file_name}"
                print(f"Written to {s3_output_link}")
                return output_file_name
        else:
            print('sadtalker error')
            sys.exit(-1)
    
    def ttv(self, prompt, neg_prompt, transcript):
        self.clear_tmp()
        audio_s3 = self.tts(transcript, "audio.mp3")
        audio_local = self.download_to_tmp(audio_s3, "audio.mp3")
        img_s3 = self.gen_img(prompt, neg_prompt, "img.png")
        img_local = self.download_to_tmp(img_s3, "img.png")
        result_s3 = self.gen_sad_talker(audio_local, img_local, "result.mp4")
        return result_s3
    
    def clear_tmp(self):
        try:
            for root, dirs, files in os.walk(gettempdir()):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            print('/tmp cleared')
        except OSError:
            print('error clearing tmp')
            sys.exit(-1)
    
    def set_voice_id(self, voice_id):
        self.voice_id = voice_id
        