from agent import Renter, Lender

class Marketplace():
    def __init__(self, num_agents, duration_mean, duration_std, price_std, match_algo, report_algo, true_algo, epsilon):
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
        if match_algo == "DA": # deferred acceptance
            self.matchings = self.match()
        elif match_algo == "BOSTON": # immediate acceptance (boston)
            self.matchings = self.boston_match()
        elif match_algo == "RICH":
            self.matchings = self.richest_renter_match()
        else:
            raise NotImplementedError("This algo has not been implemented.")

        # print(f"Checking for stability...")
        # self.stable = self.is_stable()

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

    def match(self):
        # renter-proposing

        # convert lender pref lists into dictionary for faster lookup
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
    
    def boston_match(self):
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
    
        # Initialize all renters as free
        free_renters = set(self.renters)

        # Initialize all lenders as free
        for lender in self.lenders:
            lender.match = None

        while free_renters:
            # In each round, each free renter applies to their most preferred lender that has not yet rejected them
            for renter in list(free_renters):
                if not renter.reported_pref_order:  # If the renter has no more preferences, they remain unmatched
                    free_renters.remove(renter)
                    continue

                # Renter applies to the most preferred lender in their list
                preferred_group = renter.reported_pref_order.pop(0)
                for preferred_lender in preferred_group:
                    # If the lender is free or prefers this renter over their current match
                    if preferred_lender.match is None or lenders_prefs[preferred_lender.id][renter.id] < lenders_prefs[preferred_lender.id][preferred_lender.match.id]:
                        # If the lender is already matched, the current match becomes free
                        if preferred_lender.match:
                            free_renters.add(preferred_lender.match)
                            preferred_lender.match.match = None

                        # Match the renter and the lender
                        preferred_lender.match = renter
                        renter.match = preferred_lender
                        free_renters.remove(renter)
                        break  # Renter exits the loop once matched

        matchings = [(renter.id, renter.match.id if renter.match else None) for renter in self.renters]
        return matchings
    
    def richest_renter_match(self):
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

        # Sort renters by price in descending order
        sorted_renters = sorted(self.renters, key=lambda renter: renter.price, reverse=True)

        # Initialize all lenders as free
        for lender in self.lenders:
            lender.match = None

        # Renters propose in order of their price, highest first
        for renter in sorted_renters:
            for preferred_group in renter.reported_pref_order:
                for preferred_lender in preferred_group:
                    # If the lender is free or prefers this renter over their current match
                    if preferred_lender.match is None or lenders_prefs[preferred_lender.id][renter.id] < lenders_prefs[preferred_lender.id][preferred_lender.match.id]:
                        # If the lender is already matched, the current match becomes unmatched
                        if preferred_lender.match:
                            preferred_lender.match.match = None

                        # Match the renter and the lender
                        preferred_lender.match = renter
                        renter.match = preferred_lender
                        break  # Renter exits the loop once matched

                if renter.match:
                    break  # Move to the next renter once the current one is matched

        matchings = [(renter.id, renter.match.id if renter.match else None) for renter in self.renters]
        return matchings

        