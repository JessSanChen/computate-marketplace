from marketplace import Marketplace


if __name__ == '__main__':
    # num_agents, duration_mean, duration_std, price_std, report_algo, true_algo, epsilon
    # report_algo: UTILITY, WEIGHTED_RANK
    # true_algo: BASELINE, STOCH, GROUPED
    # epsilon is grouped_epsilon if grouped, std if stochastic
    market = Marketplace(15, 4, 1, 0.5, "WEIGHTED_RANK", "BASELINE")
    print(market.stable)