import os
from .models import Document, Content
from .doc_pre_processor import parse_pdf, parse_csv, parse_html, pars_txt


def save_pdf_data(file_path):
    text = parse_pdf(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='pdf', content=text)
    Content.objects.create(document=document, body_text=text)


def save_csv_data(file_path):
    text = parse_csv(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='csv', content=text)
    Content.objects.create(document=document, body_text=text)


def save_html_data(file_path):
    text = parse_html(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='html', content=text)
    Content.objects.create(document=document, body_text=text)

def save_txt_data(file_path):
    text = pars_txt(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='txt', content=text)
    Content.objects.create(document=document, body_text=text)
