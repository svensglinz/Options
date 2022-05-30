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

```
#initialize Option 

Vanilla_Option(S = 100, K = 100, v = 0.3, r = 0.05, t = 1, type = "Call")
```
The Class *Vanilla Option* contains the following methods:
```
#initialize Option
option_1 = Vanilla_Option(S = 100, K = 100, v = 0.3, r = 0.05, t = 1, type = "Call")
option_2 = Vanilla_Option(S = 100, K = 100, r = 0.05, t = 1, type = "Call", price_act = 5)
```
```
#get results:
option.price(method = "BSM")
>
option.price(method = "MC", nsim = 10, nstep = 10)
>
option.price(method = "CRR", nstep = 100)
>
option.greeks("delta")
>
```

```
option_2.implied_vol()
>
```
