#!/usr/bin/env bash
# Run all script to generate the results presented in the paper "On Fading
# Channel Dependency Structures with a Positive Zero-Outage Capacity" (Karl-L.
# Besser, Pin-Hsun Lin, Eduard Jorswieck, IEEE Transactions on Communications,
# vol. 69, no. 10, pp. 6561-6574, Oct 2021.)
#
# Copyright (C) 2021 Karl-Ludwig Besser
# License: GPLv3

echo "Running boundary example"
python boundary.py --plot --export -x 8 -y 0

echo "Running Rayleigh fading example"
python rayleigh_fading.py --plot --export -x 0 5 0 -5 -5 -y 0 5 5 5 10

echo "Running MRC script..."
python3 maximum_ratio_combining.py --plot --export -s 0 -m 5

echo "Running SC script..."
python3 selection_combining.py --plot --export -s 10 -m 2 5 10
