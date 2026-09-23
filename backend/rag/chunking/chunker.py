from typing import Any, Dict, List


class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = " ".join(words[start:end])
            chunks.append({
                "content": chunk_text,
                "chunk_index": len(chunks),
                "metadata": {
                    **metadata,
                    "word_count": len(words[start:end]),
                    "start_word": start,
                },
            })
            if end == len(words):
                break
            start += self.chunk_size - self.chunk_overlap

        return chunks
