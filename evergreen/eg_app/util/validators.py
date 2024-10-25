import email_validator as ev
import re

def validate_email(email: str, check_deliverability=False) -> bool:
    """ Checks if the given email passes validation requirements

    Validation requirements:
    - Valid University at Buffalo email only
      - User is comprised of letters followed by optional numbers
      - User is 4-8 chars, inclusive
      - Server is (optional subdomain).buffalo.edu

    :param email: The email addresses from the user to validate
    :param check_deliverability: Whether or not to perform a DNS query to see  \
    if the domain can receive mail. Recommended to use `True` on registration, \
    `False` on regular login. See https://pypi.org/project/email-validator/
    
    :returns: `True` if the email address passes requirements, `False` otherwise
    """

    try:
      email_info = ev.validate_email(email, check_deliverability=check_deliverability)

      local = email_info.local_part
      domain = email_info.domain

      l_len = 4 <= len(local) and len(local) <= 8
      # If the local part (before the @) is [4-8] characters long, inclusive
      l_match = re.match(r"^[a-z]+[0-9]*$", local, re.I) != None
      # If the local part (before the @) is exactly a valid UBIT name
      d_match = re.match(r"^(?:[a-z]*\.)?buffalo\.edu$", string=domain) != None
      # If the domain (after the @) is exactly (optional subdomain).buffalo.edu

      return l_len and l_match and d_match
      
    except ev.EmailNotValidError as e:
      return False

def validate_password(password: str) -> bool:
    """ Checks if the given password passes validation requirements

    Validation requirements:
    - Length between 12 and 255 chars (inclusive)

    :param password: The password from the user to validate
    
    :returns: `True` if the password passes requirements, `False` otherwise
    """

    return 12 <= len(password) and len(password) < 256
