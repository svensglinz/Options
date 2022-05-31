# Options

## Functionality: 

The following code can price plain vanilla options (European and American) as well as some popular exotic options using different pricing models. 

Plain Vanilla Options can be priced with: 
  
  European: 
  - Black Scholes Model 
  - Cox Ross Rubinstein Binomial Model 
  - Monte Carlo Model
  
  American: 
  - Cox Ross Rubinstein Binomial Model 
  - Monte Carlo Model

  Exotic Options (...list...)
  - Monte Carlo Model


The script contains the class *Vanilla_Option* and *Exotic Option*

### Vanilla Options: 
Arguments: S: Current Stock Price, K: Strike Price, v: [OPTIONAL] annualized Volatility (ie. 10% = 0.1), r: annualized interest rate (ie. 10% = 0.1), t: Time to Maturity (in years), type: "Call" or "Put"

European: Set to True by default. Needs to be changed to False for American Options
"""

```
Vanilla_Option(S = 100, K = 100, v = 0.3, r = 0.05, t = 1, type = "Call", European = True)
```
Methods: 
#get results:
"""
method: Default is "BSM", can be changed to "CRR" (cox ross rubinstein) or "MC" (Monte Carlo)
--> CRR requires nstep / MC requires nstep and nsim
"""
"""
leaving empty will return all greeks, alternatively, we can get only one greek by including the argument 
"delta", "vega", "gamma", etc. in the function. 
"""
```
option.price(method = "BSM")
option.price(mehtod = "MC", nsim = 10, nstep = 100)
option.greeks()
option.greeks("delta")
```

```
get implied volatility for a specific Option price (using the BSM Model)
option_2.implied_vol(price = )
>
```
