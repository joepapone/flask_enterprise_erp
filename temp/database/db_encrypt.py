from os import urandom
from hashlib import pbkdf2_hmac
from hmac import compare_digest

# Hash and salt password using sha256 ou sha512
def encode(password: str) -> tuple:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = urandom(16)
    pw_hash = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=100000)
    #print('Salt:{0} / Hash:{1}'.format(salt, pw_hash))
    return salt.hex(), pw_hash.hex()

# Compare hashed and salted password with user password
def decode(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    salt = bytes.fromhex(salt)
    pw_hash = bytes.fromhex(pw_hash)
    return compare_digest(
        pw_hash,
        pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=100000)
    )