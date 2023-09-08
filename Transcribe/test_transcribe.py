import boto3
import time
import json

bucket_name = 'aigc-bj-team1'

def upload_to_s3(file_path, bucket):
    object_name = file_path.split('/')[-1]  # 使用文件名作为 object_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None
    return "s3://" + bucket + "/" + object_name
def get_transcript(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    response_json = json.loads(obj['Body'].read().decode("utf-8"))
    transcript = response_json['results']['transcripts'][0]['transcript']
    return transcript


def transcribe_audio_file_from_sagemaker(file_path):
    s3_url = upload_to_s3(file_path, bucket_name)
    if not s3_url:
        return "Failed to upload to S3."
    
    job_name = "TranscriptionJob" + str(time.time())
    transcribe_client = boto3.client('transcribe')
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_url},
        MediaFormat='wav',  # For .wav files or mp3
        IdentifyLanguage=True,
        LanguageOptions=['en-US', 'zh-CN'],
        OutputBucketName=bucket_name,
        OutputKey='transcription_result.txt'
    )

    max_tries = 100
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            if job_status == 'COMPLETED':
                transcript = get_transcript(bucket_name, 'transcription_result.txt')
                return transcript
            return f"Transcription job {job_name} failed."
        time.sleep(10)
    return "Transcription job timed out."

# Example usage
file_path = "testfile/Recording.wav"
result = transcribe_audio_file_from_sagemaker(file_path)
print(result)
