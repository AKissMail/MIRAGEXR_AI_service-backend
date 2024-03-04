import csv
import PyPDF2
from bs4 import BeautifulSoup


def parse_pdf(file_path):
    """
     Extracts and returns the text from a PDF file.
     Parameters:
     - file_path (str): The path to the PDF file to be parsed.
     Returns:
     - str: The extracted text from the PDF file.
     """
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n'
        return text


def parse_csv(file_path):
    """
     Extracts and returns the text from a CSV file.
     Parameters:
     - file_path (str): The path to the CSV file to be parsed.
     Returns:
     - str: The extracted text from the PDF file.
     """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        csv_reader = csv.reader(file)
        text = ''
        for row in csv_reader:
            text += ', '.join(row) + '\n'
        return text


def parse_html(file_path):
    """
     Extracts and returns the text from an HTML file.
     Parameters:
     - file_path (str): The path to the HTML file to be parsed.
     Returns:
     - str: The extracted text from the PDF file.
     """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = ' '.join(soup.get_text().split())
        return text


def pars_txt(file_path):
    """
    Reads and returns the entire content of a text file.
    Parameters:
        - file_path (str): The path to the text file to be read.
    Returns:
        - str: The content of the text file.
    """
    with open(file_path, 'r') as file:
        return file.read()
