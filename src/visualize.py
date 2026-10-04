#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# get the country/language counts
items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]), reverse=True)[:10]

# sort the top 10 from low to high
items = sorted(items, key=lambda item: item[1])

# create bar graph
keys = [item[0] for item in items]
values = [item[1] for item in items]

plt.bar(keys, values)
plt.xlabel('Key')
plt.ylabel('Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# save graph as png
output_path = args.input_path + '_' + args.key.replace('#', '') + '.png'
plt.savefig(output_path)
