rm(list=ls())

require(dplyr)
require(RSQLite)

# connect to db
db = dbConnect("SQLite",dbname="/Users/johndegoede/Documents/Final_UFORE_FIA_Organization/SQLite_Database/rollup")


# get tree data from sqlite db  
            res <- dbSendQuery(db, "SELECT * from `fia.tree.carbon`")
            fia.tree.carbon <- dbFetch(res)
            dbClearResult(res)
            fia.tree.carbon %>% nrow() # check rownums
            fia.tree.carbon[,c(2:5,7:10)] <- sapply(fia.tree.carbon[,c(2:5,7:10)],as.numeric) # convert certain cols to numeric

            res <- dbSendQuery(db, "SELECT * from `la.tree.carbon`")
            la.tree.carbon <- dbFetch(res)
            dbClearResult(res)
            la.tree.carbon %>% nrow()
            la.tree.carbon[,c(2:4,6:9)] <- sapply(la.tree.carbon[,c(2:4,6:9)],as.numeric)

            res <- dbSendQuery(db, "SELECT * from `sac.tree.carbon`")
            sac.tree.carbon <- dbFetch(res)
            dbClearResult(res)
            sac.tree.carbon %>% nrow()
            sac.tree.carbon[,c(2:4,6:9)] <- sapply(sac.tree.carbon[,c(2:4,6:9)],as.numeric)
            
            res <- dbSendQuery(db, "SELECT * from `sb.tree.carbon`")
            sb.tree.carbon <- dbFetch(res)
            dbClearResult(res)
            sb.tree.carbon %>% nrow()
            sb.tree.carbon[,c(2:4,6:9)] <- sapply(sb.tree.carbon[,c(2:4,6:9)],as.numeric)

# get plot data from sqlite db
            res <- dbSendQuery(db, "SELECT * from `fia.plots.included`")
            fia.plots.included <- dbFetch(res)
            dbClearResult(res)
            fia.plots.included %>% nrow()
            
            res <- dbSendQuery(db, "SELECT * from `la.plots.included`")
            la.plots.included <- dbFetch(res)
            dbClearResult(res)
            la.plots.included %>% nrow()
            
            res <- dbSendQuery(db, "SELECT * from `sac.plots.included`")
            sac.plots.included <- dbFetch(res)
            dbClearResult(res)
            sac.plots.included %>% nrow()
            
            res <- dbSendQuery(db, "SELECT * from `sb.plots.included`")
            sb.plots.included <- dbFetch(res)
            dbClearResult(res)
            sb.plots.included %>% nrow()

# get avoided emis calcs data from sqlite db
           # res <- dbSendQuery(db, "SELECT * from `fia.buildings.calcs`")
            res <- dbSendQuery(db, "SELECT * from `fia.buildings.calcs.01092015`")
            fia.building.calcs <- dbFetch(res)
            dbClearResult(res)
            fia.building.calcs %>% nrow()
            fia.building.calcs[,c(4:6,17,23)] <- sapply(fia.building.calcs[,c(4:6,17,23)],as.numeric)

            # res <- dbSendQuery(db, "SELECT * from `la.buildings.calcs`")
            res <- dbSendQuery(db, "SELECT * from `la.buildings.calcs.01092015`")
            la.building.calcs <- dbFetch(res)
            dbClearResult(res)
            la.building.calcs %>% nrow()
            la.building.calcs[,3:5] <- sapply(la.building.calcs[,3:5],as.numeric)

           # res <- dbSendQuery(db, "SELECT * from `sac.buildings.calcs`")
            res <- dbSendQuery(db, "SELECT * from `sac.buildings.calcs.01092015`")  
            sac.building.calcs <- dbFetch(res)
            dbClearResult(res)
            sac.building.calcs %>% nrow()
            sac.building.calcs[,3:5] <- sapply(sac.building.calcs[,3:5],as.numeric)

           # res <- dbSendQuery(db, "SELECT * from `sb.buildings.calcs`")
            res <- dbSendQuery(db, "SELECT * from `sb.buildings.calcs.01092015`")
            sb.building.calcs <- dbFetch(res)
            dbClearResult(res)
            sb.building.calcs %>% nrow()
            sb.building.calcs[,3:5] <- sapply(sb.building.calcs[,3:5],as.numeric)

# equations from Allan
      # roots = 0.78
      # carbon_fraction = 0.5
      # co2_fraction = 3.67
      # carbon = carbon_fraction * biomass / roots
      # co2 = carbon * co2_fraction

