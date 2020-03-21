import numpy as np

class GeneticModel():
    def __init__(self, model, genes):
        self.genes = genes
        self.model = model

    def set_y0(self, y0):
        self.y0 = y0

    def simulate(self, t):
        return self.model.integrate(t, self.y0)

    def fitness(self, data, valid = None):
        t = np.linspace(0, len(data), len(data))
        result = self.simulate(t)
        return sum([1/(np.linalg.norm(data - res)) 
               for idx, res in enumerate(result)
               if valid and valid[idx]])

    # Generate N childs from this parent
    def sample(self):
        return [gene.sample() for gene in self.genes]
