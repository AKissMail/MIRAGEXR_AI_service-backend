import json
import os
from document.docment_utility.documentParser import parse_pdf, parse_csv, parse_txt, parse_html
from document.saveRAG.saveFaiss import save_faiss_document
from document.saveRAG.saveChromaDB import save_chromadb_document
from document.saveRAG.saveJaccard import save_jaccard_document
from document.docment_utility.chunking import create_text_chunks


def handle_data(request_data, config_name):
    """

    Handle Data

    This method handles the incoming data by performing various operations based on the file type and the configuration
    specified.

    Parameters:
    - request_data: The request data containing the document file and other relevant information.
    - config_name: The name of the configuration to be used for processing the data.

    Returns:
    - If the configuration file exists and the data is successfully processed, it returns True.
    - If the configuration file doesn't exist or there is an error in processing the data, it returns False.

    """
    config_path = os.path.join('config/think/', f'{config_name}.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        print("Fail to load config with " + config_path + " and " + config_name)
        return False

    document_file = request_data.get('document')
    if isinstance(document_file, list):
        document_file = document_file[0]
    file_type = document_file.content_type

    if file_type == 'application/pdf':
        text = parse_pdf(document_file)
    elif file_type == 'text/csv':
        text = parse_csv(document_file)
    elif file_type == 'text/plain':
        text = parse_txt(document_file)
    elif file_type == 'text/html':
        text = parse_html(document_file)
    else:
        return False

    chunks = create_text_chunks(text)

    rag_function = config['rag_function']
    if rag_function == 'faiss':
        for chunk in chunks:
            save_faiss_document(chunk, file_type, request_data)
    elif rag_function == 'chromadb':
        for chunk in chunks:
            save_chromadb_document(chunk, file_type, request_data, config)
    elif rag_function == 'jaccard':
        for chunk in chunks:
            save_jaccard_document(chunk, file_type, request_data)
    else:
        return False
    return True
