from agent import Renter, Lender

class Marketplace():
    # algo = "STRICT", "WEIGHTED"
    def __init__(self, num_agents, duration_mean, duration_std, price_std, report_algo, true_algo):
        self.num_agents = num_agents
        self.duration_mean = duration_mean
        self.duration_std = duration_std
        self.price_std = price_std

        self.renters = [Renter(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]
        self.lenders = [Lender(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]

        self.generate_pref_orders(report_algo, true_algo)

        self.matchings = self.match()

    def generate_pref_orders(self, report_algo, true_algo):
        # generate report pref order: STRICT, WEIGHTED
        if report_algo == "STRICT": # strict preference orders
            for i in range(self.num_agents):
                self.renters[i].strict_pref_order(self.lenders)
                self.lenders[i].strict_pref_order(self.renters)
        else: # weighted preference orders
            for i in range(self.num_agents):
                self.renters[i].weighted_pref_order(self.lenders)
                self.lenders[i].weighted_pref_order(self.renters)

        # generate true pref order: STOCHASTIC, GROUPED, AREA
        if true_algo == "STOCHASTIC": # fuzziness in weight reportings
            ADJUSTED_STD = 0.1
            for i in range(self.num_agents):
                self.renters[i].stoch_pref_order(self.lenders, ADJUSTED_STD)
                self.lenders[i].stoch_pref_order(self.renters, ADJUSTED_STD)
        elif true_algo == "GROUPED": # ceiling function
            for i in range(self.num_agents):
                self.renters[i].grouped_pref_order(self.lenders)
                self.lenders[i].grouped_pref_order(self.renters)
        else: # area
            for i in range(self.num_agents):
                self.renters[i].area_pref_order(self.lenders)
                self.lenders[i].area_pref_order(self.renters)
            

    def match(self):
        # renter-proposing

        # convert lender pref lists into dictionary for faster lookup
        lenders_prefs = {lender.id: {renter.id: i for (i, renter) in enumerate(lender.reported_pref_order)} for lender in self.lenders}
        renter_prefs = {renter.id: {lender.id: i for (i, lender) in enumerate(renter.reported_pref_order)} for renter in self.renters}
        print("Lender preferences:", lenders_prefs)
        print("Renter preferences:",renter_prefs)

        # initialize set of unmatched renters
        free_renters = set(self.renters)

        while free_renters: # while there exists unmatched renters
            # select a renter
            renter = free_renters.pop()
            # print(f"renter {renter.id}")
            
            for preferred_lender in renter.reported_pref_order:
                for preferred_group in preferred_group:
                    # if lender is free, match
                    if preferred_lender.match is None:
                        preferred_lender.match = renter
                        renter.match = preferred_lender
                        # print("matched empty")
                        print(f"lender {preferred_lender.id} matched with renter {renter.id}")
                        break
                    # if lender has a prior match, check higher priority
                    else:
                        current_match_rank = lenders_prefs[preferred_lender.id][preferred_lender.match.id]
                        new_match_rank = lenders_prefs[preferred_lender.id][renter.id]

                        if new_match_rank < current_match_rank:
                            # If the lender prefers the new renter, make the switch
                            free_renters.add(preferred_lender.match)
                            preferred_lender.match = renter
                            renter.match = preferred_lender
                            # print("matched non-empty")
                            print(f"lender {preferred_lender.id} matched with renter {renter.id}")
                            break
                if renter.match:
                    break 
        
        matchings = [(renter.id, renter.match.id) for renter in self.renters]

        print(f"(renter,lender) matches: {matchings}")
        return matchings
    
    def is_stable(self):
        # check each lender
        for lender in self.lenders:
            for preferred_group in lender.true_pref_order:

                for preferred_renter in preferred_group:
                    # Check if the lender prefers this renter over their current match
                    if lender.true_pref_order.index(preferred_renter) < lender.true_pref_order.index(lender.match):
                        # Check if the preferred renter also prefers this lender over their current match
                        # if preferred_renter.true_pref_order.index(lender) < preferred_renter.true_pref_order.index(preferred_renter.match):
                        
                        # pref group version
                        if any(preferred_lender in renter.true_pref_order for preferred_lender in lender.true_pref_order):
                            return False  # Found an unstable pair
                
        # Check each renter
        for renter in self.renters:
            for preferred_lender in renter.true_pref_order:
                # Check if the renter prefers this lender over their current match
                if renter.true_pref_order.index(preferred_lender) < renter.true_pref_order.index(renter.match):
                    # Check if the preferred lender also prefers this renter over their current match
                    # if preferred_lender.true_pref_order.index(renter) < preferred_lender.true_pref_order.index(preferred_lender.match):
                    if any(preferred_renter in lender.true_pref_order for preferred_renter in renter.true_pref_order):
                        return False  # Found an unstable pair
                    
        return True
