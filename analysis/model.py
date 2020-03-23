from algorithms.genetic.genes import ConstGene, UniformGene, UniformIntGene, PoissonGene, NormalGene
from algorithms.genetic.individuals import GeneticModel
from algorithms.genetic.population import Population
from scipy.integrate import solve_ivp
import numpy as np


class SEIR():
    def __init__(self, intervention_day, R0, effectiveness, mean_incubation_time, mean_remove_time):

        # The day when restrictive measure where applied since the beginning of the epidemic
        self.intervention_day = intervention_day
        # Infection Rate. Is calculated as the inverse of the mean latent period
        self.sigma = 1 / mean_incubation_time
        # Remove Rate, calculated as the inverse of the mean infectious period
        self.gamma = 1 / mean_remove_time

        self.beta_0 = R0 * self.gamma  # Transmission Rate before intervention
        self.beta_1 = effectiveness * self.beta_0  # Transmission Rate after intervention

    @staticmethod
    def __model(t, y, intervention_day, beta_0, beta_1, sigma, gamma):
        # Extract compartements from y vector
        S, E, I, R = y

        # Total number of people
        N = sum(y)

        # The beta depends on the intervention day
        # Here we are modelling a threshold but it may be not the
        # best way since adoption of lockdown measure is gradual
        beta = beta_0 if t <= intervention_day else beta_1

        # New exposed, infected and removed
        new_exposed = beta * S * I / N
        new_infected = sigma * E
        new_removed = gamma * I

        # SEIR model
        dS = -new_exposed
        dE = new_exposed - new_infected
        dI = new_infected - new_removed
        dR = new_removed

        return dS, dE, dI, dR

    def integrate(self, t, y0):

        # Integrate the SEIR equations over the time t.
        results = solve_ivp(
            self.__model,  # the SEIR differential equation
            t_span=(min(t), max(t)),
            y0=y0,
            t_eval=t,
            args=[self.intervention_day, self.beta_0, self.beta_1, self.sigma, self.gamma],
            method="RK45",
            vectorized=True)
        # return results.y.T
        y = results.y.T
        return [y[:, idx] for idx in range(y.shape[1])]


class SEIRModel(GeneticModel):
    def __init__(self, intervention_day, R0, effectiveness, incubation_time, remove_time, population_size,
                 initial_exposed, initial_infected, initial_removed):
        # Optimization parameters
        genes = [
            intervention_day, R0, effectiveness, incubation_time, remove_time, population_size, initial_exposed,
            initial_infected, initial_removed
        ]
        # Optimization model
        model = SEIR(intervention_day=intervention_day.value,
                     R0=R0.value,
                     effectiveness=effectiveness.value,
                     mean_incubation_time=incubation_time.value,
                     mean_remove_time=remove_time.value)
        # Initialize genetic model
        super().__init__(model, genes)
        # Set initial condition
        self.set_y0([population_size.value, initial_exposed.value, initial_infected.value, initial_removed.value])


class SEIRPopulation(Population):
    def __init__(self, reference, filename):
        element_fitness = lambda elem: elem.fitness(reference, [False, False, False, True])
        super().__init__(SEIRModel, element_fitness, filename)