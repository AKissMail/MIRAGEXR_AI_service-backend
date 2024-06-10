import faiss
import numpy as np
from django.apps import apps

from document.models import Embedding


def get_embedding(text):
    """
    Get the embedding vector for the given text.

    :param text: The text for which to get the embedding vector.
    :type text: str

    :return: The embedding vector of the text.
    :rtype: numpy.ndarray
    """
    ft_model = apps.get_app_config('think').ft_model
    preprocessed_text = text.replace('\n', ' ')
    return ft_model.get_sentence_vector(preprocessed_text)


def query_faiss_embeddings(query_text):
    """
    Query Faiss Embeddings

    This method takes a query text and returns the nearest sentences based on the embeddings stored in the database.

    Parameters:
    - query_text (str): The text to be used as the query.

    Returns:
    - nearest_sentences (list): A list of the nearest sentences based on the query text's embeddings.

    """
    embeddings = Embedding.objects.all()
    embedding_list = [np.frombuffer(e.embedding, dtype='float32') for e in embeddings]
    metadata_list = [e.metadata for e in embeddings]
    dimension = 300
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embedding_list))
    query_embedding = get_embedding(query_text['message'])
    D, I = index.search(np.array([query_embedding]), k=2)
    I = I[0].astype(int)
    nearest_sentences = [metadata_list[i]['sentences'] for i in I]
    return nearest_sentences
