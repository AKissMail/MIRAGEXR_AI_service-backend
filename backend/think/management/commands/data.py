import nltk
from django.core.management.base import BaseCommand
from pathlib import Path
from ...data_integration import (save_pdf_data, save_html_data, save_csv_data, save_txt_data)
from ...models import Document

import chromadb
import nltk
import os

from langdetect import detect
from textstat import textstat


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
    help = 'Process and load documents into the database'

    def handle(self, *args, **options):
        handeledDocumnet = []
        self.stdout.write('Loading data...')
        self.stdout.write('Process PDF')
        for pdf_path in Path('data').glob('*.pdf'):
            save_pdf_data(str(pdf_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {pdf_path.name}'))
        self.stdout.write('Process HTML')
        for html_path in Path('data').glob('*.html'):
            save_html_data(str(html_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {html_path.name}'))
        self.stdout.write('Process CSV')
        for csv_path in Path('data').glob('*.csv'):
            save_csv_data(str(csv_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {csv_path.name}'))
        for txt_path in Path('data').glob('*.txt'):
            save_txt_data(str(txt_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {txt_path.name}'))

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
                    handeledDocumnet.append(doc.pk)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing document ID {doc.pk}: {str(e)}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped document ID {doc.pk} due to None content"))
        if not (os.path.exists("data/v_DB/chroma.sqlite3")):
            print("Creating the Chroma DB")
            client = chromadb.PersistentClient(path="data/v_DB")
            collection =client.create_collection("NorwegianGPT")
        else:
            print("Found Database")
            client = chromadb.PersistentClient(path="data/v_DB")
            collection = client.get_collection("NorwegianGPT")
        newData = Document.objects.filter(id__in=handeledDocumnet)

        for doc in newData:
            print(doc.pk)

            metaData = {}
            if doc.title is not None:
                metaData["title"] = doc.title
            if doc.source_type is not None:
                metaData["source_type"] = doc.source_type
            if doc.ltx is not None:
                metaData["ltx"] = doc.ltx
            if doc.smog_index is not None:
                metaData["smog_index"] = doc.smog_index
            if doc.language is not None:
                metaData["language"] = doc.language
            if doc.sentences is not None:
                metaData["sentences"] = doc.sentences
            if doc.words is not None:
                metaData["words"] = doc.words
            if doc.average_sentence_length is not None:
                metaData["average_sentence_length"] = doc.average_sentence_length
            if doc.word_count is not None:
                metaData["word_count"] = doc.word_count
            if doc.sentences_count is not None:
                metaData["sentences_count"] = doc.sentences_count

            collection.add(
                documents=[doc.content],
                metadatas=[metaData],
                ids=[str(doc.pk)]
            )
            print(f"ID {doc.pk} is now part of the Vector DB")



    def get_language(self):
        try:
            return detect(self)
        except Exception as _:
            return None
