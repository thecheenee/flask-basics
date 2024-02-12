import re

def is_email_valid(emailid):
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  if(re.fullmatch(regex, emailid)):
    return True
  else:
    return False