"""
#
# Jaracah Teague
# Apex - Final Project Visualization
# Appalachian State University
# 05/3/22
#
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import json
import time
import os

# read json lines file into a pandas dataframe
filename = 'final_apex_data.jl'
df = pd.read_json(filename, lines=True)

# cleaning
# remove all commas from the dataframe columns
df = df.replace(',','', regex=True)
# clean mmr column to remove RP
# convert other columns to floats for plotting
df['br_mmr'] = df['br_mmr'].str.rstrip('RP')
df['br_mmr']= df['br_mmr'].astype(float)
df['level'] = df['level'].astype(float)
df['kills'] = df['kills'].astype(float)

df.to_csv('final_apex_data.csv')

# data = sns.load_dataset('final_apex_data.csv')
x  = sns.jointplot(data=df, x='br_mmr', y='level', kind='reg')
# sns.lmplot(x="br_mmr", y="level", data=df, ax=ax_joint);

x1 = sns.jointplot(data=df, x='br_mmr', y='kills', kind='reg')
x2 = sns.jointplot(data=df, x='level', y='kills', kind='reg')

# create matplotlib plots
fig, axs = plt.subplots(nrows=1, ncols=4, gridspec_kw={'width_ratios': [1, 1, 1, 1]})
fig=plt.figure(1)

# (1) most frequently used legends 
axs[0] = df.groupby('legend').legend.count().plot.bar(ax=axs[0], color="Purple")
axs[0].set_title("Legend Usage")
fig=plt.figure(1)

# (2) MMR v Level
axs[1] = df.plot.scatter(x='br_mmr', y='level', ax=axs[1], color="Orange")
axs[1].set_title("MMR v Level")
fig=plt.figure(1)

# (3) Level v Kills
axs[2] = df.plot.scatter(x='level', y= 'kills', ax=axs[2], color="Red")
axs[2].set_title("Level v Kills")
fig=plt.figure(1)

# (4) MMR v Kills
axs[3] = df.plot.scatter(x='br_mmr', y= 'kills', ax=axs[3], color="Blue")
axs[3].set_title("MMR vs Kills")
fig=plt.figure(1)

fig.suptitle("Apex Legends Top 1000 Player Statistics (cross-platform)", fontsize=16)
fig.tight_layout()

plt.show()
