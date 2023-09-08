import gradio as gr
import boto3
import time
import json

def transcribe(audio):
    # 使用Amazon Transcribe服务进行音频转录的代码逻辑保持不变

    # 为了简化，我们将直接使用audio文件路径，而不是先上传到S3
    # 创建一个 Amazon Transcribe 转录任务
    job_name = "ExampleJob" + str(time.time())  # 一个在Amazon Transcribe中独特的名称
    transcribe_client = boto3.client('transcribe')
    
    # 我们直接使用本地音频文件路径，不再上传到S3
    media_uri = "file://" + audio

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat='wav',
        IdentifyLanguage=True,
        LanguageOptions=['en-US', 'zh-CN']
    )

    max_tries = 100
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                transcript = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                return transcript
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    return "Fail"

# 创建Gradio界面
gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="microphone", format="wav", type="filepath"),  # 使用microphone录制音频
    outputs="text"
).launch(share=True)
