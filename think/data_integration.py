import os
from dokument.models import Document, Content
from .doc_pre_processor import parse_pdf, parse_csv, parse_html, pars_txt


def save_pdf_data(file_path):
    """
     Processes and saves the content of a PDF file into the Database.

     Parameters:
        - file_path (str): The file system path to the PDF file to be processed.
     """
    text = parse_pdf(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='pdf', content=text)
    Content.objects.create(document=document, body_text=text)


def save_csv_data(file_path):
    """
        Processes and saves the content of a CSV file into the Database.

        Parameters:
            - file_path (str): The file system path to the CSV file to be processed.
    """
    text = parse_csv(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='csv', content=text)
    Content.objects.create(document=document, body_text=text)


def save_html_data(file_path):
    """
        Processes and saves the content of an HTML file into the Database.

        Parameters:
            - file_path (str): The file system path to the HTML file to be processed.
    """
    text = parse_html(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='html', content=text)
    Content.objects.create(document=document, body_text=text)


def save_txt_data(file_path):
    """
        Processes and saves the content of a TXT file into the Database.

        Parameters:
            - file_path (str): The file system path to the TXT file to be processed.
    """
    text = pars_txt(file_path)
    title = os.path.basename(file_path)
    document = Document.objects.create(title=title, source_type='txt', content=text)
    Content.objects.create(document=document, body_text=text)
