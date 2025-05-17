import argparse
import inflect
import math
import numpy as np
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--mean', default='0.00037829')
parser.add_argument('--stdev', default='0.0125988158')
parser.add_argument('--days', default='21')
parser.add_argument('--num_sims', default='1000000')
args=parser.parse_args()

mean = float(args.mean)
stdev = float(args.stdev)
period = int(args.days)
num_sims = int(args.num_sims)

random_moves = np.random.normal(loc=mean, scale=stdev, size=(num_sims, period))

stock_multipliers = np.prod(1 + random_moves, axis=1)
stock_paths = np.cumprod(1 + random_moves, axis=1)
stock_paths = np.hstack([np.ones((stock_paths.shape[0], 1)), stock_paths])
stock_highs = np.max(stock_paths, axis=1)
stock_lows = np.min(stock_paths, axis=1)

import inflect
engine = inflect.engine()

def print_percentiles(data, label):
    print(f"# {label}")
    for p in [0.1, 1, 2.5, 5, 10, 20, 30, 50, 70, 80, 90, 95, 97.5, 99, 99.9]:
        val = np.percentile(data, p)
        print(f"{engine.ordinal(p)} percentile: {val}")
    print("")

print_percentiles(stock_multipliers, "Stock")
print_percentiles(stock_highs, "Stock highs")
print_percentiles(stock_lows, "Stock lows")
