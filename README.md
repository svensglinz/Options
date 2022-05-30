# Options

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
