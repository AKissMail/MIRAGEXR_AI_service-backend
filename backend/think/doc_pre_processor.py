import csv
import PyPDF2
from bs4 import BeautifulSoup
from django.contrib.sites import requests


def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n'
        return text


def parse_csv(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        csv_reader = csv.reader(file)
        text = ''
        for row in csv_reader:
            text += ', '.join(row) + '\n'
        return text


def parse_html(file_path):
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        # Optional: Entfernen von Skript- und Stil-Tags
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Den Text extrahieren und zusätzlichen Whitespace entfernen
        text = ' '.join(soup.get_text().split())
        return text


def pars_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    para = [p.text for p in soup.find_all('p')]
    return '\n'.join(para)


def pars_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
