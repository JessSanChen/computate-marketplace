from agent import Renter, Lender

class Marketplace():
    def __init__(self, num_agents, duration_mean, duration_std, price_std, report_algo, true_algo, epsilon):
        self.num_agents = num_agents
        self.duration_mean = duration_mean
        self.duration_std = duration_std
        self.price_std = price_std

        # print(f"Generating {num_agents} renters and lenders...")
        self.renters = [Renter(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]
        self.lenders = [Lender(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]

        # print(f"Calculating reported pref orders using {report_algo} and true pref orders using {true_algo}...")
        self.generate_pref_orders(report_algo, true_algo, epsilon)

        # print(f"Performing Gale-Shapley matching...")
        self.matchings = self.match()

        # print(f"Checking for stability...")
        self.stable = self.is_stable()

    def generate_pref_orders(self, report_algo, true_algo, epsilon):
        # report_algo: UTILITY, WEIGHTED_RANK
        # true_algo: BASELINE, STOCH, GROUPED
        # epsilon is grouped_epsilon if grouped, std if stochastic
        if report_algo == "UTILITY":
            for i in range(self.num_agents):
                self.renters[i].reported_pref_order = self.renters[i].baseline_util_pref_order(self.lenders)
                self.lenders[i].reported_pref_order = self.lenders[i].baseline_util_pref_order(self.renters)
            if true_algo == "BASELINE":
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].baseline_util_pref_order(self.lenders)
                    self.lenders[i].true_pref_order = self.lenders[i].baseline_util_pref_order(self.renters)
            elif true_algo == "STOCHASTIC":
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].stoch_util_pref_order(self.lenders, epsilon)
                    self.lenders[i].true_pref_order = self.lenders[i].stoch_util_pref_order(self.renters, epsilon)
            elif true_algo == "GROUPED": 
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].grouped_util_pref_order(self.lenders, epsilon)
                    self.lenders[i].true_pref_order = self.lenders[i].grouped_util_pref_order(self.renters, epsilon)
            else:
                raise NotImplementedError("This algo has not been implemented.")
        elif report_algo == "WEIGHTED_RANK":
            for i in range(self.num_agents):
                self.renters[i].reported_pref_order = self.renters[i].baseline_weightedrank_pref_order(self.lenders)
                self.lenders[i].reported_pref_order = self.lenders[i].baseline_weightedrank_pref_order(self.renters)
            if true_algo == "BASELINE":
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].baseline_weightedrank_pref_order(self.lenders)
                    self.lenders[i].true_pref_order = self.lenders[i].baseline_weightedrank_pref_order(self.renters)
            elif true_algo == "STOCHASTIC":
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].stoch_weightedrank_pref_order(self.lenders, epsilon)
                    self.lenders[i].true_pref_order = self.lenders[i].stoch_weightedrank_pref_order(self.renters, epsilon)
            elif true_algo == "GROUPED": 
                for i in range(self.num_agents):
                    self.renters[i].true_pref_order = self.renters[i].grouped_weightedrank_pref_order(self.lenders, epsilon)
                    self.lenders[i].true_pref_order = self.lenders[i].grouped_weightedrank_pref_order(self.renters, epsilon)
            else:
                raise NotImplementedError("This algo has not been implemented.")
        else:
            raise NotImplementedError("This algo has not been implemented.")
        # # generate report pref order: STRICT, WEIGHTED
        # if report_algo == "STRICT": # strict preference orders
        #     for i in range(self.num_agents):
        #         self.renters[i].strict_pref_order(self.lenders)
        #         self.lenders[i].strict_pref_order(self.renters)
        # else: # weighted preference orders
        #     for i in range(self.num_agents):
        #         self.renters[i].weighted_pref_order(self.lenders)
        #         self.lenders[i].weighted_pref_order(self.renters)

        # # generate true pref order: STOCHASTIC, GROUPED, AREA
        # if true_algo == "STOCHASTIC": # fuzziness in weight reportings
        #     # ADJUSTED_STD = 0.1
        #     ADJUSTED_STD = 0.
        #     for i in range(self.num_agents):
        #         self.renters[i].stoch_pref_order(self.lenders, ADJUSTED_STD)
        #         self.lenders[i].stoch_pref_order(self.renters, ADJUSTED_STD)
        # elif true_algo == "SAME": # check is stable
        #     for i in range(self.num_agents):
        #         self.renters[i].true_pref_order = self.renters[i].reported_pref_order
        #         self.lenders[i].true_pref_order = self.lenders[i].reported_pref_order
        # elif true_algo == "GROUPED": # ceiling function
        #     for i in range(self.num_agents):
        #         self.renters[i].grouped_pref_order(self.lenders)
        #         self.lenders[i].grouped_pref_order(self.renters)
        # else: # area
        #     for i in range(self.num_agents):
        #         self.renters[i].area_pref_order(self.lenders)
        #         self.lenders[i].area_pref_order(self.renters)
            

    def match(self):
        # renter-proposing

        # convert lender pref lists into dictionary for faster lookup
        # lenders_prefs = {lender.id: {renter.id: i for (i, renter) in enumerate(lender.reported_pref_order)} for lender in self.lenders}
        # renter_prefs = {renter.id: {lender.id: i for (i, lender) in enumerate(renter.reported_pref_order)} for renter in self.renters}
        
        # grouped preferences version
        lenders_prefs = {
            lender.id: {
                renter.id: i
                for i, group in enumerate(lender.reported_pref_order)
                for renter in group
            }
            for lender in self.lenders
        }

        renter_prefs = {
            renter.id: {
                lender.id: i
                for i, group in enumerate(renter.reported_pref_order)
                for lender in group
            }
            for renter in self.renters
        }
        
        # print("Renter preferences:",[[[lender.id for lender in lenders] for lenders in renter.reported_pref_order] for renter in self.renters])
        # print("Lender preferences:", [[[renter.id for renter in renters] for renters in lender.reported_pref_order] for lender in self.lenders])
        

        # initialize set of unmatched renters
        free_renters = set(self.renters)

        while free_renters: # while there exists unmatched renters
            # select a renter
            renter = free_renters.pop()
            # print(f"renter {renter.id}")
            
            for preferred_group in renter.reported_pref_order:
                for preferred_lender in preferred_group:
                    # if lender is free, match
                    if preferred_lender.match is None:
                        preferred_lender.match = renter
                        renter.match = preferred_lender
                        # print("matched empty")
                        # print(f"Matched empty: Renter {renter.id} matched with lender {preferred_lender.id}")
                        break
                    # if lender has a prior match, check higher priority
                    else:
                        current_match_rank = lenders_prefs[preferred_lender.id][preferred_lender.match.id]
                        new_match_rank = lenders_prefs[preferred_lender.id][renter.id]

                        if new_match_rank < current_match_rank:
                            # If the lender prefers the new renter, make the switch
                            # print(f"Preferred lender {preferred_lender.id} was last matched with renter {preferred_lender.match.id}")
                            preferred_lender.match.match = None
                            free_renters.add(preferred_lender.match)
                            preferred_lender.match = renter
                            renter.match = preferred_lender
                            # print("matched non-empty")
                            # print(f"Matched non-empty: Renter {renter.id} matched with lender {preferred_lender.id}")
                            break
                if renter.match:
                    break 
        
        matchings = [(renter.id, renter.match.id) for renter in self.renters]

        # print(f"(renter,lender) matches: {matchings}")
        return matchings
    
    def is_stable(self):
        # Check each lender
        for lender in self.lenders:
            # print(f"BIG LOOP: Lender {lender.id}")
            lender_current_match_group_index = None
            for i, preferred_group in enumerate(lender.true_pref_order):
                if lender.match in preferred_group:
                    lender_current_match_group_index = i
                    # print(f"Lender {lender.id} is matched with renter {lender.match.id}, which is in true pref group {lender_current_match_group_index}")
                    break

            if lender_current_match_group_index is None:
                # when would this happen?
                # print(f"Lender {lender.id}'s match is not found in any of its true pref groups.")
                continue  # If the current match is not found in any group

            # checking all the "more preferred" groups for potential unstable pairs
            for preferred_group in lender.true_pref_order[:lender_current_match_group_index]:
                for preferred_renter in preferred_group:
                    # print(f"Checking preferred renter {preferred_renter.id}")
                    # Check if the preferred renter also prefers this lender over their current match
                    renter_current_match_group_index = None
                    for j, renter_preferred_group in enumerate(preferred_renter.true_pref_order):
                        if preferred_renter.match in renter_preferred_group:
                            renter_current_match_group_index = j
                            # print(f"Renter {preferred_renter.id} is matched with {preferred_renter.match.id} in true pref group {renter_current_match_group_index}")
                            break

                    # does this change for indifference?
                    # can be in same group (index + 1)
                    if any(lender in group for group in preferred_renter.true_pref_order[:renter_current_match_group_index + 1]):
                        # print("Found unstable pair.")
                        return False  # Found an unstable pair

        # Check each renter
        for renter in self.renters:
            # print(f"BIG LOOP: Renter {renter.id}")
            renter_current_match_group_index = None
            for i, preferred_group in enumerate(renter.true_pref_order):
                if renter.match in preferred_group:
                    renter_current_match_group_index = i
                    # print(f"Renter {renter.id} is matched with lender {renter.match.id}, which is in true pref group {renter_current_match_group_index}")
                    break

            if renter_current_match_group_index is None:
                # print(f"Renter {renter.id}'s match is not found in any of its true pref groups.")
                continue  # If the current match is not found in any group

            # checking all the "more preferred" groups for potential unstable pairs
            for preferred_group in renter.true_pref_order[:renter_current_match_group_index]:
                for preferred_lender in preferred_group:
                    # print(f"Checking preferred lender {preferred_lender.id}")
                    # Check if the preferred renter also prefers this lender over their current match
                    lender_current_match_group_index = None
                    for j, lender_preferred_group in enumerate(preferred_lender.true_pref_order):
                        if preferred_lender.match in lender_preferred_group:
                            lender_current_match_group_index = j
                            # print(f"Lender {preferred_lender.id} is matched with {preferred_lender.match.id} in true pref group {lender_current_match_group_index}")
                            break
                    
                    # can be in same group
                    if any(renter in group for group in preferred_lender.true_pref_order[:lender_current_match_group_index+1]):
                        # print("Found unstable pair.")
                        return False  # Found an unstable pair

        return True
    
    if False:
        def is_stable(self):
            # check each lender
            for lender in self.lenders:
                for preferred_group in lender.true_pref_order:
                    if lender.match in preferred_group:
                        # The lender's current match is in this preferred group
                        current_match_group = preferred_group
                        break
                    else:
                        # if current match not found in any group, continue
                        continue

                for preferred_group in lender.true_pref_order:
                    for preferred_renter in preferred_group:
                        if preferred_group == current_match_group:
                            # No need to check further if we reached the group of the current match
                            break

                        # Check if the preferred renter also prefers this lender over their current match
                        for renter_preferred_group in preferred_renter.true_pref_order:
                            if lender in renter_preferred_group:
                                # The lender is in one of the renter's preferred groups
                                renter_current_match_group = [group for group in preferred_renter.true_pref_order if preferred_renter.match in group][0]
                                if renter_preferred_group.index(lender) < renter_preferred_group.index(renter_current_match_group):
                                    return False  # Found an unstable pair

                    # # Check if the lender prefers this renter over their current match
                    # if lender.true_pref_order.index(preferred_renter) < lender.true_pref_order.index(lender.match):
                    #     # Check if the preferred renter also prefers this lender over their current match
                    #     # if preferred_renter.true_pref_order.index(lender) < preferred_renter.true_pref_order.index(preferred_renter.match):
                        
                    #     # pref group version
                    #     if any(preferred_lender in renter.true_pref_order for preferred_lender in lender.true_pref_order):
                    #         return False  # Found an unstable pair
                    
            # Check each renter
            for renter in self.renters:
                for preferred_group in renter.true_pref_order:
                    if renter.match in preferred_group:
                        # The renter's current match is in this preferred group
                        current_match_group = preferred_group
                        break
                else:
                    # If the current match is not found in any group, continue to the next renter
                    continue

                for preferred_group in renter.true_pref_order:
                    for preferred_lender in preferred_group:
                        if preferred_group == current_match_group:
                            # No need to check further if we reached the group of the current match
                            break

                        # Check if the preferred lender also prefers this renter over their current match
                        for lender_preferred_group in preferred_lender.true_pref_order:
                            if renter in lender_preferred_group:
                                # The renter is in one of the lender's preferred groups
                                lender_current_match_group = [group for group in preferred_lender.true_pref_order if preferred_lender.match in group][0]
                                if lender_preferred_group.index(renter) < lender_preferred_group.index(lender_current_match_group):
                                    return False  # Found an unstable pair

            # for renter in self.renters:
            #     for preferred_lender in renter.true_pref_order:
            #         # Check if the renter prefers this lender over their current match
            #         if renter.true_pref_order.index(preferred_lender) < renter.true_pref_order.index(renter.match):
            #             # Check if the preferred lender also prefers this renter over their current match
            #             # if preferred_lender.true_pref_order.index(renter) < preferred_lender.true_pref_order.index(preferred_lender.match):
            #             if any(preferred_renter in lender.true_pref_order for preferred_renter in renter.true_pref_order):
            #                 return False  # Found an unstable pair
                        
            return True
