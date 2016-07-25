from emissions.emissionscalc import energycalc
import csv


def testrun():
    infile = open("/home/adh/UrbanForests/JDGCode/sac_buildings_run.csv")
    inlist = []
    outfile = open("/home/adh/UrbanForests/JDGCode/sac_buildings_testcalc.csv", "w")
    outwriter = csv.writer(outfile)
    for row in csv.reader(infile):
        inlist.append(row)
        
    for l in inlist[1:]:
        (spcode, climatezone, dbh_orig, height, azimuth, distance, vintage, shade_reduction, lu_conversion_shade, lu_conversion_climate, eqpt_cooling_potential, eqpt_heating_potential) = (l[6], l[1], l[7], l[8], l[9], l[10], l[11], l[14], l[16], l[17], l[18], l[19])
#        print (spcode, climatezone, dbh_orig, height, azimuth, distance, vintage, shade_reduction, lu_conversion_shade, lu_conversion_climate, eqpt_cooling_potential, eqpt_heating_potential)
        energyresult = energycalc(spcode, climatezone, dbh_orig, height, azimuth, distance, vintage, shade_reduction, lu_conversion_shade, lu_conversion_climate, eqpt_cooling_potential, eqpt_heating_potential)
        print(energyresult)
        outwriter.writerow(energyresult)
    outfile.close()


## http://localhost:8000/api/avoided?spec=WARO&region=SoCalC&dbh=18.05512786&ht=37.72966&azimuth=85&dist=28&vintage=1954&shadereduc=0.85&luconvshade=1&luconvclim=1&eqcoolpot=0.3029&eqheatpot=0.479
