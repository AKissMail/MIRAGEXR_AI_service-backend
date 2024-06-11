import unittest
from django.test import TestCase
from document.models import Embedding, Document


class DocumentModelTest(TestCase):
    def setUp(self):
        self.document = Document.objects.create(
            title='Test Document',
            source_type='pdf',
            content='This is a test document.',
            ltx=1.0,
            smog_index=1.0,
            language='en',
            sentences='This is a sentence.',
            words='These are words.',
            average_sentence_length=4.0,
            word_count=4,
            sentences_count=1,
            model_type='faiss',
        )

    def test_document_title(self):
        self.assertEqual(self.document.title, 'Test Document')

    def test_document_source_type(self):
        self.assertEqual(self.document.source_type, 'pdf')

    def test_document_content(self):
        self.assertEqual(self.document.content, 'This is a test document.')

    def test_document_ltx(self):
        self.assertEqual(self.document.ltx, 1.0)

    def test_document_smog_index(self):
        self.assertEqual(self.document.smog_index, 1.0)

    def test_document_language(self):
        self.assertEqual(self.document.language, 'en')

    def test_document_sentences(self):
        self.assertEqual(self.document.sentences, 'This is a sentence.')

    def test_document_words(self):
        self.assertEqual(self.document.words, 'These are words.')

    def test_document_average_sentence_length(self):
        self.assertEqual(self.document.average_sentence_length, 4.0)

    def test_document_word_count(self):
        self.assertEqual(self.document.word_count, 4)

    def test_document_sentences_count(self):
        self.assertEqual(self.document.sentences_count, 1)

    def test_document_model_type(self):
        self.assertEqual(self.document.model_type, 'faiss')

    def test_document_str(self):
        self.assertEqual(self.document.__str__(), 'Test Document')


class TestEmbedding(TestCase):

    def setUp(self):
        """
        Setup function to create a test embedding instance.
        """
        self.document = Document.objects.create()  # Create a document object
        self.embedding = Embedding.objects.create(
            document=self.document,
            embedding=b'\x01\x02\x03\x04',
            metadata={"key": "value"},
        )

    def test_str_representation(self):
        """
        Test string representation of Embedding instance.
        """
        self.assertEqual(str(self.embedding), f"Embedding for Document ID {self.embedding.document.id}")

    def test_binary_embedding_field(self):
        """
        Test binary data are saved correctly in `embedding` attribute.
        """
        self.assertEqual(self.embedding.embedding, b'\x01\x02\x03\x04')

    def test_metadata_field(self):
        """
        Test JSON data are saved correctly in `metadata` attribute.
        """
        self.assertEqual(self.embedding.metadata, {"key": "value"})

    def test_document_field(self):
        """
        Test document field is saved correctly.
        """
        self.assertEqual(self.embedding.document, self.document)


if __name__ == "__main__":
    unittest.main()