from document.models import Document


def save_document_to_db(text, file_type, request_data, metadata):
    """

    Save a document to the database.

    Parameters:
    - text (str): The content of the document.
    - file_type (str): The type of the document file.
    - request_data (dict): The data received from the request.
    - metadata (dict): The metadata of the document.
    - config (dict): The configuration settings.

    Returns:
    - document (Document): The saved document.

    """
    document = Document(title=request_data['name'], source_type=file_type, content=text)
    document.language = metadata.get('language')
    document.sentences = metadata.get('sentences')
    document.words = metadata.get('words')
    document.word_count = metadata.get('word_count')
    document.sentences_count = metadata.get('sentences_count')
    document.average_sentence_length = metadata.get('average_sentence_length')
    document.ltx = metadata.get('ltx')
    document.smog_index = metadata.get('smog_index')
    document.save()

    return document
