from document.docment_utility.metadata import extract_metadata
from document.models import Document


def save_jaccard_document(text, file_type, request_data):
    """

    Save Document for the jaccard RAG model

    Saves a document to the database using the Jaccard similarity model.

    Parameters:
    - text (str): The content of the document.
    - file_type (str): The type of the document file.
    - request_data (dict): Additional data for the document.
    - config (dict): Configuration settings.

    Returns:
    - document (Document): The saved document.

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
        model_type='jaccard'
    )
    document.save()

    return document
