import random

class AntColony:
    def __init__(self, distances, n_ants, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 1.0 will lead to no decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        """
        self.distances  = distances
        self.pheromone = 1 / (len(distances) * 0.5 * distances.mean())
        self.all_inds = range(len(distances))
        self.pheromone_levels = [[self.pheromone] * len(distances) for _ in range(len(distances))]
        self.all_inds = list(range(len(distances)))
        self.n_ants = n_ants
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self, num_iterations):
        """
        Args:
            num_iterations (int): number of iterations
        Returns:
            tuple: (best_path, all_paths, all_path_costs)
        """
        all_paths = []
        all_path_costs = []
        for i in range(num_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.pheromone_levels, self.distances)
            self.pheromone_levels = self.pheromone_levels * self.decay
        all_path_costs = [self.path_cost(path, self.distances) for path in all_paths]
        best_path_index = all_path_costs.index(min(all_path_costs))
        best_path = all_paths[best_path_index]
        return best_path, all_paths, all_path_costs

    def spread_pheronome(self, all_paths, pheromone_levels, distances):
        """
        Args:
            all_paths (list): list of lists, where each list has the order in which the nodes are visited
            pheromone_levels (2D list): matrix with pheromone levels on all paths
        """
        # for all ants, deposit pheromone on the path they have travelled
        for path in all_paths:
            pheromone_to_deposit = 1 / self.path_cost(path, distances)
            for move in path:
                pheromone_levels[move] = pheromone_levels[move] + pheromone_to_deposit

    def gen_path_dist(self, path, distances):
        """
        Args:
            path (list): list of node indices
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
        Returns:
            float: total distance of path
        """
        total_dist = 0
        for ele in path:
            total_dist += distances[ele][path[ele + 1]]
        return total_dist

    def gen_all_paths(self):
        """
        Returns:
            list: all possible paths
        """
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path_dist(list(range(len(self.distances))), self.distances)
            all_paths.append(path)
        return all_paths

    def path_cost(self, path, distances):
        """
        Args:
            path (list): list of node indices
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
        Returns:
            float: total distance of path
        """
        total_cost = 0
        for ele in path:
            total_cost += distances[ele][path[ele + 1]]
        return total_cost

# Example Usage
if __name__ == "__main__":
    # Example distance matrix (replace with your own)
    distances = [
        [0, 2, 3, 4],
        [2, 0, 5, 6],
        [3, 5, 0, 7],
        [4, 6, 7, 0]
    ]

    # Example parameters
    n_ants = 5
    decay = 0.95
    alpha = 1
    beta = 1

    ant_colony = AntColony(distances, n_ants, decay, alpha, beta)
    best_path, all_paths, all_path_costs = ant_colony.run(num_iterations=100)

    print("Best Path:", best_path)
    print("All Paths:", all_paths)
    print("All Path Costs:", all_path_costs)
