import uuid
from eg_app.models import Account, AuthToken
import bcrypt

def register(email: str, password: str) -> tuple[bool, str]:
    """ Attempts to register an account for the given credentials

    Only creates account, without generating auth token or signing in

    :param email: The already-validated email address to create the account with
    :param password: The already-validated password to use

    :returns: A tuple containing `(True, "")` if created successfully or
    `(False, "[reason]")` not be. The reason can be passed to the user.
    """
    try:
        Account.objects.get(email=email)
        return (False, "Account with that email already exists")
    except Account.DoesNotExist:
        pwdHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        newAcct = Account(email=email, pwdHash=pwdHash)
        newAcct.save()
        return (True, "")

def login(email: str, password: str) -> str:
    """ Attempts to login with the given credentials and make auth token

    :param email: The email address to login with
    :param password: The password to login with

    :returns: Authentication token to send to user, `""` if unsuccessful
    """
    try:
        user = Account.objects.get(email=email)
        if not bcrypt.checkpw(password.encode(), user.pwdHash):
            # Invalid password
            return ""
        token = str(uuid.uuid4())
        newAuth = AuthToken(token=token, user=user)
        newAuth.save()
        return token
    except Account.DoesNotExist:
        return ""
