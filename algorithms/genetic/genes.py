import numpy as np

# A gene that is sampling using a poisson distribution
class __Gene():
  def __init__(self, value, distribution, **params):
    # Values that can mutate througth generations
    self.value = value
    # Values that do not mutate througth generations 
    self.params = params
    # When mutate, sample from a probability distribution
    self.distribution = distribution

  def sample(self, n=1):
    min_val = self.params["min_val"] if "min_val" in self.params.keys() else -np.inf
    max_val = self.params["max_val"] if "max_val" in self.params.keys() else np.inf
    return type(self)(np.clip(self.distribution(self.value, n), min_val, max_val), **self.params)

class NormalGene(__Gene):
  def __init__(self, value, **params):
    sigma = params["sigma"] if "sigma" in params.keys() else 0.1
    super().__init__(value, lambda x, n: np.random.normal(x, sigma, n), **params)

class PoissonGene(__Gene):
  def __init__(self, value, **params):
    sigma = params["sigma"] if "sigma" in params.keys() else 0.1
    super().__init__(value, np.random.poisson, **params)

class UniformGene(__Gene):
  def __init__(self, value, **params):
    delta = params["delta"] if "delta" in params.keys() else 1
    super().__init__(value, lambda x, n: np.random.uniform(x-delta, x+delta, n), **params)

class UniformIntGene(__Gene):
  def __init__(self, value, **params):
    delta = params["delta"] if "delta" in params.keys() else 1
    super().__init__(value, lambda x, n: np.random.randint(x-delta, x+delta, n), **params)

class ConstGene(__Gene):
  def __init__(self, value, **params):
    super().__init__(value, lambda x, n: x * np.ones((n, 1)), **params)
