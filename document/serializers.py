from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    """A serializer class to serialize documents.

    This class is a subclass of `serializers.Serializer` and is used to
    serialize documents. It provides fields for document file, name, and database.

    Attributes:
        document: A `serializers.FileField` field for the document file.
        name: A `serializers.CharField` field for the name of the document.
        database: A `serializers.CharField` field for the database the document is associated with.

    """
    document = serializers.FileField()
    name = serializers.CharField()
    database = serializers.CharField()


class ConfigurationSerializer(serializers.Serializer):
    prompt_start = serializers.CharField()
    prompt_end = serializers.CharField()
    context_start = serializers.CharField()
    context_end = serializers.CharField()
    database_name = serializers.CharField()
    update_database = serializers.BooleanField()
    new_database = serializers.BooleanField()
    delete_database = serializers.BooleanField()

