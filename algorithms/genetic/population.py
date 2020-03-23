from multiprocessing.pool import ThreadPool as Pool
from algorithms.genetic.genes import generate_gene
import numpy as np
import itertools
import yaml


class Population():
    def __init__(self, model_type, element_fitness, filename):

        # Save fitness function and the model type
        self.element_fitness = lambda elem: (elem, element_fitness(elem))
        self.model_type = model_type

        # Load configuration from file
        with open(filename, "r") as fp:
            self.load_configuration(yaml.load(fp, yaml.SafeLoader))

        # Get the elements
        self.initialize_population()

    def load_configuration(self, configs):
        # Number of generations
        self.generations = configs["training"]["generations"]
        # Number of survivors in each generations
        self.survivors = configs["training"]["survivors"]
        # Number of offsprings for each couple
        self.offsprings = configs["training"]["offsprings"]
        # Selection methods
        self.selection_methods = configs["training"]["selection_methods"]
        # Preserve parents
        self.preserve_parents = configs["training"]["preserve_parents"]

        # Load genes configurations
        with open(configs["genes"]["filename"], "r") as fp:
            self.genes = yaml.load(fp, yaml.SafeLoader)

    def initialize_population(self):
        # number of elements in each generation
        total_elements = self.survivors * self.offsprings // 2
        self.elements = [self.generate_element() for _ in range(total_elements)]

    def generate_element(self):
        # Generate elements
        return self.model_type(**{name: generate_gene(name, **params) for name, params in self.genes.items()})

    # Element fitness
    def fitness(self):
        with Pool(processes=4) as pool:
            return dict(pool.map(self.element_fitness, self.elements))

    # Return the models sorted by their fitness
    def best_models(self):
        return [elem for elem, fitness in sorted(self.fitness().items(), key=lambda item: item[1], reverse=True)]

    def softmax(self, x):
        score = np.exp(np.asarray(list(x)))
        return (score / score.sum(0)).tolist()

    # Select individuals from a population
    def selection(self):
        if self.selection_methods.lower() == "stochastic":
            elements_fitness = self.fitness().values()
            probability_distribution = self.softmax(elements_fitness)
            return np.random.choice(self.elements, size=self.survivors,
                                    p=probability_distribution), min(elements_fitness)
        else:
            selected = self.best_models()[:self.survivors]
            return selected, self.element_fitness(selected[0])[1]

    # Randomly mix two parents to give N offsprings
    def crossover(self, parent1, parent2):
        for _ in range(self.offsprings):
            which_one = np.random.randint(2, size=len(parent1.genes)).astype(np.bool)
            genome = np.choose(which_one, [parent1.sample(), parent2.sample()])
            yield self.model_type(**{gene.name: gene for gene in genome})
        if self.preserve_parents:
            yield parent1
            yield parent2

    # Match randomly two element
    def random_match(self, selected):
        combinations = list(itertools.combinations(selected, 2))
        np.random.shuffle(combinations)
        return combinations[:len(selected) // 2]

    # a single generation step
    def step(self):
        # Implement the evolution of the population
        survivors, best_fitness = self.selection()
        population = sum([list(self.crossover(parent1, parent2)) for parent1, parent2 in self.random_match(survivors)],
                         [])
        self.elements = population
        return best_fitness, population

    def train(self):
        for idx in range(self.generations):
            yield idx, self.step()
