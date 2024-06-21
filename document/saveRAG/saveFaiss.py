import faiss
import numpy as np
from document.docment_utility.metadata import extract_metadata
from document.models import Document, Embedding
from think.rag_models.faiss import get_embedding


def save_faiss_document(text, file_type, request_data):
    """

    Saves a document for the faiss RAG model with the given parameters.

    Parameters:
    - text (str): The text content of the document.
    - file_type (str): The type of the source file.
    - request_data (dict): Additional data related to the request.
    - config (dict): Configuration parameters.

    Returns:
    - document (Document): The saved document object.

    Example usage:
    ```
    text = "Lorem ipsum dolor sit amet."
    file_type = "txt"
    request_data = {'name': 'Document 1'}
    config = {...}

    saved_document = save_faiss_document(text, file_type, request_data, config)
    ```
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
        model_type='faiss'
    )
    document.save()

    embedding = get_embedding(text)

    Embedding.objects.create(
        document=document,
        embedding=embedding.tobytes(),
        metadata=metadata
    )

    dimension = 300
    assert embedding.shape[
               -1] == dimension, f"Embedding dimension mismatch, expected {dimension} but got {embedding.shape[-1]}"

    Embedding.objects.create(
        document=document,
        embedding=embedding.tobytes(),
        metadata=metadata
    )

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array([embedding]))

    return document
