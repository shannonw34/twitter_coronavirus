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

# use a font that supports Korean characters
plt.rcParams['font.family'] = ['UnDotum']

fig, ax1 = plt.subplots(figsize=(10, 6))

# first hashtag on left y-axis
hashtag1 = args.hashtags[0]
days1 = sorted(data[hashtag1])
values1 = [data[hashtag1][day] for day in days1]

ax1.plot(
    days1,
    values1,
    marker='.',
    markersize=3,
    linewidth=2,
    label=hashtag1
)

ax1.set_xlabel('Day of Year')
ax1.set_ylabel(hashtag1)

# second hashtag on right y-axis
if len(args.hashtags) > 1:
    hashtag2 = args.hashtags[1]
    days2 = sorted(data[hashtag2])
    values2 = [data[hashtag2][day] for day in days2]

    ax2 = ax1.twinx()

    ax2.plot(
        days2,
        values2,
        marker='.',
        markersize=3,
        linewidth=2,
        label=hashtag2
    )

    ax2.set_ylabel(hashtag2)

# title and grid
ax1.set_title('Daily Coronavirus Hashtag Usage')
ax1.grid(True, alpha=0.3)

# combine legends
lines1, labels1 = ax1.get_legend_handles_labels()

if len(args.hashtags) > 1:
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
else:
    ax1.legend()

plt.tight_layout()
plt.savefig('alternative_reduce.png', dpi=200)
plt.close()
