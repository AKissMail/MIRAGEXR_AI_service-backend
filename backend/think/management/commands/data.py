from django.core.management.base import BaseCommand
from pathlib import Path
from ...data_integration import (save_pdf_data, save_html_data, save_csv_data, save_txt_data)


class Command(BaseCommand):
    help = 'Process and load documents into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading data...')
        self.stdout.write('Process PDF')
        for pdf_path in Path('data').glob('*.pdf'):
            save_pdf_data(str(pdf_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {pdf_path.name}'))
        self.stdout.write('Process HTML')
        for html_path in Path('data').glob('*.html'):
            save_html_data(str(html_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {html_path.name}'))
        self.stdout.write('Process CSV')
        for csv_path in Path('data').glob('*.csv'):
            save_csv_data(str(csv_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {csv_path.name}'))
        for txt_path in Path('data').glob('*.txt'):
            save_txt_data(str(txt_path))
            self.stdout.write(self.style.SUCCESS(f'Processed {txt_path.name}'))
