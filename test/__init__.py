from pandas import *
import numpy as np
df = DataFrame({'B': [0, np.nan, 2, 3, 4]})
print(df)


print(df['B'].rolling(2).sum())