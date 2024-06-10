from django.db import models


class Document(models.Model):
    """
    Class: Document

    A class that represents a document.

    Attributes:
    - title (CharField): The title of the document.
    - source_type (CharField): The type of the document.
    - content (TextField): The content of the document.
    - date_added (DateTimeField): The date when the document was added.
    - ltx (FloatField): The LTX value of the document.
    - smog_index (FloatField): The SMOG index value of the document.
    - language (CharField): The language of the document.
    - sentences (TextField): The sentences in the document.
    - words (TextField): The words in the document.
    - average_sentence_length (FloatField): The average length of sentences in the document.
    - word_count (IntegerField): The count of words in the document.
    - sentences_count (IntegerField): The count of sentences in the document.
    - model_type (CharField): The type of the document's model.

    Methods:
    - __str__(): Returns the title of the document.

    Example usage:

    document = Document.objects.get(pk=1)
    print(document.title)
    """
    SOURCE_CHOICES = (
        ('pdf', 'PDF'),
        ('web', 'Web'),
        ('csv', 'CSV'),
        ('txt', 'TXT')
    )
    MODEL_CHOICES = (
        ('faiss', 'FAISS'),
        ('chromadb', 'ChromaDB'),
        ('jaccard', 'Jaccard'),
    )
    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=3, choices=SOURCE_CHOICES)
    content = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    ltx = models.FloatField(null=True, blank=True)
    smog_index = models.FloatField(null=True, blank=True)
    language = models.CharField(max_length=4, blank=True, null=True)
    sentences = models.TextField(blank=True, null=True)
    words = models.TextField(blank=True, null=True)
    average_sentence_length = models.FloatField(null=True, blank=True)
    word_count = models.IntegerField(null=True, blank=True)
    sentences_count = models.IntegerField(null=True, blank=True)
    model_type = models.CharField(max_length=10, choices=MODEL_CHOICES)

    def __str__(self):
        return self.title


class Embedding(models.Model):
    """
    Class representing an embedding for a document.

    Attributes:
        document (ForeignKey): A foreign key reference to the Document model.
        embedding (BinaryField): A binary field storing the embedding data.
        metadata (JSONField): A JSON field storing additional metadata.

    Methods:
        __str__(): Returns a string representation of the embedding.
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='embeddings')
    embedding = models.BinaryField()
    metadata = models.JSONField()

    def __str__(self):
        return f"Embedding for Document ID {self.document.id}"
