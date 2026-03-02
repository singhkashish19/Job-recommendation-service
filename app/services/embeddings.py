import hashlib
import numpy as np
from typing import List

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        self.dim = 384
        if SentenceTransformer is not None:
            try:
                self.model = SentenceTransformer(model_name)
                self.dim = self.model.get_sentence_embedding_dimension()
            except Exception:
                self.model = None

    def _fallback(self, texts: List[str]):
        out = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            arr = np.frombuffer(h, dtype=np.uint8).astype(np.float32)
            # expand/trim to self.dim deterministically
            rng = np.repeat(arr, int(np.ceil(self.dim / arr.size)))[: self.dim]
            vec = rng.astype(np.float32)
            vec = vec / (np.linalg.norm(vec) + 1e-9)
            out.append(vec)
        return np.stack(out)

    def embed(self, texts: List[str]):
        if self.model:
            emb = self.model.encode(texts, show_progress_bar=False)
            return np.array(emb, dtype=np.float32)
        return self._fallback(texts)
