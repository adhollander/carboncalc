from emissions.models import BuildingClasses, AzimuthClasses, DbhClassesInterp, Palms, Energylong2, AppsMax, MaxCoolHeat, EmisFactorsCooling, EmisFactorsHeating
from django.db.models import Q

def energycalc(spcode, climatezone, dbh_orig, height, azimuth, distance, vintage, shade_reduction, lu_conversion_shade, lu_conversion_climate, eqpt_cooling_potential, eqpt_heating_potential):
    error_factor = 0.7
    dbh_orig = float(dbh_orig)
    height = float(height)
    azimuth = float(azimuth)
    distance = float(distance)
    vintage = float(vintage)
    shade_reduction = float(shade_reduction)
    lu_conversion_shade = float(lu_conversion_shade)
    lu_conversion_climate = float(lu_conversion_climate)
    eqpt_cooling_potential = float(eqpt_cooling_potential)
    eqpt_heating_potential = float(eqpt_heating_potential)
#    import ipdb; ipdb.set_trace()
    
    palmlist = [palm.sp_code for palm in Palms.objects.all()]
    if spcode in palmlist:
        dbh_calc = height
    else:
        dbh_calc = dbh_orig
        
    try:
        dbh_lookup_class_min = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].class_low
        dbh_lookup_class_max = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].class_high
        dbh_low = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].midlow
        dbh_high = DbhClassesInterp.objects.filter(Q(midlowfake__lte=dbh_calc) & Q(midhighfake__gt=dbh_calc))[0].midhigh
    
        if azimuth <= 22.5 or azimuth >= 337.5:
            azimuth_lookup_class = "N"
        else:  
            azimuth_lookup_class = AzimuthClasses.objects.filter(Q(degree_start__lte=azimuth) & Q(degree_end__gte=azimuth))[0].direction 
        
        building_lookup_class = BuildingClasses.objects.filter(Q(distance_start__lte=distance) & Q(distance_end__gte=distance))[0].class_desc
        
        if vintage < 1950:
            vintage_lookup_class = "pre1950"
        elif vintage >= 1950 and vintage <= 1980:
            vintage_lookup_class = "1950-1980"
        else:
            vintage_lookup_class = "post1980"
        
