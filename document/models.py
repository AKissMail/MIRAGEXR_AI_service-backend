from django.db import models


class Document(models.Model):
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
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='embeddings')
    embedding = models.BinaryField()
    metadata = models.JSONField()

    def __str__(self):
        return f"Embedding for Document ID {self.document.id}"
