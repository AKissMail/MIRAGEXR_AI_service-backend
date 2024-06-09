from random import random

import faiss
import numpy as np
from document.models import Document
from rest_framework.response import Response
from rest_framework import status


def get_embedding(text):
    # Diese Funktion sollte die Einbettung für den gegebenen Text zurückgeben.
    # Implementieren Sie hier Ihre Methode, um Text in Einbettungen zu konvertieren.
    # Beispiel: Rückgabe einer Dummy-Einbettung
    return np.random.rand(512).astype('float32')


def faiss_search(query, documents):
    dimension = 512  # Dimension Ihrer Einbettungen
    index = faiss.IndexFlatL2(dimension)

    # Dokumenteneinbettungen berechnen und hinzufügen
    embeddings = np.array([get_embedding(doc.content) for doc in documents])
    index.add(embeddings)

    query_embedding = get_embedding(query)  # Einbettung der Abfrage berechnen
    D, I = index.search(np.array([query_embedding]), k=5)  # Top 5 Treffer abrufen

    results = [documents[i] for i in I[0]]
    return results


def vector_DB_faiss(validated_data):
    query = validated_data.get("message")

    try:
        documents = Document.objects.all()
    except Exception as e:
        return Response("Couldn't retrieve the documents. {}".format(e), status=status.HTTP_400_BAD_REQUEST)

    results = faiss_search(query, documents)

    if not results:
        return " "

    document = random.choice(results)

    return document.content
