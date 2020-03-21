from analysis.model import SEIRPopulation
import numpy as np
import pytest

@pytest.mark.parametrize("days", range(10, 200, 20))
def test_population(days):
    reference = np.linspace(0, days, days)
    population = SEIRPopulation(reference, 10, 10)

    # Check fitness function
    assert population.fitness()
    # Best models
    assert population.best_models()
    # CHeck population selection
    assert population.selection()
    # Check step
    assert population.step()