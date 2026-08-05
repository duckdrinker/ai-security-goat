"""
bad_pickle_load_urlopen.py
Triggers unsafe-deserializer-on-remote-artifact: streams a remote artifact
directly into pickle.load(), the most direct form of this weakness — any
attacker who can influence the URL content (or intercept the connection) can
execute arbitrary code in-process.
"""
import pickle
from urllib.request import urlopen

with urlopen("http://models.example-artifacts.net/embeddings_cache.pkl") as remote_file:
    embeddings_cache = pickle.load(remote_file)
