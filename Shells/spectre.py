#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

def read_edit(filename):
    """Read data from EDIT type DRAGON filename
    filename : input file containing 'ENERGY', 'DELTAU',
               and 'FLUX-INTG' data
    return dataframe with flux averaged in lethargy
    """
    if not os.path.exists(filename):
        raise FileNotFoundError('spectre.py: File '+filename+' not found')
    print('reading', filename)
    with open(filename, 'r') as fh:
        strg=fh.read()
    for keyword in ['TIMESTAMP', 'ENERGY', 'DELTAU', 'FLUX-INTG']:
        if keyword not in strg:
            raise AssertionError('spectre.py: keyword '+keyword+' not found in '+filename)

    keyword = 'TIMESTAMP'
    match = re.findall(r'^'+keyword+r'\s+([^>]+)\s->', strg, re.M+re.S)
    timestamp = np.array([m.split() for m in match]).astype(float)
    timesteps = timestamp.shape[0]

    keyword = 'ENERGY'
    match = re.search(r'^'+keyword+r'\s+([^>]+)\s->', strg, re.M+re.S)
    energy = np.array(match[1].split()).astype(float)

    keyword = 'DELTAU'
    match = re.search(r'^'+keyword+r'\s+([^>]+)\s->', strg, re.M+re.S)
    deltau = np.array(match[1].split()).astype(float)

    keyword = 'FLUX-INTG'
    match = re.findall(r'^'+keyword+r'\s+([^>]+)\s->', strg, re.M+re.S)
    flux = np.array(match).astype(float).reshape(timesteps, -1)

    flxar  = np.zeros((2*energy.size-2, 1+timestamp.shape[0]))
    flxar[0, 0] = energy[0]
    flxar[-1, 0] = energy[-1]
    flxar[1:-1, 0] = np.array([[e, e] for e in energy[1:-1]]).ravel()
    for time in range(1, 1+timestamp.shape[0]):
        flxnorm = flux[time-1]/deltau/flux[time-1].sum()
        # we duplicate data along energy axis
        flxar[:, time] =  np.array([[f, f] for f in flxnorm]).ravel()
    columns = ['e']+list(timestamp[:,0])
    df = pd.concat([pd.DataFrame(flxar, columns=columns)], axis=1, keys=[filename])
    return df

parser = argparse.ArgumentParser(description='Plot flux spectrum averaged in lethargy')
parser.add_argument('filename', help='input filename(s) of edit type', nargs='+')
parser.add_argument('-t', '--timestep', type=int, help='timestep(s)', default=1, nargs='+')
parser.add_argument('-l', '--legend',  help='legend labels', default=None, nargs='+')
parser.add_argument('-o', '--output', help='Output file name (default spectre.pdf)', default='spectre.pdf')
parser.add_argument('-d', '--data', help='Data storage file name (default spectre.csv)', default='spectre.csv')

args = parser.parse_args()
if not isinstance(args.filename, list):
    args.filename = [args.filename]
if not isinstance(args.timestep, list):
    args.timestep = [args.timestep]
if len(args.filename)>1 and len(args.timestep)>1 :
    parser.error('impossible to deal with several inputfiles and several timesteps at the same time')
df = pd.DataFrame()
for filename in args.filename:
    flxar = read_edit(filename)
    df = pd.concat([df, flxar], axis=1)

## Begining of plot
plt.xlabel('E (eV)')
plt.ylabel('Averaged flux in lethargy')
plt.xscale('log')
plt.xlim([1.0e-3, 1.0e8])


if len(args.filename)>=1 and len(args.timestep)==1:
    for filename in args.filename:
        dfp = df[filename].iloc[:, [0, args.timestep[0]]]
        label = filename+' t (days) = '+str(dfp.columns[1])
        plt.plot(dfp['e'], dfp.iloc[:, 1], label=label)
elif  len(args.filename)==1 and len(args.timestep)>1:
    for step in args.timestep:
        dfp = df[filename].iloc[:, [0, step]]
        label = filename+' t (days) = '+str(dfp.columns[1])
        plt.plot(dfp['e'], dfp.iloc[:, 1], label=label)

if args.legend is not None:
    plt.legend(args.legend)
else:
    plt.legend()

plt.savefig(args.output)
df.to_csv(args.data, index=None)
print('output file: '+args.output)
print('datafile: '+args.data)
print("reload dataframe\n> pd.read_csv('"+args.data+"', header=[0, 1])")
if args.output.endswith('pdf'):
    os.popen('evince '+args.output+'&')
