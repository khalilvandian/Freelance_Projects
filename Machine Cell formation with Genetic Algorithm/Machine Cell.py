from Model import Model
import numpy as np
import pygad
from matplotlib import pyplot as plt

mod = Model(cell_count=4, machine_count=5,worker_count=4,part_count=5)

ga_model = pygad.GA(num_generations=30,
                       num_parents_mating=10,
                       fitness_func=mod.fitness_func,
                       initial_population=np.reshape(mod.generate_population(80), (80,mod.reshape_param)),
                       crossover_type=mod.crossover_func,
                       mutation_type=mod.mutation_func,
                       gene_type=int,
                       mutation_probability=0.1)

ga_model.run()

solution, solution_fitness, solution_idx = ga_model.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

ga_model.plot_fitness()

# prediction = np.sum(np.array(function_inputs)*solution)
# print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
