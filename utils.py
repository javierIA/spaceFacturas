from tools import RelugarExpretions


def validate_rfc(word):
    if RelugarExpretions.validRFC(word):
        return word
def validate_date(word):
    if RelugarExpretions.validDate(word):
        return word

def validte_words(word,words):
    if RelugarExpretions.searchCustomWord(words,word):
        print("true")
        return True
 
def word_finder(word,matcher):
    if RelugarExpretions.searchCustomWord(word, matcher):
        return word       
