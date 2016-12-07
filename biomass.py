# -*- coding: utf-8 -*-
"""
Biomass Urban Forestry calculator.

Calculates biomass, carbon, and equivalent CO2 for a tree given the species,
region, dbh, and height.
"""
import sqlite3
from math import exp, log, log10

import growth

# alter depending on install path.
UrbForDB = "/home/adh/UrbanForests/UrbanForestCC.sqlite" 

roots = 0.78
carbon_fraction = 0.5
co2_fraction = 3.67

dbconn = sqlite3.connect(UrbForDB)


# in the below how do I handle TypeError: 'NoneType' object is not iterable?

def equation_dw12(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form: a * (dbh^b) * c. """
    qstr = "SELECT a, b FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b) = coeffs
    biomass =  float(a) * (dbh** float(b))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)

def equation_dw13(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form:  (a*ht+b)+(c*ht+d) """
    qstr = "SELECT a, b, c, d FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d) = coeffs
    biomass =  float(a) * ht + float(b) + float(c1) * ht + float(d)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)

def equation_dw14(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form:  (exp(a+b*(ln(dbh)))+exp(c+d*(ln(dbh))) """
    qstr = "SELECT a, b, c, d FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d) = coeffs
    biomass =  exp(float(a) + float(b) * log(dbh)) + exp(float(c1) + float(d) * log(dbh))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)

def equation_dw15(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form:  (exp(a+b*ln(dbh)))*c """
    qstr = "SELECT a, b FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b) = coeffs
    biomass = exp(float(a) + float(b) * log(dbh))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)

def equation_dw16(dbconn, speccode, biomassassign, dbh, ht):
    """  Equation form: a^(b+c*(log10(dbh^d))) """
    qstr = "SELECT a, b, c, d FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d) = coeffs
    biomass =  float(a) ** (float(b) + float(c1) * log10(dbh ** float(d)))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_dw18(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form: ((a + b * dbh + c * (dbh ^ d))-(e + f * dbh + g * (dbh ^ h))) """
    qstr = "SELECT a, b, c, d, e, f, g, h FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d, e, f, g, h) = coeffs
    biomass =  float(a) + float(b) * dbh + float(c1) * (dbh ** float(d)) - (float(e) + float(f) * dbh  + float(g) * (dbh ** float(h)))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_dw19(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form:  a*((SGsp)dbh^2*ht)^c where SGsp = specific gravity for species."""
    qstr = "SELECT a, c FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, c1) = coeffs
    qstr = "SELECT DWDensity FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    c.execute(qstr)
    (density,) = c.fetchone()
    biomass =  float(a) * ((float(density)/1000.0) * (dbh ** 2) * ht) ** float(c1)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_dw20(dbconn, speccode, biomassassign, dbh, ht):
    """ Equation form:  exp(a+b*log(dbh))-exp(c+(d/dbh)) """
    qstr = "SELECT a, b, c, d FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d) = coeffs
    biomass =  exp(float(a) + float(b) * log(dbh)) - exp(float(c1) + float(d)/dbh)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_dw21(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form:  a*(dbh^b)-(exp(c+(d/dbh)) """
    qstr = "SELECT a, b, c, d FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d) = coeffs
    #print "coeffs: ", a, b, c1, d
    biomass =  float(a) * (dbh ** float(b)) - exp(float(c1) + float(d)/dbh)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_dw22(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form:  exp(a+b*ln(dbh)) """
    qstr = "SELECT a, b FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b) = coeffs
    biomass =  exp(float(a) + float(b) * log(dbh))
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)

def equation_dw23(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form: exp(a+b*ln(dbh)+c*ln(ht)+d*ln(e/f) """
    qstr = "SELECT a, b, c, d, f FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d, f) = coeffs
    qstr = "SELECT DWDensity FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    c.execute(qstr)
    (density,) = c.fetchone()
    biomass = exp(float(a) + float(b) * log(dbh) + float(c1) * log(ht) + float(d) * log(float(density)/float(f)) )
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_fw1(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form:  a*(dbh)^b """
    qstr = "SELECT a, b FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b) = coeffs
    qstr = "SELECT DWDensity FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    c.execute(qstr)
    (density,) = c.fetchone()
    biomass =  float(a) * (dbh ** float(b)) * (float(density)/1000.0)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_vol10(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form:  a*dbh^b*ht^c """
    qstr = "SELECT a, b, c FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1) = coeffs
    qstr = "SELECT DWDensity FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    c.execute(qstr)
    (density,) = c.fetchone()
    biomass = float(a) * (dbh ** float(b)) * (ht ** float(c1))  * float(density)
    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
def equation_vol11(dbconn, speccode, biomassassign, dbh, ht):
    """Equation form:  a(b*(dbh/c)^d*(e*ht)^f) """
    qstr = "SELECT a, b, c, d, e, f FROM VolBioCoeffs WHERE SpecCode = '%s'" % (biomassassign)
    c = dbconn.cursor()
    c.execute(qstr)
    coeffs = c.fetchone()
    (a, b, c1, d, e, f) = coeffs
    qstr = "SELECT DWDensity FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    c.execute(qstr)
    (density,) = c.fetchone()
   # biomass = float(a) * (float(b) * (dbh/float(c1)) ** float(d)) * (float(e) * (ht ** float(f)))  * float(density)
# JdG correction below.
    biomass = float(a) * (float(b) * (dbh/float(c1)) ** float(d)) * ((float(e) * ht) ** float(f))  * float(density)

    carbon = carbon_fraction * biomass / roots
    co2 = carbon * co2_fraction
    return (biomass, carbon, co2)
    
eqn_lookup = {'dw12': equation_dw12, 'dw13': equation_dw13, 'dw14': equation_dw14, 
              'dw15': equation_dw15, 'dw16': equation_dw16, 'dw18': equation_dw18, 
              'dw19': equation_dw19, 'dw20': equation_dw20, 'dw21': equation_dw21,
              'dw22': equation_dw22, 'dw23': equation_dw23, 'fw1': equation_fw1,
              'vol10': equation_vol10, 'vol11': equation_vol11}
              
minmaxtypedict = {'dw12': 'dbh', 'dw13': 'ht', 'dw14': 'dbh', 
              'dw15': 'dbh', 'dw16': 'dbh', 'dw18': 'dbh', 
              'dw19': 'dbh', 'dw20': 'dbh', 'dw21': 'dbh', # dw19, dw23, vol10, vol11 both
              'dw22': 'dbh', 'dw23': 'dbh', 'fw1': 'dbh',
              'vol10': 'dbh', 'vol11': 'dbh'}

def biomass_calc(dbconn, speccode, region, dbh=0, ht=0, useminmax=False, negcorrect=False):
    """Calculate biomass, carbon, and CO2 equivalent given tree data.
    
    Args:
    dbconn - database connection handle
    speccode - species code
    region - region code
    dbh - tree dbh in cm
    ht - tree height in m
    useminmax - flag to limit dbh or height over which equations are applicable
    negcorrect - iteration correction upwards if calculated biomass < 0
    
    Returns:
    biomass - biomass of tree in kg
    carbon - carbon stored by tree in kg
    co2 - CO2 equivalent of tree biomass
    """
    #qstr = "SELECT BiomassEqn FROM SpeciesCodeList WHERE SpeciesCode = '%s'" % (speccode)
    qstr = "SELECT b.EqnName, b.SpecCode FROM SpeciesCodeList a, VolBioCoeffs b WHERE a.BioMassAssign = b.SpecCode AND a.SpeciesCode = '%s' AND a.Region = '%s'" % (speccode, region)
    c = dbconn.cursor()
    c.execute(qstr)
    qresult = c.fetchone()
    (eqn, biomassassign) = qresult
    if useminmax:
        minmaxtype = minmaxtypedict[eqn]
        growthspecies = growth.growth_calc_species(dbconn, speccode, region)
#        qstr = "SELECT AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s'" % (growthspecies, region)
        if minmaxtype == 'dbh':
            qstr = "SELECT AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'd.b.h.'" % (growthspecies, region)
        else:
            qstr = "SELECT AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'tree ht'" % (growthspecies, region)
        c.execute(qstr)
        qresult = c.fetchone()
        (appsmin, appsmax) = qresult
        #print appsmin, appsmax
        appsmin = float(appsmin)
        appsmax = float(appsmax)
        if minmaxtype == 'dbh':
            if dbh < appsmin:
                dbh = appsmin
            elif dbh > appsmax:
                dbh = appsmax
        else:
            if ht < appsmin:
                ht = appsmin
            elif ht > appsmax:
                ht = appsmax 
    #print eqn, biomassassign
    (biomass, carbon, co2) = eqn_lookup[eqn](dbconn, speccode, biomassassign, dbh, ht)
# If biomass ends up negative in calculation, iterate upwards in terms of integral age until
# biomass no longer negative
    if negcorrect:
        if biomass < 0:
            testage = 0
            testbiomass = biomass
            while testbiomass < 0:
                (testsizeval, testtype) = growth.inv_age_calc(dbconn, speccode, region, testage)
                if testsizeval < appsmin:
                    testsizeval = appsmin
                elif testsizeval > appsmax:
                    testsizeval = appsmax
                if testtype == 'dbh':
                    (testbiomass, testcarbon, testco2) = eqn_lookup[eqn](dbconn, speccode, biomassassign, testsizeval, ht)
                else:
                    (testbiomass, testcarbon, testco2) = eqn_lookup[eqn](dbconn, speccode, biomassassign, dbh, testsizeval)
                testage += 1
            biomass = testbiomass
            carbon = testcarbon
            co2 = testco2
            
    return (biomass, carbon, co2)
