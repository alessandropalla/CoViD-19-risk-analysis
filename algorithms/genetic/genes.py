import numpy as np


class __Gene():
    def __init__(self, name, value, distribution, **params):
        # Gene name
        self.name = name
        # Values that can mutate througth generations
        self.value = value
        # Values that do not mutate througth generations
        self.params = params
        # When mutate, sample from a probability distribution
        self.distribution = distribution

    def sample(self, n=1):
        min_val = self.params["min_val"] if "min_val" in self.params.keys() else -np.inf
        max_val = self.params["max_val"] if "max_val" in self.params.keys() else np.inf
        return type(self)(self.name, np.clip(self.distribution(self.value, n), min_val, max_val).item(), **self.params)

    def dump(self):
        return (self.name, {
            "gene_type": type(self).__name__,
            "intitialization": {
                "type": "int",
                "value": float(self.value)
            },
            **self.params
        })


class NormalGene(__Gene):
    def __init__(self, name, value, **params):
        sigma = params["sigma"] if "sigma" in params.keys() else 0.1
        super().__init__(name, value, lambda x, n: np.random.normal(x, sigma, n), **params)


class PoissonGene(__Gene):
    def __init__(self, name, value, **params):
        sigma = params["sigma"] if "sigma" in params.keys() else 0.1
        super().__init__(name, value, np.random.poisson, **params)


class UniformGene(__Gene):
    def __init__(self, name, value, **params):
        delta = params["delta"] if "delta" in params.keys() else 1
        super().__init__(name, value, lambda x, n: np.random.uniform(x - delta, x + delta, n), **params)


class UniformIntGene(__Gene):
    def __init__(self, name, value, **params):
        delta = params["delta"] if "delta" in params.keys() else 1
        super().__init__(name, value, lambda x, n: np.random.randint(x - delta, x + delta, n), **params)


class ConstGene(__Gene):
    def __init__(self, name, value, **params):
        super().__init__(name, value, lambda x, n: x * np.ones((n, 1)), **params)


# Map string to gene class
gene_map = {
    "NormalGene": NormalGene,
    "PoissonGene": PoissonGene,
    "UniformGene": UniformGene,
    "UniformIntGene": UniformIntGene,
    "ConstGene": ConstGene,
}


# Generate genes from parameters
def generate_gene(name, gene_type, intitialization, **params):
    value = intitialization["value"]
    if "type" in intitialization and intitialization["type"].lower() == "random":
        value = np.random.uniform(value[0], value[1])
    return gene_map[gene_type](name, value, **params)
