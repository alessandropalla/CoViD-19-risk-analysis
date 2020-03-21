from analysis.model import SEIR
import numpy as np
import pytest

@pytest.mark.parametrize("intervention_day", range(0, 100, 10))
@pytest.mark.parametrize("R0", range(1, 3, 5))
@pytest.mark.parametrize("effectivness", np.linspace(0.1, 1, 3))
@pytest.mark.parametrize("mean_incubation_time", np.linspace(1, 10, 3))
@pytest.mark.parametrize("mean_removal_time", np.linspace(1, 10, 3))
def test_integration(intervention_day, R0, effectivness, mean_incubation_time, mean_removal_time):
    model = SEIR(intervention_day=intervention_day,
                 R0 = R0,
                 effectivness = effectivness,
                 mean_incubation_time = mean_incubation_time,
                 mean_removal_time = mean_removal_time)

    y0 = [60000000, 0, 1, 0]
    t =  list(range(200))
    S, E, I, R = model.integrate(t, y0)
