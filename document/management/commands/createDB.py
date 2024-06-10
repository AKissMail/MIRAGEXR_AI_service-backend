import chromadb
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Creates the Chroma DB using a PersistentClient.
    """
    def handle(self, *args, **options):
        print("Creating the Chroma DB")
        chromadb.PersistentClient(path="vectorDB")
