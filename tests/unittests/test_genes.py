from algorithms.genetic.genes import PoissonGene, NormalGene, UniformGene, UniformIntGene
import numpy as np
import pytest


@pytest.mark.parametrize("value", np.linspace(0, 20, 10))
@pytest.mark.parametrize("min_value", np.linspace(0, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_poisson(value, min_value, delta):
    gene = PoissonGene("dummy", value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta for x in samples])


@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_uniform(value, min_value, delta):
    gene = UniformGene("dummy", value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta for x in samples])


@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_normal(value, min_value, delta):
    gene = NormalGene("dummy", value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta for x in samples])


@pytest.mark.parametrize("value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("min_value", np.linspace(-10, 10, 10))
@pytest.mark.parametrize("delta", np.linspace(0, 10, 10))
def test_sample_uniformint(value, min_value, delta):
    gene = UniformIntGene("dummy", value, min_val=min_value, max_val=min_value + delta)
    samples = [gene.sample().value for _ in range(100)]
    assert all([x >= min_value and x <= min_value + delta for x in samples])


@pytest.mark.parametrize("gene_type", [PoissonGene, NormalGene, UniformGene, UniformIntGene])
@pytest.mark.parametrize("value", [1, 5, 10, 30])
@pytest.mark.parametrize("min_value", [-np.inf, 0, 2])
@pytest.mark.parametrize("max_value", [+np.inf, 3, 5, 7])
@pytest.mark.parametrize("delta", [1, 2, 3, 10])
def test_generations(gene_type, value, min_value, max_value, delta):
    gene = gene_type("dummy", value, min_val=min_value, max_val=max_value).sample()
    for idx in range(10):
        assert gene.value >= min_value and gene.value <= max_value
        gene = gene.sample()