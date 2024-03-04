import requests
'''
This is a simple Test script to test if the TTS endpoint is working properly. 
'''
print("Testing TTS endpoint")
endpoint = "http://localhost:8000/options/"  # TTS-Endpoint

data = {"speakOut": "Hi, jeg heter Andreas", "voice": "default", "model": "default", "speed": 0.5}
response = requests.post(endpoint, json=data)


if response.status_code == 200:
    filename = "TTS_Test.mp3"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"MP3 saved as {filename}.")
else:
    print(f"Error: {response.status_code}")
    #print(response.text)
