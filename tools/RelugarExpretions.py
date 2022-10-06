
import re 
import regex
from sqlalchemy import false
def validRFC(rfc):
        valid = re.compile(r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$')
        return valid.match(rfc)
def validPhone(phone):
        valid = re.compile(r'^[0-9]{10}$')
        return valid.match(phone)
def validEmail(email):
        valid = re.compile(r'^[\w-]+@[\w-]+\.[\w-]+$')
        return valid.match(email)
def validTaxid(taxid):
        valid = re.compile(r'^[0-9]{9}$')
        return valid.match(taxid)
def validDate(date):
        valid = re.compile(r'^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$')
        return valid.match(date)
def searchDate(date):
        pattern = re.compile(r'^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$', re.IGNORECASE|re.M)
        return re.findall(pattern,date)
def searchRFC(rfc):
        pattern = regex.compile(r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$', re.IGNORECASE|re.M)
        return regex.search(pattern,rfc)
def searchCustomWord(words,matcher):
        if re.search(matcher,words,re.IGNORECASE):
                return True
        else:
                return False