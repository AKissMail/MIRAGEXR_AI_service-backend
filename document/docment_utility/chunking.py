import nltk

DEFAULT_CHUNK_SIZE = 200
DEFAULT_OVERLAP = 50


def create_text_chunks(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_OVERLAP):
    sentences = nltk.sent_tokenize(text)
    words = split_into_words(sentences)
    chunks = generate_word_chunks(words, chunk_size, overlap)
    return chunks


def split_into_words(sentences):
    words = []
    for sentence in sentences:
        words.extend(sentence.split())
    return words


def generate_word_chunks(words, chunk_size, overlap):
    chunks = []
    index = 0
    while index < len(words):
        chunk = ' '.join(words[index:index + chunk_size])
        chunks.append(chunk)
        index += (chunk_size - overlap)
    return chunks
