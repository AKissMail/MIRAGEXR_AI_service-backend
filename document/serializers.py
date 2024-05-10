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
    """
    Serializer for the Configuration model.

    Attributes:
        prompt_start (serializers.CharField): The starting prompt for the configuration.
        prompt_end (serializers.CharField): The ending prompt for the configuration.
        context_start (serializers.CharField): The starting context for the configuration.
        context_end (serializers.CharField): The ending context for the configuration.
        database_name (serializers.CharField): The database name for the configuration.
        update_database (serializers.BooleanField): Flag indicating whether to update the database.
        new_database (serializers.BooleanField): Flag indicating whether to create a new database.
        delete_database (serializers.BooleanField): Flag indicating whether to delete the database.
    """
    prompt_start = serializers.CharField()
    prompt_end = serializers.CharField()
    context_start = serializers.CharField()
    context_end = serializers.CharField()
    database_name = serializers.CharField()
    update_database = serializers.BooleanField()
    new_database = serializers.BooleanField()
    delete_database = serializers.BooleanField()


class OptionSerializer(serializers.Serializer):
    """
    The OptionSerializer class is a serializer for an options field.

    Attributes:
        options (CharField): A serializer field to store the options.json.

    Example:
        serializer = OptionSerializer(data={'options': 'Option 1, Option 2'})
        if serializer.is_valid():
            options = serializer.validated_data['options']
            # Do something with the options
    """
    data = serializers.CharField()
