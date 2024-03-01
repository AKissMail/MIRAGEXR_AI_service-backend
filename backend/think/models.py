from django.db import models


class Document(models.Model):
    SOURCE_CHOICES = (
        ('pdf', 'PDF'),
        ('web', 'Web'),
        ('csv', 'csv')
    )
    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=3, choices=SOURCE_CHOICES)
    content = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='documents/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)

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
