import requests

print("Testing STT endpoint")
endpoint = "http://localhost:8001/listen/"  # STT-Endpoint

audio_file_path = "/Users/andreas/PycharmProjects/MIRAGE-XR_TTS-STT/py_client/audio_king.mp3"
# model = ['whisperNBAiLab']
model = ['whisper']
for m in model:
    print('Test for: ' + m)
    with open(audio_file_path, 'rb') as f:
        # Correctly separate the file and the data to be sent
        files = {'audio': (audio_file_path, f, 'audio/mp3')}
        data = {'model': m}

        # Make the request with both the 'files' for the file upload and 'data' for the other form data
        response = requests.post(endpoint, files=files, data=data)

    if response.status_code == 200:
        print("Response received successfully.")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
