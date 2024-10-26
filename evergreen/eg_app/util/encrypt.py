import bcrypt




def encrypt(plaintext):

    # encode plaintext string to bytes
    plaintext = plaintext.encode('')

    hashed_password = bcrypt.hashpw(plaintext, bcrypt.gensalt())

    return hashed_password