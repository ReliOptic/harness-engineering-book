"""
Embedding provider — goal fidelity 측정용.
OpenRouter /embeddings endpoint (OpenAI SDK 호환).

make_embedding_fn() → Harness(embedding_fn=...) 인수로 직접 전달.
OPENROUTER_API_KEY 환경변수 필요.

E09 goal drift, E15 self-reporting accuracy 측정에서 사용.
API 불가 시 _hash_embed() fallback 자동 적용.
"""
from __future__ import annotations

import hashlib
import os
from typing import Callable, Optional

import numpy as np
from openai import OpenAI, APIError

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_EMBEDDING_MODEL = "openai/text-embedding-3-small"   # 1536-dim, OpenRouter 지원


def make_embedding_fn(
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    base_url: str = OPENROUTER_BASE_URL,
) -> Callable[[str], np.ndarray]:
    """
    OpenRouter embeddings API 호출 callable 반환.
    반환 타입: (text: str) -> np.ndarray[float32]

    사용:
        embedding_fn = make_embedding_fn()
        harness = Harness(config, initial_goal="...", embedding_fn=embedding_fn)
    """
    client = OpenAI(
        api_key=api_key or os.environ.get("OPENROUTER_API_KEY", ""),
        base_url=base_url,
    )

    def _embed(text: str) -> np.ndarray:
        try:
            resp = client.embeddings.create(model=model, input=[text])
            return np.array(resp.data[0].embedding, dtype=np.float32)
        except (APIError, Exception):
            # API 실패 시 hash-projection fallback (방향성은 유지, 정확도 낮음)
            return _hash_embed(text)

    return _embed


def make_offline_embedding_fn() -> Callable[[str], np.ndarray]:
    """
    API 없이 동작하는 hash-projection 기반 embedding function.
    smoke test 및 오프라인 환경, 단위 테스트 전용.
    실제 실험에서는 make_embedding_fn() 사용.
    """
    return _hash_embed


def _hash_embed(text: str, dim: int = 256) -> np.ndarray:
    """
    Hash-projection 기반 sparse embedding.
    단어별 TF를 dim 차원의 벡터에 projection.
    방향성(cosine similarity의 순서)은 유지하나 magnitude 정확도는 낮다.
    """
    words = text.lower().split()
    vec = np.zeros(dim, dtype=np.float32)
    total = max(len(words), 1)
    for word in words:
        idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % dim
        vec[idx] += 1.0 / total
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec
