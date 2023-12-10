from marketplace import Marketplace
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


if __name__ == '__main__':
    # num_agents, duration_mean, duration_std, price_std, report_algo, true_algo, epsilon
    # report_algo: UTILITY, WEIGHTED_RANK
    # true_algo: BASELINE, STOCHASTIC, GROUPED
    # epsilon is grouped_epsilon if grouped, std if stochastic
    # if using BASELINE, epsilon is not used
    # if GROUPED, epsilon must be > 0

    NUM_AGENTS = 20
    NUM_ROUNDS = 50
    DURATION_MEAN = 6
    DURATION_STD = 2
    PRICE_STD = 1

    # stability rate vs. epsilon
    stability_rates = []
    avg_revenues = [] # total system revenue per round
    epsilons = np.arange(0.005, 0.5, 0.005)
    for epsilon in epsilons:
        stable_count = 0
        total_revenue = 0
        for round in range(NUM_ROUNDS):
            market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "WEIGHTED_RANK", "GROUPED", epsilon)
            total_revenue = sum([lender.price for lender in market.lenders])
            if market.is_stable():
                stable_count += 1
        print(f"Stability rate for epsilon = {epsilon}: {stable_count / NUM_ROUNDS}")
        print(f"Avg revenue for epsilon = {epsilon}: {total_revenue / NUM_ROUNDS}")
        stability_rates.append(stable_count / NUM_ROUNDS)
        avg_revenues.append(total_revenue / NUM_ROUNDS)

    # LOWESS (Locally Weighted Scatterplot Smoothing)
    lowess = sm.nonparametric.lowess(stability_rates, epsilons, frac=0.3)

    # Scatter plot
    plt.scatter(epsilons, stability_rates, color='blue', label='Data Points')

    # Trendline
    plt.plot(lowess[:, 0], lowess[:, 1], color='red', label='LOWESS Trendline')


    plt.plot(epsilons, stability_rates, marker='o')
    plt.xlabel('Epsilon (Group Size)')
    plt.ylabel('Stability Rate')
    plt.title('Grouped Indifference: Stability Rate vs Epsilon in Marketplace Simulations')
    plt.grid(True)
    plt.show()

    # # stability rate vs. std 
    # stability_rates = []
    # stds = np.arange(0, 0.1, 0.001)
    # for std in stds:
    #     stable_count = 0
    #     for round in range(NUM_ROUNDS):
    #         market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "WEIGHTED_RANK", "STOCHASTIC", std)
    #         if market.is_stable():
    #             stable_count += 1
    #     print(f"Stability rate for std = {std}: {stable_count / NUM_ROUNDS}")
    #     stability_rates.append(stable_count / NUM_ROUNDS)

    # # LOWESS (Locally Weighted Scatterplot Smoothing)
    # lowess = sm.nonparametric.lowess(stability_rates, stds, frac=0.3)

    # # Scatter plot
    # plt.scatter(stds, stability_rates, color='blue', label='Data Points')

    # # Trendline
    # plt.plot(lowess[:, 0], lowess[:, 1], color='red', label='LOWESS Trendline')

    # plt.plot(stds, stability_rates, marker='o')
    # plt.xlabel('Standard Dev of True from Reported Preference Weight')
    # plt.ylabel('Stability Rate')
    # plt.title('Stochastic Indifference: Stability Rate vs Std in Marketplace Simulations')
    # plt.grid(True)
    # plt.show()

    
    
