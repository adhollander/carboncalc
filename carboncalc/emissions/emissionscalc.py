from emissions.models import BuildingClasses, AzimuthClasses, DbhClassesInterp, Palms, Energylong2, AppsMax, MaxCoolHeat
from django.db.models import Q

def energycalc(spcode, climatezone, dbh_orig, height, azimuth, distance, vintage):
    errorfactor = 0.7
    palmlist = [palm.sp_code for palm in Palms.objects.all()]
    if spcode in palmlist:
        dbh_calc = height
    else:
        dbh_calc = dbh_orig
    dbh_lookup_class_min = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].class_low
    dbh_lookup_class_max = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].class_high
    dbh_low = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].midlow
    dbh_high = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].midhigh

    if azimuth <= 22.5 or azimuth >= 337.5:
        azimuth_lookup_class = "N"
    else:  
        azimuth_lookup_class = AzimuthClasses.objects.filter(Q(degree_start__lte=azimuth))[0].direction 
    
    building_lookup_class = BuildingClasses.objects.filter(Q(distance_start__lte=distance) & Q(distance_end__gt=distance))[0].class_desc
    
    if vintage < 1950:
        vintage_lookup_class = "pre1950"
    elif vintage >= 1950 and vintage <= 1980:
        vintage_lookup_class = "1950-1980"
    else:
        vintage_lookup_class = "post1980"
    
    q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
    try:
        cooling_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction
    except IndexError:
        cooling_climate_low = 0 # set to 0 per lines 219-226 in avoided_emissions_calculator.R
        
    q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
    try:
        cooling_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction
    except IndexError:
        cooling_climate_high = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
    try:
        cooling_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction
    except IndexError:
        cooling_shade_low = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
    try:
        cooling_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction
    except IndexError:
        cooling_shade_high = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
    try:
        heating_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    except IndexError:
        heating_climate_low = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
    try:
        heating_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    except IndexError:
        heating_climate_high = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
    try:
        heating_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    except IndexError:
        heating_shade_low = 0
        
    q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
    try:
        heating_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    except IndexError:
        heating_shade_high = 0
    
    try:
        if spcode in palmlist:
            max_dbh = AppsMax.objects.filter(Q(sp_code=spcode) & Q(cz=climatezone))[0].height_ft
        else:
            max_dbh = AppsMax.objects.filter(Q(sp_code=spcode) & Q(cz=climatezone))[0].dbh_in
    except IndexError:
        max_dbh = None
        
    if dbh_calc > max_dbh:
        dbh_calc = max_dbh
        
    cooling_climate_interp = cooling_climate_low + (dbh_calc - dbh_low)*(cooling_climate_high-cooling_climate_low)/(dbh_high-dbh_low)
    cooling_shade_interp = cooling_shade_low + (dbh_calc - dbh_low)*(cooling_shade_high-cooling_shade_low)/(dbh_high-dbh_low)
    heating_climate_interp = heating_climate_low + (dbh_calc - dbh_low)*(heating_climate_high-heating_climate_low)/(dbh_high-dbh_low)
    heating_shade_interp = heating_shade_low + (dbh_calc - dbh_low)*(heating_shade_high-heating_shade_low)/(dbh_high-dbh_low)
        
    max_cool_contrib = MaxCoolHeat.objects.filter(Q(cz=climatezone) & Q(type_max="cool") & Q(vintage=vintage_lookup_class))[0].max  
    
    if cooling_climate_interp > max_cool_contrib:
        cooling_climate_interp = max_cool_contrib
    else: 
        cooling_climate_interp = cooling_climate_interp

    if cooling_shade_interp > max_cool_contrib:
        cooling_shade_interp = max_cool_contrib
    else:
        cooling_shade_interp = cooling_shade_interp

    #return (dbh_lookup_class_min,dbh_lookup_class_max, dbh_low, dbh_high, azimuth_lookup_class, building_lookup_class, vintage_lookup_class, cooling_climate_low, cooling_climate_high, cooling_shade_low)
    return (dbh_low, dbh_high, azimuth_lookup_class, building_lookup_class, vintage_lookup_class, cooling_climate_low, cooling_climate_high, cooling_shade_low, cooling_shade_high)
