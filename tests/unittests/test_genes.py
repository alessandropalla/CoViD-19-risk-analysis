from analysis.genetic_algorithms.genes import PoissonGene, NormalGene, UniformGene, UniformIntGene
import numpy as np
import pytest


@pytest.mark.parametrize("value", np.linspace(0, 20, 10))
@pytest.mark.parametrize("min_value", np.linspace(0, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_poisson(value, min_value, delta):
    gene = PoissonGene(value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta
                for x in samples])

@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_uniform(value, min_value, delta):
    gene = UniformGene(value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta
                for x in samples])

@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_normal(value, min_value, delta):
    gene = NormalGene(value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta
                for x in samples])

@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_uniformint(value, min_value, delta):
    gene = UniformIntGene(value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta
                for x in samples])