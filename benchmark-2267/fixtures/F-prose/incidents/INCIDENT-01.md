# Incident 01: exposed vector store

A Qdrant instance was bound to 0.0.0.0 with no API key and no TLS, and the collection was readable from the internet. Lesson: always enable authentication.
