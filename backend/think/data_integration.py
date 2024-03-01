from .models import Document, Content
from .doc_pre_processor import parse_pdf, parse_csv, parse_html, pars_url

def save_pdf_data(file_path, title, author=None):
    text = parse_pdf(file_path)
    document = Document.objects.create(title=title,source_type='pdf', content=text, author=author)
    Content.objects.create(document=document, body_text=text)


def save_csv_data(file_path, title, author=None):
    text = parse_csv(file_path)
    document = Document.objects.create(title=title, source_type='csv', content=text, author=author)
    Content.objects.create(document=document, body_text=text)

def save_html_data(file_path, title, author=None):
    text = parse_html(file_path)
    document = Document.objects.create(title=title, source_type='html', content=text, author=author)
    Content.objects.create(document=document, body_text=text)

def save_url_data(file_path, title, author=None):
    text = pars_url(file_path)
    document = Document.objects.create(title=title, source_type='html', content=text, author=author)
    Content.objects.create(document=document, body_text=text)
