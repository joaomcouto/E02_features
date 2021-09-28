def count_uppercase_words(text):
    """
    Count uppercase
    words on given text.
    """
    uppercase_words = map(str.isupper, text.split())
    value = sum(uppercase_words)
    return {'uppercase_words_number': value}
