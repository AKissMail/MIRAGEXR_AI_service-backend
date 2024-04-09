import json
import os
import random

import chromadb

from .gpt_open_ai import gpt
from .models import Document
from .serializers import ThinkSerializer


def jaccard_index(prompt, corpus_document):
    """
    Calculate the Jaccard Index between a prompt and a document as a statistical measure of
    the similarity between two sets.
    Parameters:
        - prompt (str): The user's input prompt.
        - corpus_document (str): The document text from the corpus.
    Returns:
        - float: The Jaccard similarity score between zero (no similarity) and 1 (the same content).
        Returns 0 if the corpus_document is None.
    """
    if corpus_document is None:
        return 0
    query = prompt.lower().split(" ")
    document = corpus_document.lower().split(" ")
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)


def vector_DB(validated_data):
    """
    Retrieves the content of a randomly selected document from a "NorwegianGPT" collection based on a search query.
    Parameters: - validated_data (dict): Contains the search query with the key "message". Returns: - str: Content of
    the selected document or a blank string if no match is found. Note: Uses `chromadb.PersistentClient` for database
    operations. Assumes the database and collection are correctly configured.
    """
    query = validated_data.get("message")
    client = chromadb.PersistentClient(path="data/v_DB")
    collection = client.get_collection("NorwegianGPT")
    results = collection.query(query_texts=[query])
    result = Document.objects.get(pk=random.choice(results['ids'][0]))
    if result is None:
        return " "
    return result.content


def get_best_document(validated_data):
    """
      Identifies the document with the highest Jaccard Index score based on the user's prompt.
      Parameters:
      - validated_data (dict): Containing the 'message'.
      Returns:
      - dict: Contains the user's prompt, the highest Jaccard score, and the text of the most similar
              document, or if no document was found with a score higher than 0 the sting "No document found".
      """
    prompt = validated_data.get("message")
    best_document = [" ", 0]
    for document in Document.objects.all():
        current_score = jaccard_index(prompt, document.content)
        if best_document[1] < current_score:  # Compare scores correctly
            best_document = [document.content, current_score]
    best_jaccard = {
        'user_prompt': prompt,
        'best_jaccard_score': best_document[1],
        'best_document_text': best_document[0]
    }
    return best_jaccard.content


def norwegian_on_the_web(validated_data, mode):
    """
    Processes input data using a specific configuration to enhance the prompt for the GPT model.

    This function loads a configuration file, calculates the best document match based on the
    Jaccard Index, and constructs a new prompt incorporating the original message, context,
    and the best matching document and the Configuration

    Parameters:
    - validated_data (dict): Contains the 'message' and 'context' for generating the response.
    Returns:
    - The response from the GPT model based on the enhanced prompt.
    """
    file_path = os.path.join(os.path.dirname(__file__), '../config/now.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    if mode == "jaccard":
        final_document = get_best_document(validated_data)
    if mode == "vector":
        print(vector_DB(validated_data))
        final_document = vector_DB(validated_data)
    gpt_prompt = validated_data
    gpt_prompt['message'] = (
            config['prompt_start'] +
            "User Message: {}\n\n"
            "User Context: {}\n\n"
            "Databases Document: {}\n\n" +
            config['prompt_end']
    ).format(validated_data['message'], validated_data['context'], final_document)
    gpt_prompt['context'] = (
            config['context_start'] +
            config['context_end']
    )
    gpt_prompt['model'] = 'gpt-3.5-turbo'
    result = gpt(gpt_prompt)
    print(result)
    return result


def rag_manager(data):
    """
      Manages the RAG processing flow by validating input data and directing it to the appropriate handler.
      Parameters:
      - data (dict): The input data to be processed.
      Returns:
      - dict or str: The result of the processing, which could be an error message or the generated response.
      """
    serializer = ThinkSerializer(data=data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in 'norwegian-on-the-jaccard':
            return norwegian_on_the_web(serializer.validated_data, "jaccard")
        if serializer.validated_data['model'] in 'norwegian-on-the-vector':
            return norwegian_on_the_web(serializer.validated_data, "vector")
        else:
            return {"error": "RAG model not found"}
    else:
        return {"error": "Input data is invalid.", "details": serializer.errors}
