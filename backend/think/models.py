from django.db import models


class Document(models.Model):
    """
    Represents a document as part of the RAG Corpus.
    Attributes:
        title (models.CharField): The title of the document.
        - Source_type (models.CharField): The source type of the document,
          with choices limited to PDF, Web, CSV, and Txt formats.
        - Content (models.TextField): The main content of the document as String.
        - Date_added (models.DateTimeField): When it was added to the system.
        - Ltx (models.FloatField): To sore the LTX score (a measure of readability) for documents in a nordic language.
        - Smog_index (models.FloatField): To sore the Smog score (a measure of readability) for documents in english.
        - Language (models.CharField): The language of the document.
        - Sentences (models.TextField): The sentences in the document as an array of strings.
        - Words (models.TextField): The words in the document as an array of strings.
        - Average_sentence_length (models.FloatField): Storing the average sentence length in the document.
        - Word_count (models.IntegerField): Storing the Wordcount.
        - Sentences_count (models.IntegerField): Storing the sentences count.
    """
    objects = None
    SOURCE_CHOICES = (
        ('pdf', 'PDF'),
        ('web', 'Web'),
        ('csv', 'Csv'),
        ('txt', 'Txt')
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

    def __str__(self):
        """
               Returns the title of the document as its string representation.
        """
        return self.title


class Content(models.Model):
    """
       Represents a section or a piece of content within a document.
       Attributes:
           - document (models.ForeignKey): A ForeignKey linking to the Document.
           - Heading (models.CharField): The heading of this content section.
           - Body_text (models.TextField): The body text of this content section.
           - Section_number (models.IntegerField): ID for a section within the document.
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='content_items')
    heading = models.CharField(max_length=255, blank=True, null=True)
    body_text = models.TextField(blank=True, null=True)
    section_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """
                     Returns the heading of the document as its string representation.
        """
        return self.heading or "Unnamed Content"
