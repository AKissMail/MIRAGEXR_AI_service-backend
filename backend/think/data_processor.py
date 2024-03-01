from django.core.management.base import BaseCommand
from pathlib import Path
from .data_integration import save_pdf_data, save_html_data, save_csv_data, save_url_data

das hier muss noch angepasst werden und ich brauche Test daten für das Komando...
class Command(BaseCommand):
    help = 'Process and load documents into the database'

    def handle(self, *args, **options):
        for pdf_path in Path('path/to/pdfs').glob('*.pdf'):
            save_pdf_data(str(pdf_path), title=pdf_path.stem)
            self.stdout.write(self.style.SUCCESS(f'Processed {pdf_path.name}'))