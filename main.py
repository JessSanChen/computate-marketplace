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

    # NUM_AGENTS = 20
    NUM_ROUNDS = 30
    DURATION_MEAN = 12
    DURATION_STD = 4
    PRICE_STD = 3

    """ UTILITY MATCHING ALGOS: AGG REVENUE VS NUM AGENTS """
    da_revenues = [] # total system revenue per round
    da_spreads = []
    # boston_revenues = []
    # rich_revenues = []
    num_agents_range = range(1,31)
    for num_agents in num_agents_range:
        total_da_revenue = 0
        total_da_spread = 0
        # total_boston_revenue = 0
        # total_rich_revenue = 0
        for round in range(NUM_ROUNDS):
            da_market = Marketplace(num_agents, DURATION_MEAN, DURATION_STD, PRICE_STD, "DA","UTILITY", "BASELINE",0)
            # boston_market = Marketplace(num_agents, DURATION_MEAN, DURATION_STD, PRICE_STD, "BOSTON","UTILITY", "BASELINE",0)
            # rich_market = Marketplace(num_agents, DURATION_MEAN, DURATION_STD, PRICE_STD, "RICH","UTILITY", "BASELINE",0)
            
            total_da_revenue += sum([lender.price for lender in da_market.lenders])
            # total_boston_revenue += sum([lender.price for lender in boston_market.lenders])
            # total_rich_revenue += sum([lender.price for lender in rich_market.lenders])

            total_da_spread += sum([da_market.lenders[i].price - da_market.lenders[i].match.price for i in range(num_agents)])
            # total_boston_revenue += sum([boston_market.lenders[i].price - boston_market.lenders[i].match.price for i in range(num_agents)])
            # total_rich_revenue += sum([rich_market.lenders[i].price - rich_market.lenders[i].match.price for i in range(num_agents)])
            
        print(f"Avg market revenue for num agents = {num_agents}: {total_da_revenue / NUM_ROUNDS}")

        da_revenues.append(total_da_revenue / NUM_ROUNDS)
        da_spreads.append(total_da_spread / NUM_ROUNDS)
        # boston_revenues.append(total_boston_revenue / NUM_ROUNDS)
        # rich_revenues.append(total_rich_revenue / NUM_ROUNDS)

    # Plotting
    plt.plot(num_agents_range, da_revenues, label='DA Market Agg Spread', color='blue')
    # plt.plot(num_agents_range, boston_revenues, label='Boston Market Agg Spread', color='green')
    # plt.plot(num_agents_range, rich_revenues, label='Richest-First Agg Spread', color='red')

    plt.xlabel('Number of Agents')
    plt.ylabel('Market Revenue')
    plt.title('DA Market Revenue vs. Num Agents')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.plot(num_agents_range, da_spreads, label='DA Market Agg Spread', color='blue')

    plt.xlabel('Number of Agents')
    plt.ylabel('Aggregate Spread')
    plt.title('DA Market Aggregate Spreads vs. Num Agents')
    plt.legend()
    plt.grid(True)
    plt.show()

    """ WEIGHTED RANK GROUPED: STABILITY RATE VS. GROUP EPSILON """
    # stability_rates = []
    # revenues = [] # total system revenue per round
    # price_spreads = [] # lender price - renter price
    # duration_spreads = []
    # epsilons = np.arange(0.005, 0.5, 0.005)
    # for epsilon in epsilons:
    #     stable_count = 0
    #     total_revenue = 0
    #     total_price_spread = 0
    #     total_duration_spread = 0
    #     for round in range(NUM_ROUNDS):
    #         market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "WEIGHTED_RANK", "GROUPED", epsilon)
    #         total_revenue += sum([lender.price for lender in market.lenders])
    #         total_price_spread += sum([market.lenders[i].price - market.lenders[i].match.price for i in range(NUM_AGENTS)])
    #         total_duration_spread += sum([market.lenders[i].duration - market.lenders[i].match.duration for i in range(NUM_AGENTS)])
    #         if market.is_stable():
    #             stable_count += 1
    #     print(f"Stability rate for epsilon = {epsilon}: {stable_count / NUM_ROUNDS}")
    #     print(f"Avg market revenue for epsilon = {epsilon}: {total_revenue / NUM_ROUNDS}")
    #     print(f"Agg price spread for epsilon = {epsilon}: {total_price_spread / NUM_ROUNDS}")
    #     print(f"Agg duration spread for epsilon = {epsilon}: {total_duration_spread / NUM_ROUNDS}")
        
    #     stability_rates.append(stable_count / NUM_ROUNDS)
    #     revenues.append(total_revenue / NUM_ROUNDS)
    #     price_spreads.append(total_price_spread / NUM_ROUNDS)
    #     duration_spreads.append(total_duration_spread / NUM_ROUNDS)

    # # LOWESS (Locally Weighted Scatterplot Smoothing)
    # lowess_stability = sm.nonparametric.lowess(stability_rates, epsilons, frac=0.3)

    # # Graph 1: Stability Rate
    # plt.figure()
    # plt.scatter(epsilons, stability_rates, color='blue', label='Stability Rate')
    # plt.plot(lowess_stability[:, 0], lowess_stability[:, 1], color='red', label='LOWESS Trendline (Stability)')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Stability Rate')
    # plt.title('Weighted Rank Grouped Indifference: Stability Rate vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    
    # # Graph 2: System Revenue and Aggregate Price Spread
    # plt.figure()
    # plt.plot(epsilons, revenues, color='green', label='Market Revenue')
    # plt.plot(epsilons, price_spreads, color='orange', label='Aggregate Price Spread')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Revenue / Price Spread')
    # plt.title('Weighted Rank Grouped Indifference: Market Revenue and Aggregate Price Spread vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # Graph 3: Aggregate Duration Spread
    # plt.figure()
    # plt.plot(epsilons, duration_spreads, color='green', label='Aggregate Duration Spread')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Duration Spread')
    # plt.title('Weighted Rank Grouped Indifference: Aggregate Duration Spread vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()


    """ WEIGHTED RANK STOCHASTIC: STABILITY RATE VS. STD """
    # stability_rates = []
    # revenues = [] # total system revenue per round
    # price_spreads = [] # lender price - renter price
    # duration_spreads = []
    # epsilons = np.arange(0, 0.1, 0.001)
    # for epsilon in epsilons:
    #     stable_count = 0
    #     total_revenue = 0
    #     total_price_spread = 0
    #     total_duration_spread = 0
    #     for round in range(NUM_ROUNDS):
    #         market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "WEIGHTED_RANK", "STOCHASTIC", epsilon)
    #         total_revenue += sum([lender.price for lender in market.lenders])
    #         total_price_spread += sum([market.lenders[i].price - market.lenders[i].match.price for i in range(NUM_AGENTS)])
    #         total_duration_spread += sum([market.lenders[i].duration - market.lenders[i].match.duration for i in range(NUM_AGENTS)])
    #         if market.is_stable():
    #             stable_count += 1
    #     print(f"Stability rate for epsilon = {epsilon}: {stable_count / NUM_ROUNDS}")
    #     print(f"Avg market revenue for epsilon = {epsilon}: {total_revenue / NUM_ROUNDS}")
    #     print(f"Agg price spread for epsilon = {epsilon}: {total_price_spread / NUM_ROUNDS}")
    #     print(f"Agg duration spread for epsilon = {epsilon}: {total_duration_spread / NUM_ROUNDS}")
        
    #     stability_rates.append(stable_count / NUM_ROUNDS)
    #     revenues.append(total_revenue / NUM_ROUNDS)
    #     price_spreads.append(total_price_spread / NUM_ROUNDS)
    #     duration_spreads.append(total_duration_spread / NUM_ROUNDS)

    # # LOWESS (Locally Weighted Scatterplot Smoothing)
    # lowess_stability = sm.nonparametric.lowess(stability_rates, epsilons, frac=0.3)

    # # Graph 1: Stability Rate
    # plt.figure()
    # plt.scatter(epsilons, stability_rates, color='blue', label='Stability Rate')
    # plt.plot(lowess_stability[:, 0], lowess_stability[:, 1], color='red', label='LOWESS Trendline (Stability)')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Stability Rate')
    # plt.title('Weighted Rank Stochastic Indifference: Stability Rate vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    
    # # Graph 2: System Revenue and Aggregate Price Spread
    # plt.figure()
    # plt.plot(epsilons, revenues, color='green', label='Market Revenue')
    # plt.plot(epsilons, price_spreads, color='orange', label='Aggregate Price Spread')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Revenue / Price Spread')
    # plt.title('Weighted Rank Stochastic Indifference: Market Revenue and Aggregate Price Spread vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # Graph 3: Aggregate Duration Spread
    # plt.figure()
    # plt.plot(epsilons, duration_spreads, color='green', label='Aggregate Duration Spread')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Duration Spread')
    # plt.title('Weighted Rank Stochastic Indifference: Aggregate Duration Spread vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()


    """ UTILITY GROUPED: STABILITY RATE VS. GROUP EPSILON """
    # stability_rates = []
    # revenues = [] # total system revenue per round
    # price_spreads = [] # lender price - renter price
    # duration_spreads = []
    # epsilons = np.arange(0.001, 0.1, 0.001)
    # for epsilon in epsilons:
    #     stable_count = 0
    #     total_revenue = 0
    #     total_price_spread = 0
    #     total_duration_spread = 0
    #     for round in range(NUM_ROUNDS):
    #         market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "UTILITY", "GROUPED", epsilon)
    #         total_revenue += sum([lender.price for lender in market.lenders])
    #         total_price_spread += sum([market.lenders[i].price - market.lenders[i].match.price for i in range(NUM_AGENTS)])
    #         total_duration_spread += sum([market.lenders[i].duration - market.lenders[i].match.duration for i in range(NUM_AGENTS)])
    #         if market.is_stable():
    #             stable_count += 1
    #     print(f"Stability rate for epsilon = {epsilon}: {stable_count / NUM_ROUNDS}")
    #     print(f"Avg market revenue for epsilon = {epsilon}: {total_revenue / NUM_ROUNDS}")
    #     print(f"Agg price spread for epsilon = {epsilon}: {total_price_spread / NUM_ROUNDS}")
    #     print(f"Agg duration spread for epsilon = {epsilon}: {total_duration_spread / NUM_ROUNDS}")
        
    #     stability_rates.append(stable_count / NUM_ROUNDS)
    #     revenues.append(total_revenue / NUM_ROUNDS)
    #     price_spreads.append(total_price_spread / NUM_ROUNDS)
    #     duration_spreads.append(total_duration_spread / NUM_ROUNDS)

    # # LOWESS (Locally Weighted Scatterplot Smoothing)
    # lowess_stability = sm.nonparametric.lowess(stability_rates, epsilons, frac=0.3)

    # # Graph 1: Stability Rate
    # plt.figure()
    # plt.scatter(epsilons, stability_rates, color='blue', label='Stability Rate')
    # plt.plot(lowess_stability[:, 0], lowess_stability[:, 1], color='red', label='LOWESS Trendline (Stability)')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Stability Rate')
    # plt.title('Utility Grouped Indifference: Stability Rate vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    
    # # Graph 2: System Revenue and Aggregate Price Spread
    # plt.figure()
    # plt.plot(epsilons, revenues, color='green', label='Market Revenue')
    # plt.plot(epsilons, price_spreads, color='orange', label='Aggregate Price Spread')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Revenue / Price Spread')
    # plt.title('Utility Grouped Indifference: Market Revenue and Aggregate Price Spread vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # Graph 3: Aggregate Duration Spread
    # plt.figure()
    # plt.plot(epsilons, duration_spreads, color='green', label='Aggregate Duration Spread')
    # plt.xlabel('Epsilon (Group Size)')
    # plt.ylabel('Duration Spread')
    # plt.title('Utility Grouped Indifference: Aggregate Duration Spread vs Epsilon')
    # plt.legend()
    # plt.grid(True)
    # plt.show()


    """ UTILITY STOCHASTIC: STABILITY RATE VS. STD """
    # stability_rates = []
    # revenues = [] # total system revenue per round
    # price_spreads = [] # lender price - renter price
    # duration_spreads = []
    # epsilons = np.arange(0, 0.1, 0.001)
    # for epsilon in epsilons:
    #     stable_count = 0
    #     total_revenue = 0
    #     total_price_spread = 0
    #     total_duration_spread = 0
    #     for round in range(NUM_ROUNDS):
    #         market = Marketplace(NUM_AGENTS, DURATION_MEAN, DURATION_STD, PRICE_STD, "UTILITY", "STOCHASTIC", epsilon)
    #         total_revenue += sum([lender.price for lender in market.lenders])
    #         total_price_spread += sum([market.lenders[i].price - market.lenders[i].match.price for i in range(NUM_AGENTS)])
    #         total_duration_spread += sum([market.lenders[i].duration - market.lenders[i].match.duration for i in range(NUM_AGENTS)])
    #         if market.is_stable():
    #             stable_count += 1
    #     print(f"Stability rate for epsilon = {epsilon}: {stable_count / NUM_ROUNDS}")
    #     print(f"Avg market revenue for epsilon = {epsilon}: {total_revenue / NUM_ROUNDS}")
    #     print(f"Agg price spread for epsilon = {epsilon}: {total_price_spread / NUM_ROUNDS}")
    #     print(f"Agg duration spread for epsilon = {epsilon}: {total_duration_spread / NUM_ROUNDS}")
        
    #     stability_rates.append(stable_count / NUM_ROUNDS)
    #     revenues.append(total_revenue / NUM_ROUNDS)
    #     price_spreads.append(total_price_spread / NUM_ROUNDS)
    #     duration_spreads.append(total_duration_spread / NUM_ROUNDS)

    # # LOWESS (Locally Weighted Scatterplot Smoothing)
    # lowess_stability = sm.nonparametric.lowess(stability_rates, epsilons, frac=0.3)

    # # Graph 1: Stability Rate
    # plt.figure()
    # plt.scatter(epsilons, stability_rates, color='blue', label='Stability Rate')
    # plt.plot(lowess_stability[:, 0], lowess_stability[:, 1], color='red', label='LOWESS Trendline (Stability)')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Stability Rate')
    # plt.title('Utility Stochastic Indifference: Stability Rate vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    
    # # Graph 2: System Revenue and Aggregate Price Spread
    # plt.figure()
    # plt.plot(epsilons, revenues, color='green', label='Market Revenue')
    # plt.plot(epsilons, price_spreads, color='orange', label='Aggregate Price Spread')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Revenue / Price Spread')
    # plt.title('Utility Stochastic Indifference: Market Revenue and Aggregate Price Spread vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # Graph 3: Aggregate Duration Spread
    # plt.figure()
    # plt.plot(epsilons, duration_spreads, color='green', label='Aggregate Duration Spread')
    # plt.xlabel('True Pref Weights Std from Reported Pref Weights')
    # plt.ylabel('Duration Spread')
    # plt.title('Utility Stochastic Indifference: Aggregate Duration Spread vs Report Std')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    