#        import ipdb; ipdb.set_trace()
        
        #q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        #try:
            #cooling_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction
        #except IndexError:
            #cooling_climate_low = 0 # set to 0 per lines 219-226 in avoided_emissions_calculator.R
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        #try:
            #cooling_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction
        #except IndexError:
            #cooling_climate_high = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        #try:
            #cooling_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction
        #except IndexError:
            #cooling_shade_low = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        #try:
            #cooling_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction
        #except IndexError:
            #cooling_shade_high = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        #try:
            #heating_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
        #except IndexError:
            #heating_climate_low = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        #try:
            #heating_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
        #except IndexError:
            #heating_climate_high = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        #try:
            #heating_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
        #except IndexError:
            #heating_shade_low = 0
            
        #q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        #try:
            #heating_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
        #except IndexError:
            #heating_shade_high = 0
    
    # version that uses large-scoped exception handling...
    
  # lookup all cooling energy reduction values (values are in "energy_reduction") #
  # for each tree, there will be a climate value (corresponding to clim in the building.lookup.class)
  # for any tree within 60ft of a building, there will also be a shade value (corresponding to adj, near, or far in the building lookup class)
        q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        cooling_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        cooling_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        cooling_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="cool") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        cooling_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        heating_climate_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist="Clim") & Q(vintage=vintage_lookup_class)
        heating_climate_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_min) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        heating_shade_low = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    
            
        q1 = Q(cz=climatezone) & Q(benefit_type="heat") & Q(species=spcode) & Q(dbh_class=dbh_lookup_class_max) & Q(azimuth=azimuth_lookup_class) & Q(dist=building_lookup_class) & Q(vintage=vintage_lookup_class)
        heating_shade_high = Energylong2.objects.filter(q1)[0].energy_reduction * 0.001
    
        
        if spcode in palmlist:
            max_dbh = AppsMax.objects.filter(Q(sp_code=spcode) & Q(cz=climatezone))[0].height_ft
        else:
            max_dbh = AppsMax.objects.filter(Q(sp_code=spcode) & Q(cz=climatezone))[0].dbh_in
            
        if dbh_calc > max_dbh:
            dbh_calc = max_dbh
            
        # calculate cooling (kWh) & heating (MBtu)
        #### interpolate the high and low values ##
        cooling_climate_interp = cooling_climate_low + (dbh_calc - dbh_low)*(cooling_climate_high-cooling_climate_low)/(dbh_high-dbh_low)
        cooling_shade_interp = cooling_shade_low + (dbh_calc - dbh_low)*(cooling_shade_high-cooling_shade_low)/(dbh_high-dbh_low)
        heating_climate_interp = heating_climate_low + (dbh_calc - dbh_low)*(heating_climate_high-heating_climate_low)/(dbh_high-dbh_low)
        heating_shade_interp = heating_shade_low + (dbh_calc - dbh_low)*(heating_shade_high-heating_shade_low)/(dbh_high-dbh_low)
         
        # check to see if it is surpassing max cooling contribution; not applicable for heating.  
        max_cool_contrib = MaxCoolHeat.objects.filter(Q(cz=climatezone) & Q(type_max="cool") & Q(vintage=vintage_lookup_class))[0].max  
        
        # jim's calculator totals both the climate and the shade
        if cooling_climate_interp > max_cool_contrib:
            cooling_climate_interp = max_cool_contrib
        else: 
            cooling_climate_interp = cooling_climate_interp
    
        if cooling_shade_interp > max_cool_contrib:
            cooling_shade_interp = max_cool_contrib
        else:
            cooling_shade_interp = cooling_shade_interp
            
        #### apply shade reductions ####
        cooling_shade_interp2 = cooling_shade_interp * shade_reduction
        heating_shade_interp2 = heating_shade_interp * shade_reduction
        cooling_climate_interp2 = cooling_climate_interp
        heating_climate_interp2 = heating_climate_interp
        
        #### apply land use conversions ####
        cooling_shade_interp3 = cooling_shade_interp2 * lu_conversion_shade
        heating_shade_interp3 = heating_shade_interp2 * lu_conversion_shade
        cooling_climate_interp3 = cooling_climate_interp2 * lu_conversion_climate
        heating_climate_interp3 = heating_climate_interp2 * lu_conversion_climate
        
        # distinguish between trees w/ only climate effects and those with shade and climate effects
        if distance>60.0001:
            cooling_total_ctcc = cooling_climate_interp
            heating_total_ctcc = heating_climate_interp
            cooling_total_reducts = cooling_climate_interp3
            heating_total_reducts = heating_climate_interp3
        else:
           cooling_total_ctcc = cooling_climate_interp + cooling_shade_interp
           heating_total_ctcc = heating_climate_interp + heating_shade_interp
           cooling_total_reducts = cooling_climate_interp3 + cooling_shade_interp3 
           heating_total_reducts = heating_climate_interp3 + heating_shade_interp3 
           
        cooling_total = cooling_total_reducts * eqpt_cooling_potential
        heating_total = heating_total_reducts * eqpt_heating_potential 
       
       
        ##### calculate emission equivalents (kg) for cooling & heating
        # compile emission reductions in kg
        # first, find climate zone-dependent cooling emissions values and subset them
        ef_cooling_subset = EmisFactorsCooling.objects.filter(cz=climatezone)[0]
        
        # lookup emissions factors cooling #
        # must convert emissions to co2 equivalents - emis.factors.cooling.subset[1] & so forth represent co2, methane, and nitrous oxide emission factors and 
        # multiply by global warming potential (co2=1,methane=23,no=296#
        # also calculate for ctcc to compare with carbon calculator

        # ctcc
        co2_cooling_emis_ctcc = cooling_total_ctcc*(ef_cooling_subset.co2_avg_emis_factor_kg_kwh_field)
        methane_cooling_emis_ctcc = cooling_total_ctcc*(ef_cooling_subset.methane_avg_emis_factor_kg_kwh_field*23)
        no_cooling_emis_ctcc = cooling_total_ctcc*(ef_cooling_subset.nitrous_oxide_avg_emis_factor_kg_kwh_field*296)
    
        all_cooling_emis_ctcc = co2_cooling_emis_ctcc + methane_cooling_emis_ctcc + no_cooling_emis_ctcc
        
        # new results w/multi tree & eqpt reductions
        co2_cooling_emis = cooling_total*(ef_cooling_subset.co2_avg_emis_factor_kg_kwh_field)
        methane_cooling_emis = cooling_total*(ef_cooling_subset.methane_avg_emis_factor_kg_kwh_field*23)
        no_cooling_emis = cooling_total*(ef_cooling_subset.nitrous_oxide_avg_emis_factor_kg_kwh_field*296)
    
        all_cooling_emis = co2_cooling_emis + methane_cooling_emis + no_cooling_emis
        
        # lookup emissions factors heating; unlike cooling, heating efs not climate-zone dependent #   
        ef_heating_subset = EmisFactorsHeating.objects.filter(fuel_type="Natural Gas")[0] # was fuel oil ignored because we were in Calif?
        
        # ctcc
        co2_heating_emis_ctcc = heating_total_ctcc*(ef_heating_subset.co2_emis_factor_kg_mbtu_field)
        methane_heating_emis_ctcc = heating_total_ctcc*(ef_heating_subset.methane_emis_factor_kg_mbtu_field*23)
        no_heating_emis_ctcc = heating_total_ctcc*(ef_heating_subset.nitrous_oxide_emis_factor_kg_mbtu_field*296)
        all_heating_emis_ctcc = co2_heating_emis_ctcc + methane_heating_emis_ctcc + no_heating_emis_ctcc
        
        # new results w/multi tree & eqpt reductions
        co2_heating_emis = heating_total*(ef_heating_subset.co2_emis_factor_kg_mbtu_field)
        methane_heating_emis = heating_total*(ef_heating_subset.methane_emis_factor_kg_mbtu_field*23)
        no_heating_emis = heating_total*(ef_heating_subset.nitrous_oxide_emis_factor_kg_mbtu_field*296)
        all_heating_emis = co2_heating_emis + methane_heating_emis + no_heating_emis

        # ctcc
        all_emis_ctcc = all_cooling_emis_ctcc + all_heating_emis_ctcc
    
        # ours
        all_emis = all_cooling_emis + all_heating_emis
        
        # error_reductions
        cooling_total_ctcc = cooling_total_ctcc * error_factor
        cooling_total = cooling_total * error_factor
        heating_total_ctcc = heating_total_ctcc * error_factor
        heating_total = heating_total * error_factor                       
        all_cooling_emis_ctcc = all_cooling_emis_ctcc * error_factor
        all_cooling_emis = all_cooling_emis * error_factor
        all_heating_emis_ctcc = all_heating_emis_ctcc * error_factor
        all_heating_emis = all_heating_emis* error_factor
        all_emis_ctcc = all_emis_ctcc * error_factor
        all_emis = all_emis * error_factor
        
        # form results tuple
        # I take out a bunch of id stuff. Can argue it doesn't really belong in this function.
        results = (spcode, climatezone, dbh_orig, dbh_calc, max_dbh, height, distance, building_lookup_class, azimuth_lookup_class, vintage_lookup_class, ef_cooling_subset.co2_avg_emis_factor_kg_kwh_field, cooling_total_ctcc, cooling_total,heating_total_ctcc, heating_total, all_cooling_emis_ctcc, all_cooling_emis, all_heating_emis_ctcc, all_heating_emis, all_emis_ctcc, all_emis)

    
    except IndexError:
        return ("Database lookup error")
    else:
    #return (dbh_lookup_class_min,dbh_lookup_class_max, dbh_low, dbh_high, azimuth_lookup_class, building_lookup_class, vintage_lookup_class, cooling_climate_low, cooling_climate_high, cooling_shade_low)
        return (results)
