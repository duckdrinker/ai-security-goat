"""
Triggers vector-search-without-top-k-cap: `k` is computed as `index.ntotal`
— the total number of vectors currently in the index — so the "top-k"
search always returns every single vector, ranked. As the index grows, so
does the size of every query's result set, with no independent cap
decoupling retrieval size from index size.
"""
import faiss
import numpy as np

index = faiss.read_index("docs.index")


def search(embedding: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k = index.ntotal  # "give me everything, ranked" — not a top-k search
    distances, indices = index.search(embedding.reshape(1, -1), k)
    return distances, indices
