from langdetect import detect
from textstat import textstat
from nltk.tokenize import ToktokTokenizer


def extract_metadata(text):
    """

    Extracts metadata from the given text.

    :param text: The text from which metadata needs to be extracted
    :type text: str
    :return: A dictionary containing the extracted metadata
    :rtype: dict

    """
    language = detect(text)
    toktok = ToktokTokenizer()
    metadata = {
        'language': language,
        'sentences': toktok.tokenize(text),
        'words': toktok.tokenize(text),
    }
    metadata['word_count'] = len(metadata['words'])
    metadata['sentences_count'] = len(metadata['sentences'])
    metadata['average_sentence_length'] = len(metadata['words']) / len(metadata['sentences']) if metadata[
        'sentences'] else 0
    metadata['sentences'] = " ".join(metadata['sentences'])
    metadata['words'] = " ".join(metadata['words'])

    if language == "no":
        metadata['ltx'] = ltx(text)
    if language == "en":
        metadata['smog_index'] = textstat.smog_index(text)

    return metadata


def ltx(text):
    """
    Calculate the Lix score for a given text.

    :param text: The text to calculate the Lix score for.
    :type text: str
    :return: The Lix score of the text. If the text has no sentences, None is returned.
    :rtype: float
    """
    words = text.split()
    num_words = len(words)
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    long_words = sum(1 for word in words if len(word) > 6)

    if num_sentences == 0:
        return None

    lix_score = (num_words / num_sentences) + ((long_words / num_words) * 100)
    return round(lix_score, 4)
