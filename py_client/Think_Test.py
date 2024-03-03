import requests

'''
This is a simple Test script to test if the TTS endpoint is working properly. 
'''
print("Testing thnk endpoint")
endpoint = "http://localhost:8000/think/"

data = {"message": "What is the V2? Can you give me an example?", "context": "You are an Norvigan teacher. Page 2 "
                                                                             "section 254",
        "model": "norwegian-on-the-web"}
response = requests.post(endpoint, json=data)

if response.status_code == 200:
    print(f"Success: {response.status_code}")
    print(response.headers)
    print(response.content)
    print(response.text)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
