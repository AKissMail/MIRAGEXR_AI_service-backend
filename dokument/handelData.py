from .documentParser import parse_pdf, parse_csv, parse_txt, parse_html
from .saveDocument import saveDocument


def handelDokument(request):

    document_file = request.get('document')
    if isinstance(document_file, list):
        document_file = document_file[0]
    file_type = document_file.content_type

    if file_type == 'application/pdf':
        saveDocument(parse_pdf(request), 'application/pdf', request)
        return True
    if file_type == 'text/csv':
        saveDocument(parse_csv(request), 'text/csv', request)
        return True
    if file_type == 'text/plain':
        saveDocument(parse_txt(request), 'text/plain', request)
        return True
    if file_type == 'text/html':
        saveDocument(parse_html(request), 'text/html', request)
        return True
    else:
        return False