la.av.emis <- la.plots.included %>% 
                  #join tree plot-level data to tree calculations from Allan
                  left_join(.,la.tree.carbon %>% group_by(plot.id) %>% 
                  summarize(biomass.kg=sum(biomass),CO2seq.kg=sum(CO2sequestered),tree.count=n()),by=c("plot_id"="plot.id")) %>%  
                    #calculate CO2 stored from biomass
                    mutate(CO2stored.kg = 3.67*(0.5*biomass.kg/0.78))  %>%
                      #join with avoided emission calculations by plot_id, calculate avoided emissions (by summing cooling heating reduct kg)
                      left_join(.,la.building.calcs %>% group_by(plot_id) %>% 
                      summarize(avoided.emis=sum(cooling_heating_reduct_kg_tree_)),by=c("plot_id"="plot_id")) %>% 
                        #create subplot column; always 1 for U4 data since there are no subplots in U4
                        mutate(subplot_id=1) %>% 
                          #select columns we want to keep
                          select(plot.id=plot_id,subplot.id=subplot_id,tree.count,type,cz,lu=crosswalk,ufcode,
                                 plot.area.ha=plot_area_ha,canopy.area.ha = canopy_area_ha,biomass.kg,
                                 CO2seq.kg,CO2stored.kg,CO2AvEmis.kg=avoided.emis)

la.av.emis[c(1:3,7:13)]<- sapply(la.av.emis[c(1:3,7:13)],as.numeric) # convert certain columns to numeric
                                             
sac.av.emis <-  sac.plots.included %>% 
                      #join tree plot-level data to tree calculations from Allan
                      left_join(.,sac.tree.carbon %>% group_by(plot.id) %>% 
                      summarize(biomass.kg=sum(biomass),CO2seq.kg=sum(CO2sequestered),tree.count=n()),by=c("plot_id"="plot.id")) %>%  
                        #calculate CO2 stored from biomass
                        mutate(CO2stored.kg = 3.67*(0.5*biomass.kg/0.78))  %>%
                          #join with avoided emission calculations by plot_id, calculate avoided emissions (by summing cooling heating reduct kg)
                          left_join(.,sac.building.calcs %>% group_by(plot_id) %>% 
                          summarize(avoided.emis=sum(cooling_heating_reduct_kg_tree_)),by=c("plot_id"="plot_id")) %>% mutate(subplot_id=1) %>%
                              #select columns we want to keep 
                              select(plot.id=plot_id,subplot.id=subplot_id,tree.count,type,cz,lu=crosswalk,ufcode,
                                     plot.area.ha=plot_area_ha,canopy.area.ha=canopy_area_ha,biomass.kg,
                                     CO2seq.kg,CO2stored.kg,CO2AvEmis.kg=avoided.emis) 

sac.av.emis[c(1:3,7:13)]<- sapply(sac.av.emis[c(1:3,7:13)],as.numeric) # convert certain columns to numeric

sb.av.emis <-  sb.plots.included %>% 
                     #join tree plot-level data to tree calculations from Allan
                     left_join(.,sb.tree.carbon %>% group_by(plot.id) %>% 
                     summarize(biomass.kg=sum(biomass),CO2seq.kg=sum(CO2sequestered),tree.count=n()),by=c("plot_id"="plot.id")) %>%  
                        #calculate CO2 stored from biomass
                        mutate(CO2stored.kg = 3.67*(0.5*biomass.kg/0.78))  %>%
                          #join with avoided emission calculations by plot_id, calculate avoided emissions (by summing cooling heating reduct kg)
                          left_join(.,sb.building.calcs %>% group_by(plot_id) %>% 
                          summarize(avoided.emis=sum(cooling_heating_reduct_kg_tree_)),by=c("plot_id"="plot_id")) %>% mutate(subplot_id=1) %>%
                             #select columns we want to keep
                             select(plot.id=plot_id,subplot.id=subplot_id,tree.count,type,cz,lu=crosswalk,ufcode,
                                    plot.area.ha=plot_area_ha,canopy.area.ha=canopy_area_ha,biomass.kg,
                                    CO2seq.kg,CO2stored.kg,CO2AvEmis.kg=avoided.emis)

sb.av.emis[c(1:3,7:13)]<- sapply(sb.av.emis[c(1:3,7:13)],as.numeric) # convert certain columns to numeric

