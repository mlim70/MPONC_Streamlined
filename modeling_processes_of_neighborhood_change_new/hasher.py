#hasher.py

import hashlib
import pickle

def hash_function(*args, **kwargs):
    """ Hash function """
    hasher = hashlib.md5()
    for arg in args:
        hasher.update(pickle.dumps(arg))
    for key, value in sorted(kwargs.items()):
        hasher.update(pickle.dumps((key, value)))
    return hasher.hexdigest()