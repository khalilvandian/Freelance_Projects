import numpy as np
from math import ceil


class Model:

    def __init__(self, cell_count = 3, machine_count = 4, worker_count = 3, part_count = 4,
                 operation_count = 2, period_count = 2):

        self.cells = [i+1 for i in range(cell_count)]
        self.machines = [i+1 for i in range(machine_count)]
        self.workers = [i+1 for i in range(worker_count)]
        self.parts = [i+1 for i in range(part_count)]
        self.operations = [i+1 for i in range(operation_count)]
        self.periods = [i+1 for i in range(period_count)]
        self.solution_shape = [len(self.periods), 3, len(self.parts), len(self.operations)]
        self.reshape_param = len(self.periods) * 3 * len(self.parts) * len(self.operations)
        self.ModelParameters = {
            'BU': 10000,
            'BL': 1,
            # Production cost of operation k of part type p.
            'mukp': np.random.uniform(1, 10, (len(self.operations), len(self.parts))),
            # Subcontracting cost of operations k of part type p.
            'Okp': np.random.uniform(1, 20, (len(self.operations), len(self.parts))),

            # Demand for part type p at time period t.
            'Dpt': np.random.randint(100, 1000, (len(self.parts), len(self.periods))),

            # Time required to perform operation k of part type p on machine type m with
            # worker type w.
            'Tkpmw': np.random.uniform(0, 1, (len(self.operations), len(self.parts), len(self.machines), len(self.workers))),

            # Capacity of each worker type w in hours.
            'Tw': np.random.randint(1, 100, len(self.workers)),

            # Intercellular material handling cost per part type p.
            'IEp': np.random.uniform(0.1, 2, len(self.parts)),

            # Capacity of each machine type m in hours.
            'Tm': np.random.randint(0, 1000, len(self.machines)),

            # Intracellular material handling cost per part type p.
            'IAp': np.random.uniform(0.1, 2, len(self.parts)),

            # number of alternative workers to process operation k of part
            # type p on the machine m in the cell c.
            # Sum_w_Xkpmwc = np.random.uniform(2, size=(2,))

            # Salary cost of worker type w.
            'Sw': np.random.uniform(100, 1000, len(self.workers)),

            # Amortised cost of machine type m per period.
            'alpha_m': np.random.uniform(1000, 2000, len(self.machines)),

            # Hiring cost of worker type w.
            'Hw': np.random.uniform(100, 500, (len(self.workers), len(self.periods))),

            # Operating cost per hour of machine type m.
            'beta_m': np.random.uniform(1, 20, len(self.machines)),

            # Firing cost of worker type w.
            'Fw': np.random.uniform(100, 500, (len(self.workers), len(self.periods))),

            # Relocation cost of machine type m including uninstalling, shifting, and
            # installing.
            'delta_m': np.random.uniform(100, 1000, len(self.machines))
        }

    def generate_population(self, population_number):

        population = []
        for i in range(population_number):
            periodic_sols = []
            for t in range(len(self.periods)):
                temp = [np.random.randint(1, len(self.machines) + 1, (len(self.parts), len(self.operations))),
                        np.random.randint(0, len(self.workers) + 1, (len(self.parts), len(self.operations))),
                        np.random.randint(1, len(self.cells) + 1, (len(self.parts), len(self.operations)))]
                periodic_sols.append(temp)
            population.append(self.Emendation_operation(np.array(periodic_sols)))

        return np.array(population)

    def calculate_cost(self, solution):
        Z = 0

        # Z1 The constant cost of all machines required in manufacturing cells over the planning
        # span. This cost is obtained by the product of the number of machine type m allocated
        # to cell c in period t and their associated costs.
        z1 = 0
        for m in self.machines:
            for t in self.periods:
                for c in self.cells:
                    z1 += self.Amct(m, c, t, solution) * self.alpha_m(m)

        # Z2 The salary paid to workers assigned to manufacturing cells over the planning span. It
        # is the product of the number of worker type w allocated to cell c during period t and
        # their associated costs.
        z2 = 0
        for t in self.periods:
            for w in self.workers:
                for c in self.cells:
                    z2 += self.Awct(w, c, t, solution) * self.Sw(w)

        # Z3 Machine operating cost; the cost of operating machines for part production. This cost
        # depends on the cost of operating each machine type per hour and the number of
        # hours required for each machine type.
        z3 = 0
        for t in self.periods:
            for p in self.parts:
                for k in self.operations:
                    for m in self.machines:
                        for w in self.workers:
                            for c in self.cells:
                                z3 += self.XPkpmwct(k, p, m, w, c, t, solution) * self.Tkpmw(k, p, m, w) * self.beta_mF(m)

        # Z4 The production cost of part operation; the labour cost incurred for part production. It
        # is the summation of the product of the number of part operations allocated to each
        # machine type and the labour cost.
        z4 = 0
        for t in self.periods:
            for p in self.parts:
                for k in self.operations:
                    for m in self.machines:
                        for w in self.workers:
                            for c in self.cells:
                                z4 += self.XPkpmwct(k, p, m, w, c, t, solution) * self.mukp(k, p)

        z5 = 0
        for t in self.periods:
            for p in self.parts:
                for k in self.operations:
                    z5 += self.OPkpt(k,p,t,solution) * self.ModelParameters['Okp'][k-1][p-1]


        z6 = 0
        for t in self.periods:
            for p in self.parts:
                for m in self.machines:
                    for w in self.workers:
                        for c in self.cells:
                            for k in self.operations[:-1]:
                                z6 += self.ModelParameters['IEp'][p-1] * self.XPkpmwct(k,p,m,w,c,t,solution) * \
                                      (1 - self.Xkpmwct(k+1,p,m,w,c,t,solution) * self.Xkpmwct(k,p,m,w,c,t,solution))


        z7 = 0
        for t in self.periods:
            for p in self.parts:
                for m in self.machines:
                    for w in self.workers:
                        for c in self.cells:
                            for k in self.operations[:-1]:
                                z7 += self.ModelParameters['IAp'][p-1] * self.XPkpmwct(k,p,m,w,c,t,solution) * \
                                          (self.Xkpmwct(k+1,p,m,w,c,t,solution) * self.Xkpmwct(k,p,m,w,c,t,solution))

        z8 = 0
        for t in self.periods:
            for m in self.machines:
                for c in self.cells:
                    z8 += (self.NmctPlus(m,c,t,solution) + self.NmctNegative(m,c,t,solution)) * self.ModelParameters['delta_m'][m-1]
        z8 = z8/2

        z9 = 0
        for t in self.periods:
            for w in self.workers:
                for c in self.cells:
                    z9 += self.LwctPlus(w,c,t,solution)*self.ModelParameters['Hw'][w-1][t-1]

        z10 = 0
        for t in self.periods:
            for w in self.workers:
                for c in self.cells:
                    z10 += self.LwctNegative(w,c,t,solution)*self.ModelParameters['Fw'][w-1][t-1]

        z = z1 + z2 + z3 + z4 + z5 + z6 + z7 + z8 + z9 + z10

        return z

    def crossover_func(self, parents, offspring_size, ga_instance):
        parents = parents.astype(int)
        parents = np.reshape(parents, (parents.shape[0], self.solution_shape[0], self.solution_shape[1],
                                       self.solution_shape[2], self.solution_shape[3]))
        offsprings = []
        for i in range(offspring_size[0]):
            p1 = np.random.randint(parents.shape[0])
            p2 = np.random.randint(parents.shape[0])
            res = self.crossover_parents(parents[p1], parents[p2])
            offsprings.append(res)
        offsprings = np.array(offsprings)
        return np.reshape(offsprings, (offsprings.shape[0], self.reshape_param))

    def crossover_parents(self, parent1, parent2):
        crossover_row = np.random.randint(len(self.parts))
        res = parent1.copy()
        temp_2 = parent2.copy()
        res[:, :, crossover_row + 1:, :] = temp_2[:, :, crossover_row + 1:, :]
        res = self.Emendation_operation(res)
        return res

    def fitness_func(self, ga_instance, solution, solution_idx):

        solution = solution.astype(int)
        temp = np.reshape(solution, (self.solution_shape[0], self.solution_shape[1], self.solution_shape[2], self.solution_shape[3]))

        try:
            cost = -self.calculate_cost(temp)
        except:
            print(solution,solution_idx)
            raise
        return cost

    def mutation_func(self, offspring, ga_instance):
        offspring = offspring.astype(int)
        offspring_copy = np.reshape(offspring, (offspring.shape[0], self.solution_shape[0], self.solution_shape[1],
                                                self.solution_shape[2], self.solution_shape[3]))
        mutated_offspring = []
        pop = offspring_copy.copy()

        for i in range(pop.shape[0]):
            temp = pop[i].copy()
            temp_copy = pop[i].copy()
            rows = np.random.choice(range(len(self.parts)-1), 2, replace=False)
            random_matrice =  np.random.randint(3)
            random_period = np.random.randint(len(self.periods))
            temp[random_period, random_matrice, rows[0], :] = temp_copy[random_period, random_matrice, rows[1], :]
            temp[random_period, random_matrice, rows[1], :] = temp_copy[random_period, random_matrice, rows[0], :]
            try:
                temp = self.Emendation_operation(temp)
                mutated_offspring.append(temp)
            except:
                raise

        mutated_offspring = np.array(mutated_offspring)

        return np.reshape(mutated_offspring, (offspring.shape[0], self.reshape_param))

    def Emendation_operation(self, solution):

        is_correct, constrains = self.constraint_check(solution)
        counter = 0

        while not is_correct:
            # Equation 2 fix
            if not constrains[0]:
                solution = self.Emendation_operation_2(solution)

            # Equation 3 fix
            if not constrains[1]:
                solution = self.Emendation_operation_3(solution)

            # Equation 4 fix
            if not constrains[2]:
                solution = self.Emendation_operation_4(solution)

            # Equation 5 fix
            if not constrains[3]:
                solution = self.Emendation_operation_5(solution)

            # Equation 6 fix
            if not constrains[4]:
                solution = self.Emendation_operation_6(solution)

            # Equation 7 fix
            if not constrains[5]:
                solution = self.Emendation_operation_7(solution)

            # Equation 8 fix
            if not constrains[6]:
                solution = self.Emendation_operation_8(solution)

            # Equation 9 fix
            if not constrains[7]:
                solution = self.Emendation_operation_9(solution)

            is_correct, constrains = self.constraint_check(solution)
            counter += 1
            if counter > 5:
                print('----------------------------------------------------')
                print(solution)
                machines_in_cell = 0
                for t in self.periods:
                    for c in self.cells:
                        for m in self.machines:
                            machines_in_cell += self.Amct(m, c, t, solution)
                        if (machines_in_cell > self.ModelParameters['BU']) or (
                                machines_in_cell < self.ModelParameters['BL']):
                            print("machines in cell: ", machines_in_cell)
                            print(" ,t: ", t, " ,c: ", c)
                        machines_in_cell = 0
                print('----------------------------------------------------')
                raise

        return solution

    def Emendation_operation_2(self, solution):
        return solution

    def Emendation_operation_3(self, solution):
        return solution

    def Emendation_operation_4(self, solution):
        return solution

    def Emendation_operation_5(self, solution):
        return solution

    def Emendation_operation_6(self, solution):
        return solution

    def Emendation_operation_7(self, solution):
        return solution

    def Emendation_operation_8(self, solution):

        machines_in_cell = 0
        for t in self.periods:
            for c in self.cells:
                # first count the machines in cell c
                for m in self.machines:
                    machines_in_cell += self.Amct(m, c, t, solution)
                if machines_in_cell < self.ModelParameters['BL']:
                    # check if a cell is empty, if it is, randomly assign an operation to it
                    pks = self.PKct(c, t - 1, solution)
                    if not pks:
                        p_rand = np.random.randint(1, len(self.parts) + 1)
                        k_rand = np.random.randint(1, len(self.operations) + 1)
                        solution = self.set_solution_value(t,3,p_rand,k_rand, c, solution)
                    elif machines_in_cell == 0:
                        new_w = np.random.randint(1,len(self.workers)+1)
                        pk_to_change = pks[np.random.randint(len(pks))]
                        if self.get_solution(t,2,pk_to_change[0]+1, pk_to_change[1]+1, solution) == 0:
                            solution = self.set_solution_value(t,2,pk_to_change[0]+1,pk_to_change[1]+1,new_w,solution)
                # elif machines_in_cell > self.ModelParameters['BU']:
                #
                # else:

                machines_in_cell = 0
        return solution

    def Emendation_operation_9(self, solution):
        return solution

    def constraint_check(self, solution):

        # equation 2: seems correct, every k and p are assigned a worker, cell and machine whilst population generation.
        # crossover and mutation only relocate the values.
        eq2 = True

        # equation 3:
        # checks that the production does not exceed demand, or that it is lower than demand.
        sum_eq = 0
        eq3 = True
        for t in self.periods:
            for p in self.parts:
                for k in self.operations:
                    for m in self.machines:
                        for w in self.workers:
                            for c in self.cells:
                                sum_eq += self.XPkpmwct(k,p,m,w,c,t,solution)


                    if sum_eq + self.OPkpt(k,p,t,solution) != self.DptF(p,t):
                        eq3 = False
                    sum_eq = 0

        # equation 4, machine working capacity check
        sum_eq4 = 0
        eq4 = True
        for t in self.periods:
            for c in self.cells:
                for m in self.machines:
                    for p in self.parts:
                        for w in self.workers:
                            for k in self.operations:
                                sum_eq += self.Tkpmw(k, p, m, w) * self.XPkpmwct(k, p, m, w, c, t, solution)
                    if sum_eq4 > self.ModelParameters['Tm'][m - 1] * self.Amct(m, c, t, solution):
                        eq4 = False
                    sum_eq4 = 0

        # equation 5: worker capacity check
        sum_eq5 = 0
        eq5 = True
        for t in self.periods:
            for c in self.cells:
                for w in self.workers:
                    for m in self.machines:
                        for p in self.parts:
                            for k in self.operations:
                                sum_eq5 += self.Tkpmw(k, p, m, w) * self.XPkpmwct(k, p, m, w, c, t, solution)
                    if sum_eq5 > self.ModelParameters['Tw'][w-1] * self.Awct(w,c,t,solution):
                        eq5 = False
                    sum_eq5 = 0

        # equation 6: Production Flow check
        eq6 = True
        XPkpmwct = 0
        XPk1pmwct = 0
        for t in self.periods:
            for p in self.parts:
                for k in self.operations[:-1]:
                    for m in self.machines:
                        for w in self.workers:
                            for c in self.cells:
                                XPk1pmwct += self.XPkpmwct(k + 1, p, m, w, c, t, solution)
                                XPkpmwct += self.XPkpmwct(k, p, m, w, c, t, solution)
                    if XPkpmwct + self.OPkpt(k,p,t,solution) != self.OPkpt(k + 1, p, t, solution) + XPk1pmwct:
                        eq6 = False
                    XPk1pmwct = 0
                    XPkpmwct = 0

        # equation 7: machine count stability
        eq7 = True
        for t in self.periods:
            for m in self.machines:
                for c in self.cells:
                    if self.Amct(m, c, t - 1,solution) + self.NmctPlus(m, c, t,solution) - \
                            self.NmctNegative(m, c, t,solution) != self.Amct(m,c,t,solution):
                        eq7 = False

        # equation 8: cell size check with machine count
        eq8 = True
        machines_in_cell = 0
        for t in self.periods:
            for c in self.cells:
                for m in self.machines:
                    machines_in_cell += self.Amct(m, c, t,solution)
                if (machines_in_cell > self.ModelParameters['BU']) or (machines_in_cell < self.ModelParameters['BL']):
                    eq8 = False
                machines_in_cell = 0

        # equation 9: worker count stability
        eq9 = True
        for t in self.periods:
            for w in self.workers:
                for c in self.cells:
                    if self.Awct(w,c,t - 1,solution) + self.LwctPlus(w, c, t, solution) - \
                            self.LwctNegative(w, c, t,solution) != self.Awct(w, c, t, solution):
                        eq9 = False

        final_res = eq2 and eq3 and eq4 and eq5 and eq6 and eq7 and eq8 and eq9

        return final_res, [eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]

    def set_solution_value(self, t, matrice, p, k, value, solution):
        solution[t-1][matrice-1][p-1][k-1] = int(value)
        return solution

    # Parameter Calculation Methods that are used in the class and algorithm
    def Amct(self, m, c, t, solution):
        # to calculate this parameter, we will look up ops and parts that are held in cell c, then
        # we will check which machines are for found parts and ops. Then we will use the machine capacity in hours
        # to calculate the number of machines of type m in cell c at period t

        if t < 1:
            return 0

        # parts and operations held in cell c
        pks = self.PKct(c, t-1, solution)

        machine_count = 0
        hours = 0
        # in the parts and ops, how many are done by the machine m
        for i in pks:
            if solution[t-1, 0, i[0], i[1]] == m:
                # I must calculate the hours of work needed to produce the demanded parts
                # XPkpmwct: number of part operations that must be done
                # Tkpmw: the time needed for operation k part p to be produced with machine m and worker w
                w = solution[t-1, 1, i[0], i[1]]
                try:
                    hours += self.XPkpmwct(i[1]+1,i[0]+1,m,w,c,t,solution) * self.Tkpmw(i[1]+1,i[0]+1,m,w)
                except:
                    raise
        # Hours needed is calculated, now it must be divided to machine capacity (Tm) and rounded up
        machine_count = ceil(hours / self.ModelParameters['Tm'][m-1])

        # The result is the number of machines needed to produce the demanded parts in one period,

        return machine_count

    def Awct(self, w, c, t, solution):
        # to calculate this parameter, we will look up ops and parts that are held in cell c, then
        # we will check which workers are for found parts and ops. Then we will use the worker capacity in hours
        # to calculate the number of workers of type w in cell c at period t

        if t < 1:
            return 0

        # parts and operations held in cell c
        pks = self.PKct(c, t - 1, solution)

        worker_count = 0
        hours = 0
        # in the parts and ops, how many are done by the machine m
        for i in pks:
            if solution[t - 1, 1, i[0], i[1]] == w:
                # I must calculate the hours of work needed to produce the demanded parts
                # XPkpmwct: number of part operations that must be done
                # Tkpmw: the time needed for operation k part p to be produced with machine m and worker w
                m = solution[t - 1, 0, i[0], i[1]]
                hours += self.XPkpmwct(i[1] + 1, i[0] + 1, m, w, c, t, solution) * self.Tkpmw(i[1] + 1, i[0] + 1, m, w)
        # Hours needed is calculated, now it must be divided to machine capacity (Tm) and rounded up
        worker_count = ceil(hours / self.ModelParameters['Tw'][w - 1])

        # The result is the number of machines needed to produce the demanded parts in one period,

        return worker_count

    # Function to find the parts and operations held in cell c. Existing operations for production of parts in cell c
    @staticmethod
    def PKct(c, t, solution):

        # parts and operations held in cell c
        pks = []
        for j in range(solution[t, 2].shape[0]):
            for k in range(solution[t, 2].shape[1]):
                if solution[t, 2, j, k] == c:
                    pks.append([j, k])
        return pks

    # XPkpmwc(t) Number of parts of type p processed for operation k on machine m with
    # worker type w in cell c in period t.

    def alpha_m(self, m):
        return self.ModelParameters['alpha_m'][m - 1]

    def Sw(self, w):
        return self.ModelParameters['Sw'][w - 1]

    def DptF(self,p,t):
        return self.ModelParameters['Dpt'][p-1][t-1]

    @staticmethod
    def get_solution(t, matrice, p, k, solution):
        return solution[t - 1, matrice - 1, p - 1, k - 1]

    def Tkpmw (self, k, p, m, w):
        if w < 1:
            return 0
        else:
            return self.ModelParameters['Tkpmw'][k - 1, p - 1, m - 1, w - 1]

    def beta_mF(self, m):
        return self.ModelParameters['beta_m'][m - 1]

    def mukp(self,k, p):
        return self.ModelParameters['mukp'][k - 1, p - 1]

    #   Methods for calculating Decision variables
    def XPkpmwct(self, k, p, m, w, c, t, solution):

        # if the part is produced internally it must be Dpt else it is zero
        count = 0
        if self.Xkpmwct(k, p, m, w, c, t, solution):
            count = self.DptF(p, t)

        return count

    def Xkpmwct(self, k, p, m, w, c, t, solution):

        res = 0
        if (self.get_solution(t, 1, p, k, solution) == m) & (self.get_solution(t, 2, p, k, solution) == w) & \
                (self.get_solution(t, 3, p, k, solution) == c):
            res = 1
        return res

    def NmctPlus(self, m, c, t, solution):
        # using the number of machines in cell c during period t and t-1, the change will be calculated

        if t > 1:
            Mct1 = self.Amct(m,c,t-1,solution)
        else:
            Mct1 = 0

        Mct2 = self.Amct(m,c,t,solution)

        if (Mct2 - Mct1) > 0:
            return Mct2 - Mct1
        else:
            return 0

    def NmctNegative(self, m, c, t, solution):
        # using the number of machines in cell c during period t and t-1, the change will be calculated

        if t > 1:
            Mct1 = self.Amct(m, c, t - 1, solution)
        else:
            Mct1 = 0

        Mct2 = self.Amct(m, c, t, solution)

        if (Mct2 - Mct1) < 0:
            return -(Mct2 - Mct1)
        else:
            return 0

    def LwctPlus(self,w,c,t,solution):
        # using the number of workers in cell c during period t and t-1, the change will be calculated

        if t > 1:
            Wct1 = self.Awct(w, c, t - 1, solution)
        else:
            Wct1 = 0

        Wct2 = self.Awct(w, c, t, solution)

        if (Wct2 - Wct1) > 0:
            return Wct2 - Wct1
        else:
            return 0

    def LwctNegative(self,w,c,t,solution):
        # using the number of workers in cell c during period t and t-1, the change will be calculated

        if t > 1:
            Wct1 = self.Awct(w, c, t - 1, solution)
        else:
            Wct1 = 0

        Wct2 = self.Awct(w, c, t, solution)

        if (Wct2 - Wct1) < 0:
            return -(Wct2 - Wct1)
        else:
            return 0

    def OPkpt(self, k, p, t, solution):
        # the k,p,t which is subcontracted will be in the amount of Dpt

        number = 0
        if self.is_subcontracted_kpt(k,p,t,solution):
            number = self.DptF(p,t)

        # this function is to extract the number of part operations that are subcontracted
        return number

    def Akpmt(self, k, p, m, t, solution):
        res = 0
        if self.get_solution(t,1,p,k,solution) == m:
            res = 1
        return res

    def is_subcontracted_kpt(self,k,p,t,solution):
        m = self.get_solution(t,1,p,k, solution)
        w = self.get_solution(t,2,p,k, solution)
        c = self.get_solution(t,3,p,k, solution)

        if m == 0 or w == 0 or c == 0:
            return True
        else:
            return False

