# Options

## Functionality: 

The following code can price plain vanilla options (European and American) 
The Option can be priced with the following mehtods: 
  
  European: 
  - Black Scholes Model 
  - Cox Ross Rubinstein Binomial Model 
  - Monte Carlo Model
  
  American: 
  - Cox Ross Rubinstein Binomial Model 
 
### Initialize Option: 
Arguments: 
- S: Current Stock Price
- K: Strike Price
- v: [OPTIONAL] annualized Volatility (ie. 10% = 0.1)
- r: annualized interest rate (ie. 10% = 0.1)
- t: Time to Maturity (in years)
- type: "Call" or "Put"
- European = True (default)

```
#initialize Option
Option(S = 100, K = 100, v = 0.3, r = 0.05, t = 1, type = "Call", European = True)
```
### Methods: 
#### price()
Arguments: 
- method = "BSM" (default), "MC" for Monte Carlo, "CRR" for binomial tree
- nsim / nstep (no default), required for method = "MC" and "CRR"
- antithetic = False (default), can be set to True for method = "MC"
- path = False (default), true returns simulated stock prices (method = "MC") / binomoal tree (method = "CRR")

```
option.price() 
option.price(mehtod = "MC", nsim = 10, nstep = 100, antithetic = False, path = False)
option.price(method  = "CRR", nstep = 100, path = False)
```

#### greeks()
no argument returns a list of all greeks using BSM model. Alternatively, each greek can be passed individually to the function which only returns the specific greek then
```
option.greeks() 
option.greeks("delta") 
```
#### implied_vol()
returns implied volatility for the given price using the BSM Model
```
option.implied_vol(price = 10)
```
