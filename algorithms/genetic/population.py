from multiprocessing.pool import ThreadPool as Pool
import numpy as np
import itertools

class Population():
    def __init__(self, elements, element_fitness, n_survivors, n_offsprings, random_choice=False):
        # Get the elements
        self.elements = list(elements)
        self.element_fitness = lambda elem: (elem, element_fitness(elem))
        self.model_type = list(set([type(elem) for elem in self.elements]))[0]

        # Parameters
        self.n_survivors = n_survivors
        self.n_offsprings = n_offsprings
        self.random_choice = random_choice

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
        if self.random_choice:
            elements_fitness = self.fitness().values()
            probability_distribution = self.softmax(elements_fitness)
            return np.random.choice(self.elements, size = self.n_survivors, p = probability_distribution), min(elements_fitness)
        else:
            selected = self.best_models()[:self.n_survivors]
            return selected, self.element_fitness(selected[0])[1]

    # Randomly mix two parents to give N offsprings
    def crossover(self, parent1, parent2):
        for _ in range(self.n_offsprings):
            which_one = np.random.randint(2, size=len(parent1.genes)).astype(np.bool)
            genome = np.choose(which_one, [parent1.sample(), parent2.sample()])
            yield self.model_type(*genome)

    # Match randomly two element
    def random_match(self, selected):
        combinations = list(itertools.combinations(selected, 2))
        np.random.shuffle(combinations)
        return combinations[:len(selected)//2]

    # a single generation step
    def step(self):
        # Implement the evolution of the population
        survivors, best_fitness = self.selection()
        population = sum([list(self.crossover(parent1, parent2))
                            for parent1, parent2 in self.random_match(survivors)], [])
        self.elements = population
        return best_fitness
