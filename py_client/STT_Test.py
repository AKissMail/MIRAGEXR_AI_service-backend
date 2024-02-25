import requests

''' todo hier muss alles nochmal angepasst werden! '''

# Simple Test script to test the STT endpoint functionality
print("Testing STT endpoint")
endpoint = "http://localhost:8000/upload-audio/"  # STT-Endpoint

# Hier musst du den Pfad zu deiner Audiodatei angeben
audio_file_path = 'path/to/your/audio_file.wav'
model = 'dein_gewünschtes_stt_modell'

# Öffne die Audiodatei im Binärmodus
with open(audio_file_path, 'rb') as f:
    files = {'audio_file': (audio_file_path, f, 'audio/wav')}
    data = {'model': model}
    response = requests.post(endpoint, files=files, data=data)

# Überprüfe den Statuscode der Antwort
if response.status_code == 200:
    print("Response received successfully.")
    # Hier könntest du die Antwort verarbeiten, z.B. die transkribierte Textausgabe anzeigen
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
