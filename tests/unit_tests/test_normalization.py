import numpy as np
from bittranslate.constants import SOFTMAX_T_FINAL
from bittranslate.normalization import sigmoid_normalize, softmax_normalize


def test_sigmoid_normalization():
    scores = [-4, -2, -1, 0, 1, 2, 4]
    result = sigmoid_normalize(scores)
    assert isinstance(result, list)
    assert all(isinstance(score, float) for score in result)
    answers = [
        0.01798620996209156,
        0.11920292202211755,
        0.2689414213699951,
        0.5,
        0.7310585786300049,
        0.8807970779778823,
        0.9820137900379085,
    ]
    np.testing.assert_almost_equal(result, answers, decimal=3)


def test_softmax_normalization():
    scores = [-4, -2, -1, 0, 1, 2, 4]
    result = softmax_normalize(scores, t=SOFTMAX_T_FINAL)
    assert isinstance(result, list)
    assert all(isinstance(score, float) for score in result)
    answers = [
        0.00027655841003102497,
        0.0020435056063503087,
        0.005554824156096227,
        0.015099577563801724,
        0.04104490730909013,
        0.11157162568908555,
        0.8244090012655451,
    ]
    np.testing.assert_almost_equal(result, answers, decimal=3)


def test_softmax_normalization_low_t():
    scores = [-4, -2, -1, 0, 1, 2, 4]
    result = softmax_normalize(scores, t=0.5)
    assert isinstance(result, list)
    assert all(isinstance(score, float) for score in result)
    answers = [
        1.1020095210930655e-07,
        6.016768117059262e-06,
        4.445823715120823e-05,
        0.00032850440836984036,
        0.0024273375021907737,
        0.017935732974725827,
        0.9792578399084931,
    ]
    np.testing.assert_almost_equal(result, answers, decimal=3)


def test_softmax_normalization_high_t():
    scores = [-4, -2, -1, 0, 1, 2, 4]
    result = softmax_normalize(scores, t=5.0)
    assert isinstance(result, list)
    assert all(isinstance(score, float) for score in result)
    answers = [
        0.0570420862604209,
        0.08509679308827968,
        0.10393745778861006,
        0.12694949761916458,
        0.15505646653909552,
        0.18938639590142134,
        0.28253130280300787,
    ]
    np.testing.assert_almost_equal(result, answers, decimal=3)
