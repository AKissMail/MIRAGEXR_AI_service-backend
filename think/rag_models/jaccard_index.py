from document.models import Document


def get_best_document(prompt, corpus_document):
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


def jaccard_index(validated_data):
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
    best_jaccard = {
        'user_prompt': prompt,
        'best_jaccard_score': 0,
        'best_document_text': "No document found"
    }

    for document in Document.objects.all():
        current_score = get_best_document(prompt, document.content)
        if best_document[1] < current_score:
            best_document = [document.content, current_score]
            best_jaccard = {
                'user_prompt': prompt,
                'best_jaccard_score': best_document[1],
                'best_document_text': best_document[0],
            }

    return best_jaccard['best_document_text']
