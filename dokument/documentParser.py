import csv
import pdfplumber
from bs4 import BeautifulSoup


def parse_pdf(doc):
    """
    Parse PDF method extracts the text content from a given PDF document.

    Parameters:
    - doc (dict): A dictionary containing the PDF document information.
      - 'document' (str): The path to the PDF document that needs to be parsed.

    Returns:
    - str: The extracted text content from the PDF document.
    """
    with pdfplumber.open(doc['document']) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text


def parse_csv(doc):
    """

    Parse CSV File

    This method takes a dictionary as an argument and parses a CSV file specified in the dictionary's 'document' key. It reads the CSV file, concatenates the values of each row with a comma separator, and returns the resulting text.

    Parameters:
    - doc (dict): A dictionary containing the path of the CSV file to be parsed.

    Returns:
    - text (str): The concatenated text from the CSV file.

    """
    with open(doc['document'], 'r', encoding='utf-8', errors='replace') as csvfile:
        csv_reader = csv.reader(csvfile)
        text = ''
        for row in csv_reader:
            text += ', '.join(row) + '\n'
        return text


def parse_txt(doc):
    """

    Parse text file and return the content as a string.

    :param doc: A dictionary containing information about the document.
                 - 'document': The path to the text file.

    :return: The content of the text file as a string.

    """
    with open(doc['document'], 'r') as file:
        return file.read()


def parse_html(doc):
    """
    Parses HTML document and extracts the text content.

    :param doc: Dictionary containing the path of the HTML document.
                 The path is specified using the 'document' key in the dictionary.

    :return: Extracted text content from the HTML document.
    """
    with open(doc['document'], 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = ' '.join(soup.get_text().split())
        return text
