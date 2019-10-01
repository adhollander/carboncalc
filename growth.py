# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 13:06:05 2014

@author: adh

Urban forest calculator: Calculate carbon added in previous year.

"""

import biomass
import sqlite3
from numpy import exp, log, sqrt

from scipy.optimize import brentq, fsolve

UrbForDB = "/home/adh/UrbanForests/UrbanForestCC.sqlite"

roots = 1.00
carbon_fraction = 0.5
co2_fraction = 3.67

dbconn = sqlite3.connect(UrbForDB)

def equation_loglogw1(x, a, b, c, d, e):
    """Equation form for loglogw1 """
    return exp(a + b * log(log(x+1) + (c/2)))
    
def equation_loglogw2(x, a, b, c, d, e):
    """Equation form for loglogw2 """
    return exp(a + b * log(log(x+1)) + (sqrt(x) * (c/2)))
    
def equation_loglogw3(x, a, b, c, d, e):
    """Equation form for loglogw3 """
    return exp(a + b * log(log(x+1)) + x * c/2)
    
def equation_loglogw4(x, a, b, c, d, e):
    """Equation form for loglogw4 """
    return exp(a + b * log(log(x+1))+ x * x * c/2)
    
def equation_lin(x, a, b, c=0, d=0, e=0):
    """Equation form for lin """
    return a + b*x

def equation_quad(x, a, b, c, d=0, e=0):
    """Equation form for quad """
    return a + b*x + c*x*x
    
def equation_cub(x, a, b, c, d, e):
    """Equation form for cub """
    return a + b*x + c*x*x + d*x*x*x
    
def equation_quart(x, a, b, c, d, e):
    """Equation form for quart """
    return  a + b*x + c*x*x + d*x*x*x + e*x*x*x*x

def equation_expow1(x, a, b, c, d, e):
    """Equation form for expow1 """
    return exp(a + b*x + c/10)

def equation_expow2(x, a, b, c, d, e):
    """Equation form for expow2 """
    return  exp(a + b*x + sqrt(x)*c/2)
    
def equation_expow3(x, a, b, c, d, e):
    """Equation form for expow3 """
    return  exp(a + b*x + x*c/2)
    
def equation_expow4(x, a, b, c, d, e):
    """Equation form for expow4 """
    return  exp(a + b*x + x*x*c/2)
     
eqn_lookup = {'lin1/age^2': equation_lin, 'quad1/age^2': equation_quad, 
              'quad1/age': equation_quad, 'cub1/age^2': equation_cub,
              'loglogw1': equation_loglogw1, 'loglogw3': equation_loglogw3,
              'lin1/age': equation_lin, 'lin1/sqrtage': equation_lin,
              'quad1/sqrtdbh': equation_quad, 'loglogw2': equation_loglogw2,
              'quad1/dbh': equation_quad, 'loglogw4': equation_loglogw4,
              'quad1/dbh^2': equation_quad, 'lin1/dbh': equation_lin,
              'lin1/dbh^2': equation_lin, 'quart1/age': equation_quart,
              'lin1/sqrtdbh': equation_lin, u'lin1/sqrtdbh': equation_lin,
              'lin1': equation_lin, 'expow1': equation_expow1,
              'quad1': equation_quad, 'quad1/ht': equation_quad,
              'cub1/dbh^2': equation_cub, 'quad1/sqrht': equation_quad,
              'cub1/ht': equation_cub, 'expow2': equation_expow2,
              'cub1/dbh': equation_cub, 'cuborig1/sqrtage': equation_cub,
              'cub1/ht^2': equation_cub, 'cub1/sqrtht': equation_cub,
              'quad1/sqrtage': equation_quad, 'cub1/sqrtdbh': equation_cub,
              'cub1': equation_cub, 'cub1/age': equation_cub,
              'cub1/sqrtage': equation_cub, 'quadorig1/age': equation_quad,
              'quart1/sqrtht': equation_quart, 'expow4': equation_expow4,
              'expow3': equation_expow3, 'lin1/ht^2': equation_lin,
              'quad1/ht^2': equation_quad, 'lin1/ht': equation_lin,
              'quadorig1/sqrtht': equation_quad, 'cuborig1/sqrtht': equation_cub,
              'loglog1': equation_loglogw1}
              
eqsolver_lookup = {'lin1/age^2': 'brentq', 'quad1/age^2': 'fsolve', 
              'quad1/age': 'fsolve', 'cub1/age^2': 'fsolve',
              'loglogw1': 'brentq', 'loglogw3': 'brentq',
              'lin1/age': 'brentq', 'lin1/sqrtage': 'brentq',
              'quad1/sqrtdbh': 'fsolve', 'loglogw2': 'brentq',
              'quad1/dbh': 'fsolve', 'loglogw4': 'brentq',
              'quad1/dbh^2': 'fsolve', 'lin1/dbh': 'brentq',
              'lin1/dbh^2': 'brentq', 'quart1/age': 'fsolve',
              'lin1/sqrtdbh': 'brentq', u'lin1/sqrtdbh': 'brentq',
              'lin1': 'brentq', 'expow1': 'brentq',
              'quad1': 'fsolve', 'quad1/ht': 'fsolve',
              'cub1/dbh^2': 'fsolve', 'quad1/sqrht': 'fsolve',
              'cub1/ht': 'fsolve', 'expow2': 'brentq',
              'cub1/dbh': 'fsolve', 'cuborig1/sqrtage': 'fsolve',
              'cub1/ht^2': 'fsolve', 'cub1/sqrtht': 'fsolve',
              'quad1/sqrtage': 'fsolve', 'cub1/sqrtdbh': 'fsolve',
              'cub1': 'fsolve', 'cub1/age': 'fsolve',
              'cub1/sqrtage': 'fsolve', 'quadorig1/age': 'fsolve',
              'quart1/sqrtht': 'fsolve', 'expow4': 'brentq',
              'expow3': 'brentq', 'lin1/ht^2': 'brentq',
              'quad1/ht^2': 'fsolve', 'lin1/ht': 'brentq',
              'quadorig1/sqrtht': 'fsolve', 'cuborig1/sqrtht': 'fsolve',
              'loglog1': 'brentq'}

def root_form(fn, y0):
    """Returns rewritten equation fn to find root at y value y0"""
    def fn2(x, a=0, b=0, c=0, d=0, e=0):
        return fn(x, a, b, c, d, e) - y0
    return fn2
       
#def find_eqn_root(fn, y0, a, b, c, d, e, lower_bound, upper_bound):
#    fn2 = root_form(fn, y0)
#    x0 = brentq(fn2, args=(a, b, c, d, e), a=lower_bound, b=upper_bound)
#    return 
    
# Let's try a different solver.

def find_eqn_root(fn, y0, eqstr, a, b, c, d, e, lower_bound, upper_bound):
    """Finds root of equation fn at y value y0. """
    #tol = 0.001
    #step = 0.1
    fn2 = root_form(fn, y0)
    #if abs(fn2(lower_bound) < tol):
       # lower_bound = lower_bound - step
    #if abs(fn2(upper_bound) < tol):
       # upper_bound = upper_bound + step
    #print lower_bound, upper_bound
    #x0 = brentq(fn2, args=(a, b, c, d, e), a=lower_bound, b=upper_bound)
    # bloody hell. let's try making the solver dependent on the functional form.
    if eqsolver_lookup[eqstr] == 'fsolve':
        froots = fsolve(fn2, (lower_bound + upper_bound)/2, args=(a, b, c, d, e))
    #froots = fsolve(fn2, [lower_bound, upper_bound],args=(a, b, c, d, e))
    #print froots
        x0 = froots[0]
    else:
        x0 = brentq(fn2, args=(a, b, c, d, e), a=lower_bound, b=upper_bound) 
    return x0

def nfloat(s):
    """Return floating point value of s if possible, None if not"""
    if not s == None:
        try:
            return float(s)
        except ValueError:
            return None
    else:
        return None


def growth_calc_species(dbconn, speccode, region):
    """Returns species growth assignment type given species speccode and region code"""
    qstr = "SELECT GrowthAssign FROM SpeciesCodeList WHERE SpeciesCode = '%s' AND Region = '%s'" % (speccode, region)
    c = dbconn.cursor()
    c.execute(qstr)
    qresult = c.fetchone()
    (growthspecies0) = qresult
    growthspecies = growthspecies0[0]
    if "OTHER" in growthspecies:
        qstr = "SELECT GrowthAssign FROM SpeciesCodeList WHERE SpeciesCode = '%s' AND Region = '%s'" % (growthspecies, region)
        c.execute(qstr)
        qresult = c.fetchone()
        (growthspecies0) = qresult
        growthspecies = growthspecies0[0]
    return growthspecies
        
#==============================================================================
# def growth_calc_eqn(dbconn, speccode, region):
#     growthspecies = growth_calc_species(dbconn, speccode, region)
#     c = dbconn.cursor()
#     qstr = "SELECT EqName, a, b, c, d, e, AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'd.b.h.'" % (growthspecies, region)
#     c.execute(qstr)
#     qresult = c.fetchone()
#     if qresult:
#         (eqstr, a, b, c, d, e, AppsMin, AppsMax) = qresult
#         eqtype = 'dbh'
#     else:
#         qstr = "SELECT EqName, a, b, c, d, e, AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'tree ht'" % (growthspecies, region)
#         c.execute(qstr)
#         qresult = c.fetchone() 
#         (eqstr, a, b, c, d, e, AppsMin, AppsMax) = qresult
#         eqtype = 'tree ht'
#     return eqn_lookup[eqstr], eqtype, nfloat(a), nfloat(b), nfloat(c), nfloat(d), nfloat(e), nfloat(AppsMin), nfloat(AppsMax)
#==============================================================================
    
def growth_calc_eqn2(dbconn, speccode, region, comptype):
    """Returns equation form and parameters given species code and region."""
    growthspecies = growth_calc_species(dbconn, speccode, region)
    c = dbconn.cursor()
    if comptype == 'd.b.h.':
        qstr = "SELECT EqName, a, b, c, d, e, AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'd.b.h.'" % (growthspecies, region)
        c.execute(qstr)
        qresult = c.fetchone()
        (eqstr, a, b, c, d, e, AppsMin, AppsMax) = qresult
        eqtype = 'dbh'
    else:
        qstr = "SELECT EqName, a, b, c, d, e, AppsMin, AppsMax FROM GrowCoeffs WHERE SpecCode = '%s' AND Region = '%s' AND Component = 'tree ht'" % (growthspecies, region)
        c.execute(qstr)
        qresult = c.fetchone() 
        (eqstr, a, b, c, d, e, AppsMin, AppsMax) = qresult
        eqtype = 'tree ht'
    return eqn_lookup[eqstr], eqtype, eqstr, nfloat(a), nfloat(b), nfloat(c), nfloat(d), nfloat(e), nfloat(AppsMin), nfloat(AppsMax)
    
#==============================================================================
# def age_calc(dbconn, speccode, region, dbh, ht, rounded, lower_bound, upper_bound):
#     """Compute age given dbh or height. Calls function solving eqn that predict dbh|ht from age."""
#     (eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn(dbconn, speccode, region)
#     #print eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax
#     if eqtype == 'dbh':
#         age = find_eqn_root(eqn, dbh, a, b, c, d, e, lower_bound, upper_bound)
#     else:
#         age = find_eqn_root(eqn, ht, a, b, c, d, e, lower_bound, upper_bound)
#     if rounded:
#         age = int(age)
#     return age
#==============================================================================
    
def age_calc2(dbconn, speccode, region, dbh, ht, rounded, lower_bound, upper_bound, comptype):
    """Compute age given dbh or height. Calls function solving eqn that predict dbh|ht from age."""
    #print "lower bound:upper bound: ", lower_bound, upper_bound
    (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, comptype)
    #print eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax
    if eqtype == 'dbh':
        age = find_eqn_root(eqn, dbh, eqstr, a, b, c, d, e, lower_bound, upper_bound)
    else:
        age = find_eqn_root(eqn, ht, eqstr, a, b, c, d, e, lower_bound, upper_bound)
    #print "age_calc2 age: ", age
    if rounded:
        age = int(age)
    return age
    
#def biomass_diff(dbconn, speccode, region, dbh=0, ht=0, round=False, lower_bound=0, upper_bound=100):
#    """Return increase in biomass between current year and previous year."""
#    curr_age = age_calc(dbconn, speccode, region, dbh, ht, round, lower_bound, upper_bound)
#    curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh, ht)
#    prev_age = curr_age - 1
#    print "Ages: ", curr_age, prev_age
#    (eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn(dbconn, speccode, region)
#    if eqtype == 'dbh':
#        if round:
#            curr_dbh = eqn(curr_age, a, b, c, d, e)
#            curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=curr_dbh, ht=0)
#        prev_dbh = eqn(prev_age, a, b, c, d, e)
#        # Let's deal with case where previous dbh is negative.
#        if prev_dbh <= 0:
#            prev_dbh = AppsMin
#        prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=prev_dbh, ht=0)
#    else:
#        if round:
#            curr_ht = eqn(curr_age, a, b, c, d, e)
#            curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=curr_ht)
#        prev_ht = eqn(prev_age, a, b, c, d, e)
#        if prev_ht <= 0:
#            prev_ht = AppsMin
#        prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=prev_ht)
#    print curr_biomass
#    print prev_biomass
#    # the results table sets the CO2 sequestration to the carbon stored in this minimum limiting case.
#    if abs(curr_biomass[0] - prev_biomass[0]) <= 1e-02:
#        return (curr_biomass[0], curr_biomass[1], curr_biomass[2])
#    else:
#        return (curr_biomass[0]-prev_biomass[0], curr_biomass[1]-prev_biomass[1], curr_biomass[2]-prev_biomass[2])

# now fiddling with new min/max age table        
#==============================================================================
# def biomass_diff(dbconn, speccode, region, dbh=0, ht=0, rounded=False, lower_bound=0, upper_bound=100):
#     """Return increase in biomass between current year and previous year."""
#     c = dbconn.cursor()    
#     qstr = "SELECT AppsMin, AppsMax, AppsMinAge, AppsMaxAge FROM GrowCoeffsMinMAX WHERE SpecCode = '%s' AND Region = '%s'" % (speccode, region)
#     c.execute(qstr)
#     qresult = c.fetchone()
#     (appsmin, appsmax, appsminage, appsmaxage) = qresult
#     curr_age = age_calc(dbconn, speccode, region, dbh, ht, rounded, appsminage, appsmaxage)
#     curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh, ht)
#     prev_age = curr_age - 1
#     #print "Ages: ", curr_age, prev_age
#     (eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn(dbconn, speccode, region)
#     if eqtype == 'dbh':
#         if rounded:
#             curr_dbh = eqn(curr_age, a, b, c, d, e)
#             curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=curr_dbh, ht=0)
#         prev_dbh = eqn(prev_age, a, b, c, d, e)
#         # Let's deal with case where previous dbh is negative.
#         # Nope. Let's use age as the criteriod.
#         if curr_age <= appsminage or prev_age < appsminage:
#             prev_dbh = AppsMin
#         else:
#             prev_dbh = eqn(prev_age, a, b, c, d, e)
#         prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=prev_dbh, ht=0)
#     else:
#         if rounded:
#             curr_ht = eqn(curr_age, a, b, c, d, e)
#             curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=curr_ht)
#         prev_ht = eqn(prev_age, a, b, c, d, e)
#         if curr_age <= appsminage or prev_age < appsminage:
#             prev_ht = AppsMin
#         else:
#             prev_ht = eqn(prev_age, a, b, c, d, e)
#         prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=prev_ht)
#     #print curr_biomass
#     #print prev_biomass
#     # the results table sets the CO2 sequestration to the carbon stored in this minimum limiting case.
#     # not quite -- if prev_biomass fails (negative age e.g.), the calc blows up
#     if abs(curr_biomass[0] - prev_biomass[0]) <= 1e-02:
#         return (curr_biomass[0], curr_biomass[1], curr_biomass[2])
#     else:
#         return (curr_biomass[0]-prev_biomass[0], curr_biomass[1]-prev_biomass[1], curr_biomass[2]-prev_biomass[2])
#==============================================================================

def biomass_diff2(dbconn, speccode, region, dbh, ht, rounded=False, lower_bound=0, upper_bound=100):
    """Return increase in biomass between current year and previous year.
    
    Args:
    dbconn - database connection handle
    speccode - species code
    region - region code
    dbh - Tree dbh in cm
    ht - Tree height in m
    rounded - Are ages rounded to the nearest year?
    lower_bound - lower age bound (not used)
    upper_bound - upper age bound (not used)
    
    Returns:
    (difference between current and previous years' biomass,
     difference between current and previous years' carbon,
     difference between current and previous years' CO2 equivalent)
    """
    c = dbconn.cursor()
        # need to use growth_species calc here. good thing I have a function.
    growthspecies = growth_calc_species(dbconn, speccode, region)
    qstr = "SELECT AppsMin, AppsMax, AppsMinAge, AppsMaxAge FROM GrowCoeffsMinMAX WHERE SpecCode = '%s' AND Region = '%s'" % (growthspecies, region)
    c.execute(qstr)
    qresult = c.fetchone()
    (appsmin, appsmax, appsminage, appsmaxage) = qresult
    print "appsmin: ", appsmin, "appsmax: ", appsmax, "appsminage: ", appsminage, "appsmaxage: ", appsmaxage
    qstr = "SELECT b.EqnName FROM SpeciesCodeList a, VolBioCoeffs b WHERE a.BioMassAssign = b.SpecCode AND a.SpeciesCode = '%s' AND a.Region = '%s'" % (speccode, region)
    c = dbconn.cursor()
    c.execute(qstr)
    qresult = c.fetchone()
    (eqn2) = qresult
    minmaxtype = biomass.minmaxtypedict[eqn2[0]]
    print "eqn: ", eqn2[0], "minmaxtype: ", minmaxtype
    if minmaxtype == 'dbh':
        if dbh <= appsmin:
            dbh = appsmin
            curr_age = appsminage
        elif dbh >= appsmax:
            curr_age = appsmaxage
        else:
            curr_age = age_calc2(dbconn, speccode, region, dbh, ht, rounded, appsminage, appsmaxage, 'd.b.h.')
    else:
        if ht <= appsmin:
            ht = appsmin
            curr_age = appsminage
        elif ht >= appsmax:
            curr_age = appsmaxage
        else:
            curr_age = age_calc2(dbconn, speccode, region, dbh, ht, rounded, appsminage, appsmaxage, 'tree ht')
    #curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh, ht)
    prev_age = curr_age - 1
    print "Ages: ", curr_age, prev_age, 'appsminage: ', appsminage, 'appsmaxage: ', appsmaxage
    # what if we redo this logic such that we compute previous dbh and height for all 
    # species. i think this needs rewriting...
    
    if curr_age >= appsmaxage:
        if minmaxtype == 'dbh':
            dbh = appsmax - 0.0001
        else:
            ht = appsmax - 0.0001          
    if curr_age <= appsminage or prev_age < appsminage:
        if minmaxtype == 'dbh':
            prev_dbh = appsmin
            #prev_ht = ht # I persist with the problem for now...slightly changed
            (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'tree ht')
            prev_ht = eqn(prev_dbh, a, b, c, d, e)
        else:
            prev_ht = appsmin
            prev_dbh = dbh
        prev_age = appsminage
        curr_age = appsminage + 1
    else:
        try:
            (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'd.b.h.') 
            prev_dbh = eqn(prev_age, a, b, c, d, e)
        except TypeError:  # there are no d.b.h. equations in the grow coeffs table.
            prev_dbh = 0
        (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'tree ht')
        if minmaxtype == 'dbh':        
            prev_ht = eqn(prev_dbh, a, b, c, d, e) # not sure this is true for all eqns! don't look like it.
        else:
            prev_ht = eqn(prev_age, a, b, c, d, e) # so try this
    if rounded:
        (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'd.b.h.') 
        curr_dbh = eqn(curr_age, a, b, c, d, e)
        (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'tree ht')
        curr_ht = eqn(curr_age, a, b, c, d, e)
    else:
#==============================================================================
#         curr_dbh = dbh
#         curr_ht = ht
#==============================================================================
        #print "in corr block"
        if minmaxtype == 'dbh':
            #print "corr ht"
            curr_dbh = dbh
            (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'tree ht')
            curr_ht = eqn(curr_dbh, a, b, c, d, e)
            #print "corr currht: ", curr_ht, "curr age: ", curr_age
        else:
            curr_ht = ht
            curr_dbh = dbh
            #print "corr dbh"
            #(eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, 'd.b.h.') 
            #curr_dbh = eqn(curr_age, a, b, c, d, e)
            
    # print "curr_dbh: ", curr_dbh, "curr_ht: ", curr_ht, "prev_dbh: ", prev_dbh, "prev_ht: ", prev_ht
    curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=curr_dbh, ht=curr_ht)    
    prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=prev_dbh, ht=prev_ht)
   

#==============================================================================
#     (eqn, eqtype, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn(dbconn, speccode, region)
#     if eqtype == 'dbh':
#         if rounded:
#             curr_dbh = eqn(curr_age, a, b, c, d, e)
#             curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=curr_dbh, ht=0)
#         prev_dbh = eqn(prev_age, a, b, c, d, e)
#         # Let's deal with case where previous dbh is negative.
#         # Nope. Let's use age as the criteriod.
#         if curr_age <= appsminage or prev_age < appsminage:
#             prev_dbh = AppsMin
#         else:
#             prev_dbh = eqn(prev_age, a, b, c, d, e)
#         prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=prev_dbh, ht=0)
#     else:
#         if rounded:
#             curr_ht = eqn(curr_age, a, b, c, d, e)
#             curr_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=curr_ht)
#         prev_ht = eqn(prev_age, a, b, c, d, e)
#         if curr_age <= appsminage or prev_age < appsminage:
#             prev_ht = AppsMin
#         else:
#             prev_ht = eqn(prev_age, a, b, c, d, e)
#         prev_biomass = biomass.biomass_calc(dbconn, speccode, region, dbh=0, ht=prev_ht)
#==============================================================================
    print "curr_biomass", curr_biomass
    print "prev_biomass", prev_biomass
    # the results table sets the CO2 sequestration to the carbon stored in this minimum limiting case.
    # not quite -- if prev_biomass fails (negative age e.g.), the calc blows up

#    if curr_age >= appsmaxage:
#        return (curr_biomass[0], curr_biomass[1], 0.0)
    if abs(curr_biomass[0] - prev_biomass[0]) <= 1e-02:
        return (curr_biomass[0], curr_biomass[1], curr_biomass[2])
#    else:
#        return (curr_biomass[0]-prev_biomass[0], curr_biomass[1]-prev_biomass[1], curr_biomass[2]-prev_biomass[2])
    else:
        return (curr_biomass[0]-prev_biomass[0], curr_biomass[1]-prev_biomass[1], curr_biomass[2]-prev_biomass[2])

def inv_age_calc(dbconn, speccode, region, age, comptype):
    """Compute dbh or height given age."""
    (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, comptype)
    currval = eqn(age, a, b, c, d, e)
    return (currval, eqtype, AppsMin, AppsMax)
    
def biomasstoCO2(biomass0):
    """Compute CO2 equivalent for biomass value."""
    return (biomass0 * biomass.carbon_fraction / biomass.roots)  * biomass.co2_fraction 

def growth_age_table(dbconn, speccode, region):
    """Print out table giving dbh/ht values for particular ages..."""
    (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region)
    for age in range(0,151):
        print age, eqn(age, a, b, c, d, e)

def growth_coeffs_min_max(dbconn, tol=1e-04):
    """Populate GrowCoeffsMinMax table with corresponding min and max ages to AppsMin and AppsMax"""
    c = dbconn.cursor()
    qstr = "SELECT DISTINCT Region, SpecCode FROM GrowCoeffs"
    c.execute(qstr)
    qall = c.fetchall()
    specregions = filter(lambda x: x[0] != '', qall)
    for specregion in specregions:
        appstate = 'BeforeMin'
        minage = 0
        maxage = 500
        for age in range(0, 500):
            (currval, eqtype, AppsMin, AppsMax) = inv_age_calc(dbconn, specregion[1], specregion[0], age)
            if appstate != 'SeekingMax':
                if abs(currval - AppsMin ) < tol:
                    minage = age
                    appstate = 'FoundMin'
                if appstate == 'FoundMin' and (currval > AppsMin):
                    appstate = 'SeekingMax'
            else:
                if abs(currval - AppsMax) < tol:
                    maxage = age
                    break
        #print specregion[1], specregion[0], AppsMin, AppsMax, minage, maxage
        qstr = "INSERT INTO GrowCoeffsMinMAX VALUES ('%s', '%s', %f, %f, %d, %d)" % (specregion[0], specregion[1], AppsMin, AppsMax, minage, maxage )
        #print qstr        
        c.execute(qstr)
    dbconn.commit()
    """A few records fail to get values assigned (i.e. stay at 0,500). I manually adjust these
    using the GrowthResults table"""
                    
def inv_age_calc2(dbconn, speccode, region, age):
    """Return both dbh and height as a function of age."""
    qstr = "SELECT b.EqnName FROM SpeciesCodeList a, VolBioCoeffs b WHERE a.BioMassAssign = b.SpecCode AND a.SpeciesCode = '%s' AND a.Region = '%s'" % (speccode, region)
    c = dbconn.cursor()
    c.execute(qstr)
    qresult = c.fetchone()
    (eqn2) = qresult
    minmaxtype = biomass.minmaxtypedict[eqn2[0]]
    if minmaxtype == 'dbh':
        comptype = 'd.b.h.'
    else:
        comptype = 'tree ht'
    #print "eqn: ", eqn2[0], "minmaxtype: ", minmaxtype
    (eqn, eqtype, eqstr, a, b, c, d, e, AppsMin, AppsMax) = growth_calc_eqn2(dbconn, speccode, region, comptype)
    #print "eqn: ", eqn, "eqtype: ", eqtype,  "a: ", a, "b: ", b, "c: ", c, "d: ", d, "e: ", e
    currval = eqn(age, a, b, c, d, e)
    if currval < AppsMin:
        currval = AppsMin
    if currval > AppsMax:
        currval = AppsMax
    if comptype == 'd.b.h.':
        (eqn2, eqtype2, eqstr2, a2, b2, c2, d2, e2, AppsMin2, AppsMax2) = growth_calc_eqn2(dbconn, speccode, region, 'tree ht')
        newval = eqn2(currval, a2, b2, c2, d2, e2)
        newdbh = currval
        newht = newval
    else:
        #(eqn2, eqtype2, eqstr2, a2, b2, c2, d2, e2, AppsMin2, AppsMax2) = growth_calc_eqn2(dbconn, speccode, region, 'd.b.h.')
        #newval = eqn2(currval, a2, b2, c2, d2, e2)
        newht = currval
        newdbh = None
    return (newdbh, newht, eqtype, AppsMin, AppsMax)
                
                
