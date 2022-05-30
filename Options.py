import numpy as np
import math as m
from scipy import stats

"""
DESCRIPTION
"""

class Vanilla_Option:

    def __init__(self, type, S,K ,r,t, v = None, act_price = None, European = True):
        self.type = 1 if type == "Call" else -1
        self.K = K
        self.S = S
        self.v = v
        self.r = r
        self.t = t
        self.act_price = act_price
        self.European = European

    def price(self, method = "BSM", nstep = None, nsim = None):

        if method == "BSM":
            d1 = (np.log(self.S/self.K) + (self.r + 0.5 * self.v**2)*self.t)/(self.v * np.sqrt(self.t))
            d2 = d1 - self.v * np.sqrt(self.t)

            if self.European:
                price = (self.S * stats.norm.cdf(d1* self.type) - self.K * \
                        np.exp(-self.r * self.t) * stats.norm.cdf(d2 * self.type)) * self.type
                return price

            if not self.European:
                print("BSM Method can only price European Options. Please change specifications!")

        elif method == "CRR":

            # calculate binomial tree
            dt = self.t / nstep
            u = m.exp(self.v * m.sqrt(dt))
            d = 1 / u
            q = (m.exp(self.r * dt) - d) / (u - d)
            Tree = np.zeros((nstep + 1, nstep + 1))
            for j in range(nstep + 1):
                for i in range(j + 1):
                    Tree[i, j] = self.S * m.pow(d, i) * m.pow(u, j - i)

            if self.European:
                option = np.zeros((nstep + 1, nstep + 1))
                for j in range(nstep + 1, 0, -1):
                    for i in range(j):
                        if (j == nstep + 1):
                            option[i, j - 1] = max((Tree[i, j - 1] - self.K) * self.type, 0)
                        else:
                            option[i, j - 1] = m.exp(-self.r * dt) * (q * option[i, j] + (1 - q) * option[i + 1, j])
                return option[0, 0]

            if not self.European:

                option = np.zeros((nstep + 1, nstep + 1))
                for j in range(nstep + 1, 0, -1):
                    for i in range(j):
                        if (j == nstep + 1):
                            option[i, j - 1] = max((Tree[i, j - 1] - self.K) * self.type, 0)
                        else:
                            option[i, j - 1] = max(self.K - Tree[i, j - 1], m.exp(-self.r * dt) * (q * option[i, j] + \
                                                                                                   (1 - q) * option[
                                                                                                       i + 1, j]))
                return option[0, 0]


        elif method == "MC":

            #simulate stock price paths
            e = np.random.normal(0, 1, size=(nsim, nstep))
            drift = (self.r - 0.5 * self.v ** 2) * (self.t / nstep)
            shock = self.v * m.sqrt(self.t / nstep) * e
            S_t = self.S * np.exp((drift + shock).cumsum(axis=1))


            if self.European:
                S_T = S_t[:, nstep - 1]
                C_T = np.fmax((S_T - self.K) * self.type, 0)
                price = np.exp(-self.r * self.t) * np.mean(C_T)
                return price

            if not self.European:
                pass

    def greeks(self, *args):

        print("Greeks determined with BSM Model")
        greeks = {}
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.v ** 2) * self.t) / (self.v * np.sqrt(self.t))
        d2 = d1 - self.v * np.sqrt(self.t)

        if self.type == "Call":
            greeks["delta"] = stats.norm.cdf(d1)
        elif self.type == "Put":
            greeks["delta"] = -stats.norm.cdf(-d1)

        greeks["vega"] = vega = self.S * stats.norm.pdf(d1,0.0,1.0) * np.sqrt(self.t)
        greeks["theta"] = - self.v / (2* m.sqrt(self.t)) * self.S * stats.norm.pdf(d1) - \
                self.r * self.K * m.exp(-self.r * self.t) * stats.norm.cdf(d2)
        greeks["rho"] = self.t* m.exp(-self.r * self.t) * self.K * stats.norm.cdf(d2)
        greeks["gamma"] = self.S * stats.norm.pdf(d1) * m.sqrt(self.t)

        return greeks.get(args[0])

    def implied_vol(self):

        print("Implied Volatility determined with BSM Model")
        max_iter = 100
        precision = 1.0e-10
        v_guess = 0.5

        for i in range(0, max_iter):
            self.v = v_guess
            vega = self.greeks("vega")
            diff = self.price() - self.act_price
            if (abs(diff) < precision):
                return v_guess
            v_guess = v_guess - diff / vega


"""
DESCRIPTION
"""

class Exotic_Option:

    def __init__(self, type, S,K ,r,t, v = None, act_price = None):
        self.type = 1 if type == "Call" else -1
        self.K = K
        self.S = S
        self.v = v
        self.r = r
        self.t = t
        self.act_price = act_price



"""
DESCRIPTION
"""

