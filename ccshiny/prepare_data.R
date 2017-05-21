# Create datasets for loading into Shiny application.

library(hash)

regionlist <- read.csv("/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/regions.csv")
speclist <- read.csv("/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/speciescodes.csv", header=FALSE)
names(speclist) <- c("speccode", "specname")
#specenv <- new.env(hash=TRUE)
spechash <- hash()

#for(i in seq(1:nrow(speclist))) {
#  specenv[[as.character(speclist[i,2])]] <- as.character(speclist[i,1])
#}

for(i in seq(1:nrow(speclist))) {
  spechash[[as.character(speclist[i,2])]] <- as.character(speclist[i,1])
}

#regionenv <- new.env()
regionhash <- hash()

#for(i in seq(1:nrow(regionlist))) {
#  regionenv[[as.character(regionlist[i,3])]] <- as.character(regionlist[i,1])
#}

for(i in seq(1:nrow(regionlist))) {
  regionhash[[as.character(regionlist[i,3])]] <- as.character(regionlist[i,1])
}

regioncombvec <- c(as.character(regionlist[,3]), as.character(regionlist[,1]))
speccombvec <- c(as.character(speclist[,2]), as.character(speclist[,1]))

saveRDS(regioncombvec, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/regioncombvec.rds")
saveRDS(speccombvec, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/speccombvec.rds")
#saveRDS(regionenv, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/regionenv.rds")
#saveRDS(specenv, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/specenv.rds")
saveRDS(regionhash, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/regionhash.rds")
saveRDS(spechash, "/home/adh/UrbanForests/WebCalculator/urbantreecc/ccshiny/data/spechash.rds")
