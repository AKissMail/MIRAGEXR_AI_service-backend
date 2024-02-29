import requests

'''
This is a simple Test script to test if the TTS endpoint is working properly. 
'''
print("Testing thnk endpoint")
endpoint = "http://localhost:8000/think/"

data = {"message": "Hier ist eine Satez uidn ivcjh mavcj e ", "context": " Hallo! Ja klar, ich kann dir helfen. Bitte sende mir den Satz oder die Sätze, bei denen du dir unsicher bist, und ich werde sie für dich überprüfen.Du bist ein Deutschlehrer der auf deutsch generate antwortet", "model": "gpt-4-turbo-preview"}
response = requests.post(endpoint, json=data)

if response.status_code == 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    print(response)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
