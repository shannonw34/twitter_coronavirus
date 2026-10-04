#!/bin/bash

for file in "/data/Twitter dataset/"*20-*.zip
do
    nohup python3 src/map.py --input_path "$file" --output_folder outputs &
done
