import csv
import pdfplumber
from bs4 import BeautifulSoup


def parse_pdf(doc):
    with pdfplumber.open(doc['document']) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text


def parse_csv(doc):
    with open(doc['document'], 'r', encoding='utf-8', errors='replace') as csvfile:
        csv_reader = csv.reader(csvfile)
        text = ''
        for row in csv_reader:
            text += ', '.join(row) + '\n'
        return text


def parse_txt(doc):
    with open(doc['document'], 'r') as file:
        return file.read()


def parse_html(doc):
    with open(doc['document'], 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = ' '.join(soup.get_text().split())
        return text
