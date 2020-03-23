from analysis.model import SEIRPopulation
import numpy as np
import pytest


@pytest.mark.parametrize("days", range(10, 200, 20))
@pytest.mark.parametrize("filename", [
    "tests/unittests/test_configurations/population_test_1.yaml",
    "tests/unittests/test_configurations/population_test_2.yaml"
])
def test_population(days, filename):
    reference = np.linspace(0, days, days)
    population = SEIRPopulation(reference, filename)

    # Check fitness function
    assert population.fitness()
    # Best models
    assert population.best_models()
    # CHeck population selection
    assert population.selection()
    # Check step
    assert population.step()