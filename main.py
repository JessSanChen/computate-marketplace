from marketplace import Marketplace


if __name__ == '__main__':
    # num_agents, duration_mean, duration_std, price_std, report_algo, true_algo
    market = Marketplace(15, 4, 1, 0.5, "WEIGHTED", "SAME")
    print(market.stable)