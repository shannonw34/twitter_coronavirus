#!/usr/bin/env python3

# command line args
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
import glob
import matplotlib.pyplot as plt

# scan through all daily language output files
data = {hashtag: {} for hashtag in args.hashtags}

for path in sorted(glob.glob('outputs/*.lang')):
    filename = os.path.basename(path)

    # skip the total/reduced file
    if filename == 'total.lang':
        continue

    # extract month and day from filenames such as:
    # geoTwitter20-01-08.zip.lang
    date_part = filename.split('20-')[1].split('.zip')[0]
    month, day = map(int, date_part.split('-'))

    # convert month/day to day of year
    import datetime
    day_of_year = datetime.date(2020, month, day).timetuple().tm_yday

    # load daily counts
    with open(path) as f:
        counts = json.load(f)

    # save the count for each requested hashtag
    for hashtag in args.hashtags:
        count = sum(counts.get(hashtag, {}).values())
        data[hashtag][day_of_year] = count

# plot one line for each hashtag
for hashtag in args.hashtags:
    days = sorted(data[hashtag])
    values = [data[hashtag][day] for day in days]
    plt.plot(days, values, label=hashtag)

plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.legend()
plt.tight_layout()

# save the graph
output_path = 'alternative_reduce.png'
plt.savefig(output_path)
