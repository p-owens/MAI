import pandas as pd
import os

os.chdir(os.path.dirname(__file__)) # get cwd
df = pd.read_csv('fdata.csv',                        
                        header=6,
                        names=['THz', 'dBm', 'disc'],
                        chunksize=1000, #probably need to include "chunksize=1000" when dealing with actual file
                        ) 

#bigdata = pd.concat([dfs in df], ignore_index=True, sort=False)


chunks = iter(df) 

for x in chunks:
    print(x)

                