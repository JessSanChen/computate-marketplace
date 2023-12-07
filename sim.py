from agent import Renter, Lender

class Simulation():
    # algo = "STRICT", "WEIGHTED"
    def __init__(self, num_agents, duration_mean, duration_std, price_std, algo):
        self.num_agents = num_agents
        self.duration_mean = duration_mean
        self.duration_std = duration_std
        self.price_std = price_std

        self.renters = [Renter(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]
        self.lenders = [Lender(i, duration_mean, duration_std, price_std) for i in range(self.num_agents)]

        self.generate_pref_orders(algo)

        self.matchings = self.match()

    def generate_pref_orders(self, algo):
        if algo == "STRICT": # strict preference orders
            for i in range(self.num_agents):
                self.renters[i].strict_pref_order(self.lenders)
                self.lenders[i].strict_pref_order(self.renters)
        else: # weighted preference orders
            for i in range(self.num_agents):
                self.renters[i].weighted_pref_order(self.lenders)
                self.lenders[i].weighted_pref_order(self.renters)

    def match(self):
        # renter-proposing

        # convert lender pref lists into dictionary for faster lookup
        lenders_prefs = {lender.id: {renter.id: i for (i, renter) in enumerate(lender.pref_order)} for lender in self.lenders}
        renter_prefs = {renter.id: {lender.id: i for (i, lender) in enumerate(renter.pref_order)} for renter in self.renters}
        print("Lender preferences:", lenders_prefs)
        print("Renter preferences:",renter_prefs)

        # initialize set of unmatched renters
        free_renters = set(self.renters)

        while free_renters: # while there exists unmatched renters
            # select a renter
            renter = free_renters.pop()
            # print(f"renter {renter.id}")
            
            for preferred_lender in renter.pref_order:
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
        
        matchings = [(renter.id, renter.match.id) for renter in self.renters]

        print(f"(renter,lender) matches: {matchings}")
        return matchings


