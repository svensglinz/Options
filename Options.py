import numpy as np
import math as m
from scipy import stats
import pandas as pd

"""
DESCRIPTION
"""

class Option:

    def __init__(self, type, S,K ,r,t, div = 0, v = None, European = True):
        self.type = 1 if type == "Call" else -1
        self.K = K
        self.S = S
        self.v = v
        self.r = r
        self.t = t
        self.European = European
        self.div = div

    def price(self, method = "BSM", nstep = None, nsim = None, path = False, antithetic = False, seed = None,
              discrete = False):

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
            q = (m.exp((self.r- self.div)*dt)-d)/(u-d)

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
                            if discrete = False:
                                option[i, j - 1] = m.exp(-self.r * dt) * (q * option[i, j] + (1 - q) * option[i + 1, j])
                            else:
                                option[i, j - 1] = (1/m.pow((1+self.r), self.t/nstep)) * (q * option[i, j] + (1 - q) * option[i + 1, j])
                price = option[0,0]

            if not self.European:

                option = np.zeros((nstep + 1, nstep + 1))
                for j in range(nstep + 1, 0, -1):
                    for i in range(j):
                        if (j == nstep + 1):
                            option[i, j - 1] = max((Tree[i, j - 1] - self.K) * self.type, 0)
                        else:
                            option[i, j - 1] = max((Tree[i, j - 1]-self.K)*self.type,
                                                   m.exp(-self.r * dt) * (q * option[i, j] + (1 - q) * option[i + 1, j]))
                price = option[0, 0]

            if path:
                return {"price":price, "tree": Tree}
            else:
                return price

        elif method == "MC":

            np.random.seed(seed)
            #simulate stock price paths
            e = np.random.normal(0, 1, size=(nsim, nstep))
            if antithetic:
                e = np.concatenate((e, -e), axis = 0)
            else:
                pass
            drift = (self.r - 0.5 * self.v ** 2) * (self.t / nstep)
            shock = self.v * m.sqrt(self.t / nstep) * e

            S_t = self.S * np.exp((drift + shock).cumsum(axis=1))


            if self.European:
                S_T = S_t[:, nstep - 1]
                C_T = np.fmax((S_T - self.K) * self.type, 0)
                price = np.exp(-self.r * self.t) * np.mean(C_T)

                if path:
                    return {"price":price, "tree": pd.DataFrame(S_t)}
                else:
                    return price

            if not self.European:
                print("For Monte Carlo, only pricing for european Option is available")
                return None

    """
    Theta: Time Decay per Day (1 year =365 Days) 
    """
    def greeks(self, *args):

        greeks = {}
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.v ** 2) * self.t) / (self.v * np.sqrt(self.t))
        d2 = d1 - self.v * np.sqrt(self.t)

        if self.type == 1:
            greeks["delta"] = stats.norm.cdf(d1)
        elif self.type == -1:
            greeks["delta"] = -stats.norm.cdf(-d1)

        greeks["vega"] = (self.S * stats.norm.pdf(d1) * np.sqrt(self.t)) / 100
        greeks["theta"] = (- self.v / (2* m.sqrt(self.t)) * self.S * stats.norm.pdf(d1) - \
                self.r * self.K * m.exp(-self.r * self.t) * stats.norm.cdf(d2))/365
        greeks["rho"] = (self.t * np.exp(-self.r * self.t) * self.K * stats.norm.cdf(d2))/100
        greeks["gamma"] = stats.norm.pdf(d1)/(self.v*self.S*np.sqrt(self.t))

        if len(args) == 0:
            return greeks
        else:
            return greeks.get(args[0])

    def implied_vol(self, price):

        print("Implied Volatility determined with BSM Model")

        max_iter = 100
        precision = 1.0e-10
        v_guess = 0.5

        for i in range(0, max_iter):
            self.v = v_guess
            vega = self.greeks("vega") * 100
            diff = self.price() - price
            if (abs(diff) < precision):
                return v_guess
            v_guess = v_guess - diff / vega





