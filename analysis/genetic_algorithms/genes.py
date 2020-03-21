import numpy as np

# A gene that is sampling using a poisson distribution
class Gene():
  def __init__(self, value, distribution, min_val=-np.inf, max_val=np.inf):
    self.value = value
    self.distribution = distribution
    self.min_val = min_val
    self.max_val = max_val

  def sample(self, n=1):
    return type(self)(np.clip(self.distribution(self.value, n), self.min_val, self.max_val))

class ConstGene(Gene):
    def __init__(self, value, min_val=-np.inf, max_val=np.inf):
        super().__init__(value, lambda x, n: x * np.ones((n, 1)),
                        min_val, max_val)

class NormalGene(Gene):
  def __init__(self, value, sigma=0.1, min_val=-np.inf, max_val=np.inf):
    super().__init__(value, lambda x, n: np.random.normal(x, sigma, n),
                     min_val, max_val)

class PoissonGene(Gene):
  def __init__(self, value, sigma=0.1, min_val=-np.inf, max_val=np.inf):
    super().__init__(value, np.random.poisson,
                     min_val, max_val)

class UniformGene(Gene):
  def __init__(self, value, delta=1, min_val=-np.inf, max_val=np.inf):
    super().__init__(value, lambda x, n: np.random.uniform(x-delta, x+delta, n),
                     min_val, max_val)

class UniformIntGene(Gene):
  def __init__(self, value, delta=1, min_val=-np.inf, max_val=np.inf):
    super().__init__(value, lambda x, n: np.random.randint(x-delta, x+delta, n),
                     min_val, max_val)