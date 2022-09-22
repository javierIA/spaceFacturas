from tools import RelugarExpretions


def validate_rfc(word):
    if RelugarExpretions.validRFC(word):
        return word
def validate_date(word):
    if RelugarExpretions.validDate(word):
        return word
def db_select(word):
    return db.get_client(word)
def validte_words(word,words):
    for importword in words:
        if RelugarExpretions.searchCustomWord(word, importword):
            return word
 
def word_finder(word,matcher):
    if RelugarExpretions.searchCustomWord(word, matcher):
        return word       
