def count_uppercase_words(text):
    """
    Count uppercase
    words on given text.
    """
    uppercase_words = map(str.isupper, text.split())
    value = sum(uppercase_words)
    return value

print(count_uppercase_words("ÚLTIMO MINUTO: Washington Post confirma a origem do paciente zero do coronavírus"))
