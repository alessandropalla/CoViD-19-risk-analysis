import numpy as np
import yaml


class GeneticModel():
    def __init__(self, model, genes):
        self.genes = genes
        self.model = model

    def set_y0(self, y0):
        self.y0 = [y.item() if isinstance(y, np.ndarray) else y for y in y0]

    def simulate(self, t):
        return self.model.integrate(t, self.y0)

    def fitness(self, data, valid=None):
        t = np.linspace(0, len(data), len(data))
        result = self.simulate(t)
        return sum([
            1 / (np.linalg.norm(np.log(data) - np.log(res))) for idx, res in enumerate(result) if valid and valid[idx]
        ])

    # Generate N childs from this parent
    def sample(self):
        return [gene.sample() for gene in self.genes]

    def dump(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.dumps(), fp, yaml.SafeDumper)

    def dumps(self):
        return dict(gene.dump() for gene in self.genes)
