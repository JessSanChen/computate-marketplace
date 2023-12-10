import random 
import numpy as np
import math


class Agent:
    def __init__(self, id, duration_mean, duration_std, price_std):
        self.id = id
        self.duration_mean = duration_mean
        self.duration_std = duration_std
        self.price_std = price_std

        # sample with gaussian; price as fx of duration
        self.duration = np.random.normal(self.duration_mean, self.duration_std)
        self.price = self.pricing(self.duration)

        # randomly generate 1st priority heuristic
        self.priority = random.choice(["DURATION", "PRICE"])
        # use dirichlet to randomly generate weights
        duration_weight = random.random()
        weights = {
            "DURATION": duration_weight,
            "PRICE": 1 - duration_weight
        }
        # self.weights = np.random.dirichlet(np.ones(len(HEURISTICS),size=1))
        self.weights = weights

        self.reported_pref_order = None
        self.true_pref_order = None # TODO

        self.match = None # to be matched

    def pricing(self, duration):
        # price as a sigmoid function of duration
        # optimize for 6-hour slot
        # price_fx = 8/(1+math.exp(-(1.2*duration-4)))
        price_fx = duration # LINEAR FUNCTION
        # wrap in gaussian where function is mean
        return np.random.normal(price_fx, self.price_std)
    
    def stoch_pref_order(self, others, adjusted_std):
        # agents don't actually know their true preferences, this is "benchmark"?
        new_duration_weight = np.random.normal(self.weights["DURATION"], adjusted_std)

        duration_mean = np.mean([other.duration for other in others])
        duration_std = np.std([other.duration for other in others])
        price_mean = np.mean([other.price for other in others])
        price_std = np.std([other.price for other in others])

        utility_dict = {}
        for other in others:
            duration_diff_normalized = abs(other.duration - self.duration)/duration_std 
            price_normalized = (other.price - price_mean)/price_std 

            # calculate_utility implemented by children
            utility = self.calculate_utility(new_duration_weight, duration_diff_normalized, price_normalized)
            utility_dict.setdefault(utility, []).append(other)
        
        # list of lists; inner list is group of agents with same utility
        sorted_agents = [group for _, group in sorted(utility_dict.items(), key=lambda item: item[0])]
        self.true_pref_order = sorted_agents
    
    def calculate_utility(self, duration_weight, other_duration, other_price):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def group_pref_order(self, others):
        raise NotImplementedError("TODO.")
    
    def area_pref_order(self, others):
        raise NotImplementedError("TODO.")
    

    def strict_pref_order(self, renters):
        is_price_descending = self.is_price_high_good() # true for lender, false for renter

        if self.priority == "DURATION":
            # decreasing order of price (higher price = higher priority)
            price_sort = sorted(renters, key=lambda renter: renter.price, reverse=is_price_descending)
            # increasing order of duration
            sorted_renters = sorted(price_sort, key=lambda renter: abs(renter.duration - self.duration))
        else: 
            # increasing order of dist from duration
            duration_sort = sorted(renters, key=lambda renter: abs(renter.duration - self.duration))
            # decreasing order of price (higher price = higher priority)
            sorted_renters = sorted(duration_sort, key=lambda renter: renter.price, reverse=is_price_descending)
        
        self.reported_pref_order = sorted_renters
    
    def is_price_high_good(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def weighted_pref_order(self, renters):
        is_price_descending = self.is_price_high_good() # true for lender, false for renter

        # sort by duration, sort by price, then sort by weighted average of two rankings
        price_sort = sorted(renters, key=lambda renter: renter.price, reverse=is_price_descending)
        duration_sort = sorted(renters, key=lambda renter: abs(renter.duration - self.duration))
        
        utility_dict = {}
        for renter in renters:
            price_rank = price_sort.index(renter)
            duration_rank = duration_sort.index(renter)
            weighted_avg = (self.weights["PRICE"]*price_rank) + (self.weights["DURATION"]*duration_rank)/len(self.weights)
            utility_dict.setdefault(weighted_avg, []).append(renter)

        sorted_renters = [group for _, group in sorted(utility_dict.items(), key=lambda item: item[0])]
        
        self.reported_pref_order = sorted_renters


class Lender(Agent):
    def __init__(self, id, duration_mean, duration_std, price_std):
        super().__init__(id, duration_mean, duration_std, price_std)

    # for pref order: sort descending?
    def is_price_high_good(self):
        return True

    def calculate_utility(self, duration_weight,duration_normalized, price_normalized):
        # score is diff of weighted, normalized 
        # higher price is better, higher duration is worse
        utility = (1-duration_weight) * price_normalized - duration_weight * duration_normalized
        return utility

class Renter(Agent):
    def __init__(self, id, duration_mean, duration_std, price_std):
        super().__init__(id, duration_mean, duration_std, price_std)

    # for pref order: sort descending?
    def is_price_high_good(self):
        return False

    def calculate_utility(self, duration_weight, duration_normalized, price_normalized):
        # score is diff of weighted, normalized 
        # lower price is better, lower duration is worse
        utility = duration_weight * duration_normalized - (1-duration_weight) * price_normalized
        return utility