#!/usr/bin/env python3

import argparse
import glob
import json
import os
import datetime
import matplotlib.pyplot as plt

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# store daily counts for each hashtag
data = {hashtag: {} for hashtag in args.hashtags}

# scan through daily language output files
for path in sorted(glob.glob('outputs/*.lang')):
    filename = os.path.basename(path)

    # skip the aggregate file
    if filename == 'total.lang':
        continue

    # extract date from filename
    date_part = filename.split('20-')[1].split('.zip')[0]
    month, day = map(int, date_part.split('-'))

    # convert date to day of year
    day_of_year = datetime.date(2020, month, day).timetuple().tm_yday

    # load daily counts
    with open(path) as f:
        counts = json.load(f)

    # record each hashtag's daily total
    for hashtag in args.hashtags:
        data[hashtag][day_of_year] = sum(
            counts.get(hashtag, {}).values()
        )

# create line plot
plt.figure(figsize=(10, 6))

for hashtag in args.hashtags:
    days = sorted(data[hashtag])
    values = [data[hashtag][day] for day in days]

    plt.plot(
        days,
        values,
        linewidth=2,
        marker='.',
        markersize=3,
        label=hashtag
    )

plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.title('Daily Coronavirus Hashtag Usage')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# save graph
plt.savefig('alternative_reduce.png', dpi=200)
plt.close()
