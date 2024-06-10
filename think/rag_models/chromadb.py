import random
from rest_framework import status
from rest_framework.response import Response
import chromadb
from cfehome import settings
from document.models import Document


def vector_chromadb(validated_data):
    """
    Retrieves the content of a randomly selected document from a "NorwegianGPT" collection based on a search query.
    Parameters: - validated_data (dict): Contains the search query with the key "message". Returns: - str: Content of
    the selected document or a blank string if no match is found. Note: Uses `chromadb.PersistentClient` for database
    operations. Assumes the database and collection are correctly configured.
    """

    query = validated_data.get("message")
    client = chromadb.PersistentClient(path=settings.VECTOR_DB)
    try:
        collection = client.get_collection(validated_data.get("model"))
    except Exception as e:
        return Response("Couldn't retrieve the Model. {}".format(e), status=status.HTTP_400_BAD_REQUEST)

    results = collection.query(query_texts=[query])

    if not results['ids']:
        return " "

    document_id = random.choice(results['ids'][0])

    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        return " "

    return document.content

