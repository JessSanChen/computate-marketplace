from marketplace import Simulation


if __name__ == '__main__':
    # num_agents, duration_mean, duration_std, price_std, algo
    sim = Simulation(10, 4, 1, 0.5, "WEIGHTED")