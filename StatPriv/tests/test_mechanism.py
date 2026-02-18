import numpy as np
import pytest

from src.mechanism import (
    GaussianNoise,
    LaplaceNoise,
    LaplaceNoiseEpsilonDelta,
    PoissonSubsampling,
    PureStatisticalPrivacy,
    SubsamplingWithReplacement,
    SubsamplingWithoutReplacement,
)


def test_pure_statistical_privacy():
    mechanism = PureStatisticalPrivacy(seed=42)
    data = np.array([1.0, 2.0, 3.0])

    pre = mechanism.pre_query_mechanism(data, datasize=data.size)
    post = mechanism.post_query_mechanism(10.5, datasize=data.size)

    assert np.array_equal(pre, data)
    assert post == 10.5


def test_poisson_subsampling():
    mechanism = PoissonSubsampling([0.5], seed=0)
    data = np.arange(10)

    sampled = mechanism.pre_query_mechanism(data, datasize=data.size)

    assert len(sampled) == mechanism.sample_size
    assert set(sampled).issubset(set(data.tolist()))


def test_subsampling_without_replacement():
    mechanism = SubsamplingWithoutReplacement([5], seed=0)

    with pytest.raises(ValueError):
        mechanism.pre_query_mechanism(np.array([1, 2, 3]), datasize=3)


def test_subsampling_with_replacement():
    mechanism = SubsamplingWithReplacement([5], seed=1)
    data = np.array([1, 2, 3])

    sampled = mechanism.pre_query_mechanism(data, datasize=data.size)

    assert sampled.size == 5


def test_gaussian_noise():
    mechanism = GaussianNoise([0.5], seed=123)

    noisy = mechanism.post_query_mechanism(0.0, datasize=1)

    assert noisy != 0.0


def test_laplace_noise():
    mechanism = LaplaceNoise([0.5], seed=123)

    noisy = mechanism.post_query_mechanism(0.0, datasize=1)

    assert noisy != 0.0


def test_laplace_noise_epsilon_delta():
    mechanism = LaplaceNoiseEpsilonDelta(seed=123)

    with pytest.raises(ZeroDivisionError):
        mechanism.post_query_mechanism(0.0, datasize=1, epsilon=0, sensitivity=1)

    with pytest.raises(ValueError):
        mechanism.post_query_mechanism(0.0, datasize=1, epsilon=1, sensitivity=-1)

    noisy = mechanism.post_query_mechanism(0.0, datasize=1, epsilon=1.0, sensitivity=1.0)
    assert noisy != 0.0
