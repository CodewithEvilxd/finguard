import hashlib
from typing import List
import numpy as np


class Embedder:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates a normalized dense vector embedding.
        In offline/local mode, generates a deterministic pseudo-semantic projection vector
        based on token hashing so that tests and local development run without external API dependencies.
        """
        tokens = text.lower().split()
        vector = np.zeros(self.dimension, dtype=np.float32)

        for token in tokens:
            token_hash = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:8], 16)
            idx = token_hash % self.dimension
            val = (token_hash % 1000) / 500.0 - 1.0
            vector[idx] += val

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        a = np.array(v1)
        b = np.array(v2)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))


embedder = Embedder()
