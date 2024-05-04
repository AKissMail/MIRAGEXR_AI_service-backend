from django.test import TestCase
from document.models import Document, Content


class DocumentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Document.objects.create(
            title='Title',
            source_type='pdf',
            content='Content',
            ltx=1.0,
            smog_index=1.0,
            language='en',
            sentences='Hello. World.',
            words='Hello Word',
            average_sentence_length=2.0,
            word_count=2,
            sentences_count=2
        )

    def test_document_attributes(self):
        document = Document.objects.get(id=1)
        self.assertEqual(document.title, 'Title')
        self.assertEqual(document.source_type, 'pdf')
        self.assertEqual(document.content, 'Content')
        self.assertEqual(document.ltx, 1.0)
        self.assertEqual(document.smog_index, 1.0)
        self.assertEqual(document.language, 'en')
        self.assertEqual(document.sentences, 'Hello. World.')
        self.assertEqual(document.words, 'Hello Word')
        self.assertEqual(document.average_sentence_length, 2.0)
        self.assertEqual(document.word_count, 2)
        self.assertEqual(document.sentences_count, 2)
        self.assertEqual(document._meta.app_label, 'think')


class ContentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Document.objects.create(title='Title', content='Content')
        Content.objects.create(
            document=Document.objects.get(id=1),
            heading='Header',
            body_text='Body Text',
            section_number=1
        )

    def test_content_attributes(self):
        content = Content.objects.get(id=1)
        self.assertEqual(content.document, Document.objects.get(id=1))
        self.assertEqual(content.heading, 'Header')
        self.assertEqual(content.body_text, 'Body Text')
        self.assertEqual(content.section_number, 1)
        self.assertEqual(content._meta.app_label, 'think')
