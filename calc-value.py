#!/usr/bin/python

"""
Calculate the sum of KPI adjusted values from a table.
"""

import sys,re
import dateutil.parser
import KPI

# Labels to print
labels = ['G','P','S']

# What column contains the date
date_col = 0

# The three columns to summarize
vcols = [2,3,4]

# Create object for querying the kpi database
kpidb = KPI.KPI()
kpi_today = kpidb.get_latest_kpi()

# Initial empty sums
sums = [0]*len(vcols)
kpi_sums = [0]*len(vcols)

# Open the txt files with the original table
text_file = open(sys.argv[1])
for line in text_file:
    # Is it a table line?
    if not re.search(r'^\|',line):
        continue

    # Split the columns on the vertical bar and get rid of first colmn
    cols = line.split('|')[1:]

    # Get rid of whitespace
    date_string = re.sub(' ','',cols[date_col])

    # Does it look like date? If not continue.
    if not re.search('^\d+',date_string):
        continue

    # Does it contain a dash? If so, let dateutil parse it and get the
    # monthly kpi.
    if re.search('-',date_string):
        date = dateutil.parser.parse(date_string)
        kpi = kpidb.get_monthly(date.year,date.month-1)

    # otherwise it's a year and we get the yearly average
    else:
        kpi = kpidb.get_yearly(int(date_string))

    # loop over vcols and calculate
    for i,vi in enumerate(vcols):
        # Get rid of (?) in the columns
        v = re.sub(r'\(\?\)','',
                   re.sub(' ','',cols[vi]))

        # Check if we have an entry for the column
        if len(v):
            v=float(v)
            # Sum column
            sums[i]+= v
            # kpi adjust and sum the column
            kpi_sums[i]+= kpi_today/kpi*v

def ary_fmt(v, fmt="%10.0f",sep=' | '):
    """Pretty print an array"""
    return sep.join([fmt%f for f in v])

print "        | ",ary_fmt(labels,fmt='       %-3s')
print "--------+-"+"+".join(["-"*12]*3)
print "sums    | ",ary_fmt(sums)
print "kpi_sum | ",ary_fmt(kpi_sums)
