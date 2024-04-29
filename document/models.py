from django.db import models


class Document(models.Model):
    """
    This class represents a document object in the application.

    Attributes:
        - title (CharField): The title of the document.
        - source_type (CharField): The type of the document's source.
        - content (TextField): The content of the document.
        - date_added (DateTimeField): The date and time when the document was added.
        - ltx (FloatField): The LTX value of the document.
        - smog_index (FloatFiled): The SMOG index of the document.
        - language (CharField): The language of the document.
        - sentences (TextField): The sentences in the document.
        - words (TextField): The words in the document.
        - average_sentence_length (FloatField): The average length of the sentences in the document.
        - word_count (IntegerField): The total number of words in the document.
        - sentences_count (IntegerField): The total number of sentences in the document.

    Methods:
        - __str__(): Returns the title of the document as its string representation.
    """
    class Meta:
        app_label = 'think'
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
    A class representing content within a document.

    Attributes:
        document (ForeignKey): The document that this content belongs to.
        heading (CharField): The heading for this content.
        body_text (TextField): The body text for this content.
        section_number (IntegerField): The section number for this content.

    Methods:
        __str__(): Returns the heading of the document as its string representation.

    Example usage:
        content = Content()
        content. Document = document
        content. Heading = "Introduction"
        content.body_text = "Lorem ipsum dolor sit amet..."
        content.section_number = 1
        content.save()

        print(content)
        # Output: "Introduction"

    Note: This class is related to the 'think' app.
    """
    class Meta:
        app_label = 'think'

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='content_items')
    heading = models.CharField(max_length=255, blank=True, null=True)
    body_text = models.TextField(blank=True, null=True)
    section_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """
                     Returns the heading of the document as its string representation.
        """
        return self.heading or "Unnamed Content"
