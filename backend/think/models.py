from django.db import models


class Document(models.Model):
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
        return self.title


class Content(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='content_items')
    heading = models.CharField(max_length=255, blank=True, null=True)
    body_text = models.TextField(blank=True, null=True)
    section_number = models.IntegerField(blank=True, null=True)
    tag = models.ManyToManyField('Tag', related_name='contents')

    def __str__(self):
        return self.heading or "Unnamed Content"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
