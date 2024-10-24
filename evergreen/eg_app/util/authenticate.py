import uuid
from evergreen.eg_app.models import Account, AuthToken

def signup(email: str, passwordHash: bytes) -> tuple[bool, str]:
    """ Attempts to register an account for the given credentials

    Only creates account, without generating auth token or signing in

    :param email: The already-validated email address to create the account with
    :param passwordHash: The already-validated and hashed password to use

    :returns: A tuple containing `(True, "")` if created successfully or
    `(False, "[reason]")` not be. The reason can be passed to the user.
    """
    try:
        Account.objects.get(email=email)
        return (False, "Account with that email already exists")
    except Account.DoesNotExist:
        newAcct = Account(email=email, pwdHash=passwordHash)
        newAcct.save()
        return (True, "")

def login(email: str, passwordHash: bytes) -> str:
    """ Attempts to login with the given credentials and make auth token

    :param email: The email address to login with
    :param passwordHash: The already-hashed password to login with

    :returns: Authentication token to send to user, `""` if unsuccessful
    """
    try:
        user = Account.objects.get(email=email, pwdHash=passwordHash)
        token = str(uuid.uuid4())
        newAuth = AuthToken(token=token, user=user)
        newAuth.save()
        return token
    except Account.DoesNotExist:
        return ""
