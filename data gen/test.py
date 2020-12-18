import pandas as pd
import os
import numpy as np



lower_freq = 191.6
upper_freq = 195.9
step_size = 0.1
freq_rng = np.arange(lower_freq, upper_freq, step_size)
print(len(freq_rng))
