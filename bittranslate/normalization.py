from typing import List
import numpy as np


def sigmoid_normalize(scores: List[float]) -> List[float]:
    np_scores = np.array(scores)
    norm_scores = 1 / (1 + np.exp(-np_scores))

    return norm_scores.tolist()


def softmax_normalize(scores: List[float], t: float = 1.0) -> List[float]:
    np_scores = np.array(scores)
    norm_scores = np.exp(np_scores / t) / np.sum(np.exp(np_scores / t))

    return norm_scores.tolist()
