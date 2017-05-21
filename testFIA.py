# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 16:43:34 2014

@author: adh

Reads FIA_biomass.csv file and runs biomass calculations across it.
"""

import biomass
import csv

regiondict = {'CenFla': 'Central Florida', 'GulfCo': 'Coastal Plain', 'InlEmp': 'Inland Empire',
              'InlVal': 'Inland Valleys', 'InterW': 'Interior West', 'LoMidW': 'Lower Midwest',
              'MidWst': 'Midwest', 'NoCalC': 'Northern California Coast', 'NMtnPr': 'North',
              'NoEast': 'Northeast', 'PacfNW': 'Pacific Northwest', 'Piedmt': 'South',
              'SoCalC': 'Southern California Coast', 'SWDsrt': 'Southwest Desert',
              'TpIntW': 'Temperate Interior West', 'Tropic': 'Tropical'}
              
regioninvdict = dict((v,k) for k, v in regiondict.iteritems())

outfile = '/home/adh/UrbanForests/FIA/FIA_biomass.csv'
fout = open(outfile, 'w')
writer = csv.writer(fout)
dbconn = biomass.dbconn
with open('/home/adh/UrbanForests/FIA/FIA_toRun.csv', 'rb') as f:
    reader = csv.reader(f)
    header = reader.next() # skip header
    writer.writerow(header + ["biomass", "carbon", "co2"])
    for row in reader:
        speccode = row[10]
        climzone = row[1]
        dbh = float(row[8])
        height = float(row[9])
        (biomassval, carbon, co2) = biomass.biomass_calc(dbconn, speccode, regioninvdict[climzone], dbh, height, useminmax=True)
        #print speccode, climzone, dbh, height, biomassval, carbon, co2
        writer.writerow(row + [biomassval, carbon, co2])
fout.close()