fia.av.emis <- fia.plots.included %>% 
                      #join tree plot-level data to tree calculations from Allan; this is FIA data so join by plot.id and subplot.id here
                      left_join(.,fia.tree.carbon %>% group_by(plot.id,subplot.id) %>%
                      summarize(biomass.kg=sum(biomass),CO2seq.kg=sum(CO2sequestered),tree.count=n()),by=c("plot_id"="plot.id","subplot_id"="subplot.id")) %>% 
                          #calculate CO2 stored from biomass
                          mutate(CO2stored.kg = 3.67*(0.5*biomass.kg/0.78)) %>% 
                             #join with avoided emission calculations by plot_id, calculate avoided emissions (by summing cooling heating reduct kg)       
                             left_join(.,fia.building.calcs %>% group_by(plot_id,subplot_id) %>% 
                             summarize(avoided.emis=sum(`cooling_heating_reduct_kg_tree_`)),by=c("plot_id"="plot_id","subplot_id"="subplot_id")) %>% 
                               #select columns we want to keep
                               select(plot.id=plot_id,subplot.id=subplot_id,tree.count,type,lu=crosswalk,cz,ufcode,
                                      plot.area.ha=plot_area_ha,canopy.area.ha=canopy_area_ha,biomass.kg,
                                      CO2seq.kg,CO2stored.kg,CO2AvEmis.kg=avoided.emis) 

fia.av.emis[c(1:3,7:13)]<-sapply(fia.av.emis[c(1:3,7:13)],as.numeric) # convert certain columns to numeric
 
# combine all avoided emission data
all.plots <- rbind_all(list(fia.av.emis,la.av.emis,sac.av.emis,sb.av.emis))

# eliminate NAs, replace with 0's; probably a shorter way of writing this, or perhaps dplyr isn't best solution here, but in order to keep it consistent...
all.plots2<- all.plots %>%
      mutate(tree.count=
              ifelse(is.na(tree.count),0,tree.count)) %>% 
      mutate(biomass.kg=
            ifelse(is.na(biomass.kg), 0, biomass.kg)) %>%
      mutate(CO2seq.kg=
               ifelse(is.na(CO2seq.kg), 0, CO2seq.kg)) %>% 
      mutate(CO2stored.kg=
               ifelse(is.na(CO2stored.kg), 0, CO2stored.kg)) %>% 
      mutate(CO2AvEmis.kg=
               ifelse(is.na(CO2AvEmis.kg), 0, CO2AvEmis.kg)) 

# create transfer functions
kg2t = .001 # conversion from kg to metric tonnes

#tf = "transfer function" - i.e. unit ecosystem service per unit canopy area
all.plots.tf <- 
            all.plots2 %>% 
            group_by(cz,lu) %>%
            # get all sums
            summarize(
                    total.plots=n(),
                    total.trees=sum(tree.count),
                    total.plot.area.ha = sum(plot.area.ha),
                    total.canopy.area.ha=sum(canopy.area.ha),
                    total.biomass.kg= sum(biomass.kg),
                    total.CO2.seq.kg= sum(CO2seq.kg),
                    total.CO2.stored.kg= sum(CO2stored.kg),
                    total.CO2.avoided.emis= sum(CO2AvEmis.kg,na.rm=TRUE)
                    ) %>%
            # create tfs from the sums
            mutate(
                    biomass.tf=(total.biomass.kg * kg2t)/total.canopy.area.ha,
                    CO2seq.tf=(total.CO2.seq.kg * kg2t)/total.canopy.area.ha,
                    CO2stored.tf=(total.CO2.stored.kg*kg2t)/total.canopy.area.ha,
                    CO2.avoided.tf=(total.CO2.avoided.emis*kg2t)/total.canopy.area.ha,
                    `CO2.dollar.per.t`=16.53, # this value is constant across CA 
                    `CO2seq.tf.dollars`=`CO2.dollar.per.t`*`CO2seq.tf`,
                    `CO2.avoided.tf.dollars`=`CO2.dollar.per.t`*`CO2.avoided.tf`
                    #Cseq.tf=CO2seq.tf/3.67,
                    #Cstored.tf=CO2stored.tf/3.67,
                    #C.avoided.tf=CO2.avoided.tf/3.67,
                    ) %>% ungroup()

# round to 2 decimal places
all.plots.tf[,5:17] <- round(all.plots.tf[,5:17],2)
# in lu/cz combinations where no trees exist, fill NA's with NO DATA
all.plots.tf[all.plots.tf$total.trees==0,][,c(7:14,16:17)]<-"NO DATA"

# last row is an FIA plot that somehow fell out of climate zone boundaries, so we remove that
all.plots.tf %>% tail()
all.plots.tf <- all.plots.tf %>% slice(-35)
# view final table
all.plots.tf %>% View()

