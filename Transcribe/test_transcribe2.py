import boto3
import time
import json
import os

bucket_name = 'aigc-bj-team1'


def upload_to_s3(file_path, bucket):
    object_name = file_path.split('/')[-1]
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")
        return None
    return "s3://" + bucket + "/" + object_name


def get_transcript(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    response_json = json.loads(obj['Body'].read().decode("utf-8"))
    transcript = response_json['results']['transcripts'][0]['transcript']
    return transcript


def transcribe_audio_file(file_path):
    s3_url = upload_to_s3(file_path, bucket_name)
    if not s3_url:
        print(f"Failed to upload {file_path} to S3.")
        return None
    
    job_name = "TranscriptionJob" + str(time.time())
    transcribe_client = boto3.client('transcribe')
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_url},
            MediaFormat='wav',  # Ensure this matches the format of your files
            IdentifyLanguage=True,
            LanguageOptions=['en-US', 'zh-CN'],
            OutputBucketName=bucket_name,
            OutputKey=f"{job_name}_result.txt"
        )
    except Exception as e:
        print(f"Error starting transcription job for {file_path}: {e}")
        return None

    max_tries = 100
    while max_tries > 0:
        max_tries -= 1
        try:
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        except Exception as e:
            print(f"Error fetching transcription job status for {file_path}: {e}")
            return None
        
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            if job_status == 'COMPLETED':
                transcript = get_transcript(bucket_name, f"{job_name}_result.txt")
                return transcript
            else:
                print(f"Transcription job for {file_path} failed. Reason: {job['TranscriptionJob'].get('FailureReason', 'Unknown')}")
                return None
        time.sleep(10)
    print(f"Transcription job for {file_path} timed out.")
    return None



def transcribe_audio_files_from_directory(directory_path):
    results = {}
    audio_files = [f for f in os.listdir(directory_path) if f.endswith('.wav')]
    for audio_file in audio_files:
        full_path = os.path.join(directory_path, audio_file)
        transcript = transcribe_audio_file(full_path)
        if transcript:
            results[audio_file] = transcript
        else:
            print(f"Failed to transcribe {audio_file}")
    return results


# Specify the directory containing the audio files
directory_path = "testfile"
results = transcribe_audio_files_from_directory(directory_path)

# Save the results to a JSON file
with open("transcription_results.json", "w") as f:
    json.dump(results, f)
