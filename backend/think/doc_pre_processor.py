import csv
import PyPDF2
from bs4 import BeautifulSoup
from django.contrib.sites import requests


def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader()
        text = ''
        for page in pdf_reader.pages:
            text += page.extractText() + '\n'
        return text


def parse_csv(file_path):
    with open(file_path, 'rb') as file:
        csv_reader = csv.reader(file)
        text = ''
        for row in csv_reader:
            text += row[0] + '\n'
        return text


def parse_html(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()


def pars_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    para = [p.text for p in soup.find_all('p')]
    return '\n'.join(para)
