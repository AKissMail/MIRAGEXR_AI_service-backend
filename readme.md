# MirageXR AI Services

This server backend implements a facade to AI services, providing a wrapper to [MirageXR](https://github.com/WEKIT-ECS/MIRAGE-XR), 
specifically to facilitate dialogue interaction with Large Language Models (LLMs) using Speech-To-Text (STT) and Text-To-Speech 
(TTS) services. LLM interaction follows the Retrieval-Augmented Generation (RAG) pattern, see [Lewis et al.](https://arxiv.org/abs/2005.11401),
and manages a data pipeline for storing documents as corpora, enhancing the dialogue experience in eXtended Reality settings.

## Table of Contents

- [Introduction](#introduction)
- [Endpoints and Features](#features)
- [License](#license)

## Introduction

The MirageXR AI service backend extends the capabilities of the MirageXR project by adding a wrapper to external AI services 
for advanced dialogue functionalities. It serves as a facade to different LLMs, STT, and TTS models, providing endpoints 
that incorporate RAG patterns for dynamic conversation flow. The backend also includes a data pipeline to manage and store 
various documents within a corpus, making it a versatile tool for dialogue management in XR environments.

## Features

### Endpoints:

- `/listen`: Accepts an MP3 file and returns a transcript using Whisper models.
- `/options`: Offers a JSON response detailing the available models.
- `/speak`: Converts text into speech.
- `/think`: Supports three different LLM models: GPT-3.5, GPT-4, and the RAG Model.

### Data Pipeline:

- Processes and stores content from PDF, TXT, and CSV files in a database, making it accessible for RAG. 
- All documents in /data/ will be processed. With the command `data`, the data will be processed and uploaded
- to the database. An additional analysis can be run using the command `analyze_data`. 

### Database 

![db.png](db.png)


### Set up
1. Clone the project.
2. Install with pip all the dependencies: `pip install -r requirements.txt`
3. Set up an environment: Create a `backend/.env` file with the field `OPENAI_API_KEY=$your_key`.
4. `cd backend`
5. Run the Django server with `python manage.py runserver 8000 &`.
6. Set up the database with `python manage.py makemigrations`
7. and `python manage.py migrate`.
8. Create a superuser with `python manage.py createsuperuser`.
9. Access the backend via `http://127.0.0.1:8000/admin/`, and create a new user (optional) and an authentication token, to be used with the API request.
10. Deposit documents in the data folder (backend/data). This can include PDF, HTML, and CSV files.
11. Run the data pipeline with `python manage.py data` to import the files
12. and `python manage.py analyze_data` to process them.
13. Send your request (e.g., via Postman) and include the key in the header with the line key `Authorization` set to `Token $key`.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
