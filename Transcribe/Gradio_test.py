import gradio as gr
import boto3
import time
import json

bucket_name = 'aigc-bj-team1'


def upload_to_s3(file_path, bucket):
    object_name = "example.mp3" # unique in a bucket
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except:
        return False
    return "s3://"+bucket+"/"+object_name

def get_transcript(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    response_json = json.loads(obj['Body'].read())
    transcript = response_json['results']['transcripts'][0]['transcript']
    return transcript

def transcribe(audio):
    bucket = bucket_name
    s3_url = upload_to_s3(audio, bucket)
    # create a transciption job
    job_name = "ExampleJob" + str(time.time()) # a unique name in your Amazon Transcribe
    transcribe_client = boto3.client('transcribe')
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_url},
        MediaFormat='mp3',
        IdentifyLanguage = True,
        LanguageOptions=['en-US', 'zh-CN'],
        OutputBucketName=bucket,
        OutputKey='example_text.txt'
    )
    max_tries = 100
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                transcript = get_transcript(bucket,'example_text.txt')
                return transcript
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    return "Fail"

gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="upload", format="mp3", type="filepath"),
    outputs="text").launch(share=True)