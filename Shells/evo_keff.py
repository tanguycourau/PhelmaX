#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

def read_fmt(filename):
    """Reading data produced by FMT: DRAGON module
    Time, Keff, isotopic densities
    """
    if not os.path.exists(filename):
        raise FileNotFoundError('evo_keff.py: File '+filename+' not found')
    with open(filename, 'r') as fh:
        strg = fh.read()
    for keyword in ['Time', 'Keff', 'Den']:
        if keyword not in strg:
            raise AssertionError('evo_keff.py: keyword '+keyword+' not found in '+filename)

    match = re.findall(r'(^\w+\s+|^\w+\s+\([:,\s+\d+]+\))=([^;]+);', strg, re.M+re.S) #keyword|keyword ( : , 1) = [xxx yyyy];
    df = pd.DataFrame()
    for (key, vals) in match:
        if 'zeros' not in vals: ## we delete lines as  DenU235 = zeros(32,3)
            if key.startswith('Den'):
                key='_'.join(key[3:-1].split()[0:3:2]) ## we replace DenU235    (:,   1) by U235_1
            else:
                key=key.strip()  # we replace 'Keff |Time ' by 'Keff|Time'
            df = pd.concat([df, pd.DataFrame(np.fromstring(vals[1:-1], sep=' '), columns=[key])], axis=1)
    return df


parser = argparse.ArgumentParser(description='Plot keff versus time')
parser.add_argument('filename', help='input filename(s) of FMT type', nargs='+')
parser.add_argument('-l', '--legend',  help='legend labels', default=None, nargs='+')
parser.add_argument('-o', '--output', help='Output file name (default evo_keff.pdf)', default='evo_keff.pdf')
parser.add_argument('-d', '--data', help='Data storage file name (default evo_keff.csv)', default='evo_keff.csv')

args = parser.parse_args()
if not isinstance(args.filename, list):
    args.filename = [args.filename]
df = pd.DataFrame()
for filename in args.filename:
    dfmt = pd.concat([read_fmt(filename)[['Time', 'Keff']]], axis=1, keys=[filename])
    df = pd.concat([df, dfmt], axis=1)

## Begining of plot
plt.xlabel('time (days)')
plt.ylabel('K-effective')
plt.grid()

for filename in args.filename:
    plt.plot(df[filename]['Time'], df[filename]['Keff'], label=filename)

if args.legend is not None:
    plt.legend(args.legend)
else:
    plt.legend()
plt.savefig(args.output)
df.to_csv(args.data, index=False)
print('output file: '+args.output)
print('data file: '+args.data)
print("reload dataframe\n> pd.read_csv('"+args.data+"', header=[0, 1])")
os.popen('evince '+args.output+'&')
