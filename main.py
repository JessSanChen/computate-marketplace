from marketplace import Marketplace


if __name__ == '__main__':
    # num_agents, duration_mean, duration_std, price_std, report_algo, true_algo, epsilon
    # report_algo: UTILITY, WEIGHTED_RANK
    # true_algo: BASELINE, STOCHASTIC, GROUPED
    # epsilon is grouped_epsilon if grouped, std if stochastic
    # if using BASELINE, epsilon is not used
    # if GROUPED, epsilon must be > 0
    market = Marketplace(15, 4, 1, 0.5, "WEIGHTED_RANK", "GROUPED", 0.05)
    print(market.stable)