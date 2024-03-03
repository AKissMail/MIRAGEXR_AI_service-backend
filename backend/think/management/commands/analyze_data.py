import nltk
from django.core.management.base import BaseCommand
from langdetect import detect
from textstat import textstat
from ...models import Document



def ltx(text):
    words = text.split()
    num_words = len(text.split())
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    long_words = sum(1 for word in words if len(word) > 6)

    if num_sentences == 0:  # Prevent division by zero
        return None

    lix_score = (num_words / num_sentences) + ((long_words / num_words) * 100)
    return round(lix_score, 4)


class Command(BaseCommand):
    help = 'Analyses the documents in the Database and add complexity scores, themes and Content segmentation'

    def handle(self, *args, **options):
        self.stdout.write("Analyzing data...")

        # Fetch all documents
        documents = Document.objects.all()

        for doc in documents:
            # Ensure doc.content is not None
            if doc.content:
                try:
                    language = detect(doc.content)
                    if language == "no":
                        readability = ltx(doc.content)
                        doc.language = language
                        doc.ltx = readability
                        doc.sentences = nltk.sent_tokenize(doc.content, language='norwegian')
                        doc.words = nltk.word_tokenize(doc.content, language='norwegian')
                        doc.word_count = len(doc.words)
                        doc.sentences_count = len(doc.sentences)
                        doc.average_sentence_length = len(doc.words) / len(doc.sentences) if doc.sentences else 0

                    if language in ('en', None):
                        doc.language = language
                        doc.smog_index = textstat.smog_index(doc.content)
                        doc.sentences = nltk.sent_tokenize(doc.content)
                        doc.words = nltk.word_tokenize(doc.content)
                        doc.word_count = len(doc.words)
                        doc.sentences_count = len(doc.sentences)
                        doc.average_sentence_length = len(doc.words) / len(doc.sentences) if doc.sentences else 0
                    doc.save()

                    self.stdout.write(self.style.SUCCESS(f"Processed document ID {doc.pk}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing document ID {doc.pk}: {str(e)}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped document ID {doc.pk} due to None content"))

    def get_language(self):
        try:
            return detect(self)
        except:
            return None
