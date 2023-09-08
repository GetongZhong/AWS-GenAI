import requests

api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
meeting_id = 'YOUR_MEETING_ID'

# Generate JWT token for authentication
token_url = 'https://api.zoom.us/v2/users/{userId}/token'.format(userId='me')
response = requests.post(token_url, headers={'Authorization': 'Bearer ' + api_secret})
jwt_token = response.json()['token']

# Make API request to retrieve recordings
recordings_url = 'https://api.zoom.us/v2/meetings/{meetingId}/recordings'.format(meetingId=meeting_id)
response = requests.get(recordings_url, headers={'Authorization': 'Bearer ' + jwt_token})
recordings = response.json()['recording_files']

# Extract audio stream URL from the response
audio_stream_url = None
for recording in recordings:
    if recording['file_type'] == 'audio':
        audio_stream_url = recording['download_url']
        break

if audio_stream_url:
    print(f"Audio stream URL: {audio_stream_url}")
else:
    print("No audio stream found for the meeting")