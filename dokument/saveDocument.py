import os

import chromadb
import nltk
from langdetect import detect
from textstat import textstat
from nltk.tokenize import ToktokTokenizer
from dokument.models import Document


def saveDocument(text, type, request):
    print(type, request)
    language = detect(text)
    print(language)
    document = Document(title=request['name'], source_type=type, content=text)
    print(language)
    toktok = ToktokTokenizer()
    if language == "no":
        document.ltx = ltx(document.content)

    if language == "en":
        document.smog_index = textstat.smog_index(document.content)

    document.sentences = toktok.tokenize(document.content)
    document.words = toktok.tokenize(document.content)
    document.language = language
    document.word_count = len(document.words)
    document.sentences_count = len(document.sentences)
    document.average_sentence_length = len(document.words) / len(document.sentences) if document.sentences else 0
    document.sentences = " ".join(document.sentences)
    document.words = " ".join(document.words)

    document.save()

    if not (os.path.exists("vectorDB/chroma.sqlite3")):
        print("Creating the Chroma DB")
        client = chromadb.PersistentClient(path="vectorDB")
        client.create_collection(request['database'])

    try:
        client = chromadb.PersistentClient(path="data/v_DB")
        collection = client.get_collection(request['database'])
        print("Found Database")
    except Exception as e:
        print(str(e))
        client = chromadb.PersistentClient(path="data/v_DB")
        collection = client.create_collection(request['database'])

    metaData = {}
    if document.title is not None:
        metaData["title"] = document.title
    if document.source_type is not None:
        metaData["source_type"] = document.source_type
    if document.ltx is not None:
        metaData["ltx"] = document.ltx
    if document.smog_index is not None:
        metaData["smog_index"] = document.smog_index
    if document.language is not None:
        metaData["language"] = document.language
    if document.sentences is not None:
        metaData["sentences"] = document.sentences
    if document.words is not None:
        metaData["words"] = document.words
    if document.average_sentence_length is not None:
        metaData["average_sentence_length"] = document.average_sentence_length
    if document.word_count is not None:
        metaData["word_count"] = document.word_count
    if document.sentences_count is not None:
        metaData["sentences_count"] = document.sentences_count
    print(metaData)
    collection.add(
        documents=[text],
        metadatas=[metaData],
        ids=[str(document.pk)]
    )


def ltx(text):
    words = text.split()
    num_words = len(text.split())
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    long_words = sum(1 for word in words if len(word) > 6)

    if num_sentences == 0:  # Prevent division by zero
        return None

    lix_score = (num_words / num_sentences) + ((long_words / num_words) * 100)
    return round(lix_score, 4)
