import os

import chromadb
import nltk
from langdetect import detect
from textstat import textstat
from nltk.tokenize import ToktokTokenizer
from document.models import Document


def saveDocument(text, type, request):
    """Save a document with the given text, type, and request.

    Args:
        text (str): The text content of the document.
        type (str): The type of the document.
        request (dict): The request data for the document.

    Returns:
        None

    Example usage:
        saveDocument("This is a test document.", "document", {'name': 'test_document', 'database': 'documents'})

    Note:
        This method performs the following actions:
            - Detects the language of the document using the 'detect' function.
            - Creates a new document object with the provided title, source type, and content.
            - Tokenizes the document into sentences and words using the 'ToktokTokenizer'.
            - Updates various properties of the document, including language, word count, and sentence count.
            - Saves the document.
            - Checks if the Chroma database exists and creates it if not.
            - Retrieves or creates a collection in the Chroma database.
            - Adds the document to the collection with the relevant metadata.

    """
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
    """
    Calculate the Lix score of the given text.

    Parameters:
        text (str): The text to calculate the Lix score for.

    Returns:
        float: The Lix score rounded to 4 decimal places.

    Example:
        >>> ltx("This is a sample sentence.")
        16.6667
    """
    words = text.split()
    num_words = len(text.split())
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    long_words = sum(1 for word in words if len(word) > 6)

    if num_sentences == 0:  # Prevent division by zero
        return None

    lix_score = (num_words / num_sentences) + ((long_words / num_words) * 100)
    return round(lix_score, 4)
