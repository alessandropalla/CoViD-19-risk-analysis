from algorithms.genetic.genes import ConstGene
from analysis.model import SEIRModel
import pytest


@pytest.mark.parametrize("intervention_day", [10, 30, 80])
@pytest.mark.parametrize("R0", [1.5, 2.0, 2.6])
@pytest.mark.parametrize("effectiveness", [0.1, 0.5, 0.9])
@pytest.mark.parametrize("incubation_time", [1, 2, 3])
@pytest.mark.parametrize("remove_time", [1, 2, 3])
@pytest.mark.parametrize("population_size", [60000000])
@pytest.mark.parametrize("initial_exposed", [0, 10])
@pytest.mark.parametrize("initial_infected", [1, 10])
@pytest.mark.parametrize("initial_removed", [1, 10])
def test_model(intervention_day, R0, effectiveness, incubation_time, remove_time, population_size, initial_exposed,
               initial_infected, initial_removed):

    model = SEIRModel(intervention_day=ConstGene("intervention_day", intervention_day),
                      R0=ConstGene("R0", R0),
                      effectiveness=ConstGene("effectiveness", effectiveness),
                      incubation_time=ConstGene("incubation_time", incubation_time),
                      remove_time=ConstGene("remove_time", remove_time),
                      population_size=ConstGene("population_size", population_size),
                      initial_exposed=ConstGene("initial_exposed", initial_exposed),
                      initial_infected=ConstGene("initial_infected", initial_infected),
                      initial_removed=ConstGene("initial_removed", initial_removed))

    assert model

    samples = model.sample()
    assert isinstance(samples, list) and all([isinstance(sample, ConstGene) for sample in samples])
