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

        self.pref_order = None

        self.match = None # to be matched

    def pricing(self, duration):
        # price as a sigmoid function of duration
        # optimize for 6-hour slot
        # price_fx = 8/(1+math.exp(-(1.2*duration-4)))
        price_fx = duration # LINEAR FUNCTION
        # wrap in gaussian where function is mean
        return np.random.normal(price_fx, self.price_std)


class Lender(Agent):
    def __init__(self, id, duration_mean, duration_std, price_std):
        super().__init__(id, duration_mean, duration_std, price_std)

    def strict_pref_order(self, renters):
        if self.priority == "DURATION":
            # decreasing order of price (higher price = higher priority)
            price_sort = sorted(renters, key=lambda renter: renter.price, reverse=True)
            # increasing order of duration
            sorted_renters = sorted(price_sort, key=lambda renter: abs(renter.duration - self.duration))
        else: 
            # increasing order of dist from duration
            duration_sort = sorted(renters, key=lambda renter: abs(renter.duration - self.duration))
            # decreasing order of price (higher price = higher priority)
            sorted_renters = sorted(duration_sort, key=lambda renter: renter.price, reverse=True)
        
        self.pref_order = sorted_renters

    def weighted_pref_order(self, renters):
        # sort by duration, sort by price, then sort by weighted average of two rankings
        price_sort = sorted(renters, key=lambda renter: renter.price, reverse=True)
        duration_sort = sorted(renters, key=lambda renter: abs(renter.duration - self.duration))
        
        weighted_rankings = []
        for renter in renters:
            price_rank = price_sort.index(renter)
            duration_rank = duration_sort.index(renter)
            weighted_avg = (self.weights["PRICE"]*price_rank) + (self.weights["DURATION"]*duration_rank)/len(self.weights)
            weighted_rankings.append((renter, weighted_avg))
        weighted_sort = sorted(weighted_rankings, key=lambda rank: rank[1])

        sorted_renters = [renter for (renter, weighted_avg) in weighted_sort]
        
        self.pref_order = sorted_renters

class Renter(Agent):
    def __init__(self, id, duration_mean, duration_std, price_std):
        super().__init__(id, duration_mean, duration_std, price_std)

    def strict_pref_order(self, lenders):
        if self.priority == "DURATION":
            # increasing order of price (lower price = higher priority)
            price_sort = sorted(lenders, key=lambda lender: lender.price)
            # increasing order of duration
            sorted_lenders = sorted(price_sort, key=lambda lender: abs(lender.duration - self.duration))
        else: 
            # increasing order of dist from duration
            duration_sort = sorted(lenders, key=lambda lender: abs(lender.duration - self.duration))
            # decreasing order of price (lower price = higher priority)
            sorted_lenders = sorted(duration_sort, key=lambda lender: lender.price)
        
        self.pref_order = sorted_lenders

    def weighted_pref_order(self, lenders):
        # sort by duration, sort by price, then sort by weighted average of two rankings
        price_sort = sorted(lenders, key=lambda lender: lender.price)
        duration_sort = sorted(lenders, key=lambda lender: abs(lender.duration - self.duration))
        
        weighted_rankings = []
        for lender in lenders:
            price_rank = price_sort.index(lender)
            duration_rank = duration_sort.index(lender)
            weighted_avg = (self.weights["PRICE"]*price_rank) + (self.weights["DURATION"]*duration_rank)/len(self.weights)
            weighted_rankings.append((lender, weighted_avg))
        weighted_sort = sorted(weighted_rankings, key=lambda rank: rank[1])

        sorted_lenders = [lender for (lender, weighted_avg) in weighted_sort]
        
        self.pref_order = sorted_lenders