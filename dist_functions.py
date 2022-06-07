import numpy as np
import random
def invNormal(low, high, mu=0, sd=1, *, size=1000, block_size=1024):
    remain = size
    result = []
    
    mul = -0.5 * sd**-2

    while remain:
        # draw next block of uniform variates within interval
        x = np.random.uniform(low, high, size=min((remain+5)*2, block_size))
        
        # reject proportional to normal density
        x = x[np.exp(mul*(x-mu)**2) < np.random.rand(*x.shape)]
        
        # make sure we don't add too much
        if remain < len(x):
            x = x[:remain]

        result.append((x))
        remain -= len(x)

    return np.concatenate(result)

def randomNumbersNormalInverseDisturbition(low,high,mu,sigma):
    
    numbersDisturbited = invNormal(low,high,mu,sigma)
    number1=int(random.choice(numbersDisturbited))
    number2=int(random.choice(numbersDisturbited))
    return number1,number2

