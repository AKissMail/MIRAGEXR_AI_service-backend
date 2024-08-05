import nltk
# DEFAULT VALUES
DEFAULT_CHUNK_SIZE = 200
DEFAULT_OVERLAP = 50


def create_text_chunks(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_OVERLAP):
    """
    Splits the given text into chunks of specified size, with optional overlap.

    Args:
        text (str): The text to be divided into chunks.
        chunk_size (int, optional): The size of each chunk. Defaults to DEFAULT_CHUNK_SIZE.
        overlap (int, optional): The amount of overlap between chunks. Defaults to DEFAULT_OVERLAP.

    Returns:
        list: A list of text chunks.

    """
    sentences = nltk.sent_tokenize(text)
    words = split_into_words(sentences)
    chunks = generate_word_chunks(words, chunk_size, overlap)
    return chunks


def split_into_words(sentences):
    """
    Split the given sentences into words.

    Parameters:
    sentences (list): A list of sentences.

    Returns:
    list: A list of words extracted from the sentences.
    """
    words = []
    for sentence in sentences:
        words.extend(sentence.split())
    return words


def generate_word_chunks(words, chunk_size, overlap):
    """

        Generate word chunks from given list of words.

        Args:
            words (List[str]): List of words.
            chunk_size (int): The size of each word chunk.
            overlap (int): The overlap between each word chunk.

        Returns:
            List[str]: List of word chunks.

    """
    chunks = []
    index = 0
    while index < len(words):
        chunk = ' '.join(words[index:index + chunk_size])
        chunks.append(chunk)
        index += (chunk_size - overlap)
    return chunks
