    
"""
    Developer:           Rusif Eyvazli
    Date:                07/24/2019
    Project link:        https://rusife.github.io/Performance-Analysis-for-Network-Storage/
    Learn more about me: https://www.linkedin.com/in/rusifeyvazli/
    Contact:             eyvazlirusif@gmail.com
    
    Program name:        Performance Analysis for Network Storage
    Purpose:             Using this Python program you can graph a line plot using the data that 
                         has special pattern from a data file that's mixed up with other notes. 
    
    Copyright (C) <2019>  <Rusif Eyvazli>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg') #backend option for matplotlib
import matplotlib.pyplot as plt
import re # for grabbing a part of the file name
from textwrap import wrap # wrapping the title
import argparse # for optional arguments
parser = argparse.ArgumentParser()

#('arg_name', nargs='?' means optional arg., help="Help message when we run 'python name.py -h'")
parser.add_argument('File_Name', help="Enter the file name to graph it | At least one file is required to graph")
parser.add_argument('-title',nargs='?', help="Overwrites the current title")
parser.add_argument('-width',nargs='?', help="Overwrites the current lines' widths")
args=parser.parse_args()

# Key columns:
# c0 = read, c1 = seq, Names, Time, l=labels
colnames=['c0','c1','c2','c3','c4','c5',
          'Names','c7','c8','c9','c10','c11',
          'c12','c13','c14','15','c16','c17',
          'Time','c19','c20','c21','l']

# Key categories drived from last column.
# It is used to filter the data and to create new markers for each name.
categories = ['1G-a','1G-b','10G-a']

# Opens the file and graphs it.
fileN = args.File_Name
with open (fileN) as file:
    # Reads the file and assigns the columns to the header.
    data_i = pd.read_csv(file,names=colnames,sep=' ',header=None)
    #print(data_i)
    
# Creates data frame with column names. Then filters iy by Column 0 and 1, then by last column.
df =  pd.DataFrame(data_i, columns=colnames)
df = df.loc[(df['c0'] == 'read') & (df['c1'] == 'seq' )]
df = df.loc[df['l'].isin(categories)]

# Below creates and returns a dictionary of category-point combinations,
# by cycling over the marker points specified.
points = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*','H', 'D', 'd', 'P', 'X']
mult = len(categories) // len(points) + (len(categories) % len(points) > 0)
markers = {key:value for (key, value)
           in zip(categories, points * mult)} ; markers

# Below, the data only from three columns is assigned to df data frame.
header = ['Names','Time','l']
df = pd.DataFrame(df, columns = header)

# Sorts the data frame by column "Names".
df.Names = df.Names.astype(int)
df = df.sort_values(by=['Names'])

# Changes the data to match GB/Sec.
df.Time=df.Time.astype(int)
df.Time = df.Time/1000

# Sets (default) width of the lines and sets background style to white.
# If width specified as an arg. it overwrites width for the graph using '-width' argument.
sns.set(rc={"lines.linewidth": 0.3}, style='white')
if args.width:
    sns.set(rc={"lines.linewidth": args.width}, style='white')
    
# Setting new title. If title specified as an arg. it overwrites wrapped title for the graph using '-title' argument.
plt.title("Performance")
if args.title:
    plt.title("\n".join(wrap(args.title)), size = 12)
    
# Plot:
# 'hue' option is for each line's names (labels).
# 'style' is for applying markers.
sns.lineplot(data=df, x='Names', y='Time', hue='l', style='l', dashes=False,
             markers=markers, ci=None, err_style=None)

# Setting X and Y limits
plt.xlim(0, 60)
plt.ylim(0, 18)

# Labels for the axises:
plt.ylabel("Performance (GB/sec)")
plt.xlabel('Names')

# Gets the current axes object the figure is plotted on.
ax = plt.gca()
# Finds the handles/labels ax is associated with:
handles, labels = ax.get_legend_handles_labels()
# Re-sets the legend for the current axes.
ax.legend(handles=handles[1:], labels=labels[1:], title='', loc='best')

# Saves a PNG file of the current graph to the folder and updates it every time
# (nameOfimage, dpi=(sizeOfimage))
pic_name = re.split("[-]",fileN)[1]
plt.savefig(pic_name  + '-performance', dpi=(250), bbox_inches='tight')
# Hard coded name: './test.png'

# Shows the plot
plt.show()
