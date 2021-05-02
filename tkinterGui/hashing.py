import hashlib


def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def verify_pw_hash(password, pw_hash):  # pw_hash is hash from the database
    if hash_pass(password) == pw_hash:
        return True

    return False
