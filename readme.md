# MirageXR Backend

This backend serves as an integral component of [MirageXR](https://github.com/WEKIT-ECS/MIRAGE-XR), specifically 
designed to facilitate dialogues through various Large Language Models (LLMs), Speech-To-Text (STT), and Text-To-Speech 
(TTS) models. It also incorporates Retrieval-Augmented Generation (RAG) patterns and manages a data pipeline for storing 
documents within a corpus, enhancing the dialogue experience in virtual and augmented reality settings.

## Table of Contents

- [Introduction](#introduction)
- [Endpoints and Features](#features)
- [License](#license)

## Introduction

The MirageXR Backend extends the capabilities of the MirageXR project by adding advanced dialogue functionalities. 
It serves as a wrapper around different LLMs, STT, and TTS models, providing endpoints that incorporate RAG patterns 
for dynamic conversation flows. The backend also includes a data pipeline to manage and store various documents within 
a corpus, making it a versatile tool for dialogue management in XR environments.

## Features

### Endpoints:

- `/listen`: Accepts an MP3 file and returns a transcript using various Whisper models.
- `/options`: Offers a JSON response detailing the available models.
- `/speak`: Converts text into speech.
- `/think`: Supports three different LLM models: GPT-3.5, GPT-4, and the RAG Model.

### Data Pipeline:

- Processes and stores content from PDF, TXT, and CSV files in a database, making it accessible for the RAG Model. 
- All documents in /data/ will be processed. With the command `data` the data will be processed and uploaded to the database. An additional analysis can be run with the command `analyze_data`. 

### Database 

![db.png](db.png)


### Set up
1. Pull the project however you want.
2. Install with pip all the dependencies and set up an environment.
3. Create a .env file with the field `OPENAI_API_KEY=$your_key`.
4. Run the Django server with `python manage.py runserver 8000`.
5. Set up the database with `python manage.py makemigrations` and `python manage.py migrate`.
6. Create a Superuser with `python manage.py createsuperuser`.
7. In the backend, create a user and a key. Open the endpoint admin, and create a user and a user key for the API request.
8. Fill up the data folder (backend/data) with your data including PDF, HTML, and CSV files.
9. Run the data pipeline with `python manage.py data` and `python manage.py analyze_data`.
10. Send your request via Postman and include the key in the `Authorization` header as `Token $key`.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.