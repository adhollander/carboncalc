# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 09:54:08 2014
Script for producing biomass and CO2 sequestration results from John de Goede
data tables.

@author: adh
"""

import growth, biomass
import sys

FIAdata = False

f = sys.stdin
fout = sys.stdout
lines = f.readlines()
header = lines[0].strip()
fout.write("%s,biomass,CO2sequestered\n" % header) 
for line in lines[1:]:
    larr = line.split(',')
    climatezone = larr[0].strip().replace('\"','')
    if FIAdata:
        speccode = larr[5].strip().replace('\"','')
        dbh = float(larr[6])
        height = float(larr[7])
    else:
        speccode = larr[4].strip().replace('\"','')
        dbh = float(larr[5])
        height = float(larr[6])
    #print speccode,climatezone,dbh,height
    fout.write("%s," % (line.strip()))
    try:
         treebiomass = biomass.biomass_calc(biomass.dbconn,speccode, climatezone, dbh, height, useminmax=True, negcorrect=True)[0]
    except Exception, e:
         treebiomass = e
    try:
         CO2seq = str(growth.biomass_diff2(biomass.dbconn, speccode, climatezone, dbh, height)[2])
    except Exception, e:
         CO2seq = e
    #treebiomass = biomass.biomass_calc(biomass.dbconn,speccode, climatezone, dbh, height)[0]
    #CO2seq = growth.biomass_diff2(growth.dbconn, speccode, climatezone, dbh, height)
    fout.write("%s,%s\n" % (treebiomass, CO2seq))
    #print biomass
    #fout.write("%f\n" % float(treebiomass))
