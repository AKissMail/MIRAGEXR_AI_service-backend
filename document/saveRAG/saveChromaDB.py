import chromadb

from cfehome import settings
from document.docment_utility.metadata import extract_metadata
from document.models import Document


def save_chromadb_document(text, file_type, request_data, config):
    """
    Save a document to ChromaDB and return the saved document.

    :param text: The content of the document.
    :type text: str
    :param file_type: The type of file from which the document originated.
    :type file_type: str
    :param request_data: Additional information about the document.
    :type request_data: dict
    :param config: Configuration settings.
    :type config: dict
    :return: The saved document.
    :rtype: Document
    """
    metadata = extract_metadata(text)
    document = Document(
        title=request_data['name'],
        source_type=file_type,
        content=text,
        language=metadata.get('language'),
        sentences=metadata.get('sentences'),
        words=metadata.get('words'),
        word_count=metadata.get('word_count'),
        sentences_count=metadata.get('sentences_count'),
        average_sentence_length=metadata.get('average_sentence_length'),
        ltx=metadata.get('ltx'),
        smog_index=metadata.get('smog_index'),
        model_type='chromadb'
    )

    client = chromadb.PersistentClient(path=settings.VECTOR_DB)
    try:
        collection = client.get_collection(config['apiName'])
    except Exception:
        collection = client.create_collection(config['apiName'])

    metaData = {key: value for key, value in metadata.items() if value is not None}
    metaData["title"] = document.title
    metaData["source_type"] = document.source_type

    collection.add(
        documents=[text],
        metadatas=[metaData],
        ids=[str(document.pk)]
    )
    return document
