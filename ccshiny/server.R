# Server logic for preliminary interface to carbon calculator using R/Shiny.
#
#

library(shiny)
library(rhandsontable) # Used for spreadsheet interface to calculator

treecols <- c("aww", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")

shinyServer(function(input, output, session) {
  values <- reactiveValues()
  
  observeEvent(input$uploadedsheet, {
    fuploaded <- input$uploadedsheet[1,"datapath"]
    if(!is.null(fuploaded)) {
      fdf <- read.csv(fuploaded)
      treedf <- data.frame(treeid = numeric(), species = character(), region = character(),
                           dbh = numeric(), height = numeric(), biomass = numeric(), carbon = numeric(), co2 = numeric(),
                           biomassg = numeric(), carbong = numeric(), co2g = numeric(),
                           stringsAsFactors = F)
      treedfnames <- names(treedf)
      treedf <- rbind(treedf, fdf[,1:5])
      nacol <- rep(NA, nrow(treedf))
      treedf <- cbind(treedf, biomass=nacol, carbon=nacol, co2=nacol, biomassg=nacol, carbong=nacol, co2g=nacol )
#      names(treedf) <- treedfnames
      values[["DF"]] <- treedf
    }
  }, ignoreNULL=FALSE)
  
  observeEvent(input$calc_results, {
  #data <- eventReactive(input$calc_results, {
 # data <- eventReactive(catcher(), {
      
    if (!is.null(input$hot)) {
      DF = hot_to_r(input$hot)
    } else {
      if (is.null(values[["DF"]]))
        DF = data.frame(treeid = 1:10, species = rep('QUAG', 10), region = rep('NoCalC', 10),
                        dbh = rep(5,10), height= rep(4,10), biomass=rep(NA,10), carbon=rep(NA,10), co2=rep(NA,10),
                        biomassg=rep(NA,10), carbong=rep(NA,10), co2g=rep(NA,10),
                        stringsAsFactors = F)
      else
        DF <- values[["DF"]]
    }
    biomassd <- biomassq(DF$species, DF$region, DF$dbh, DF$height)
    DF$biomass <- biomassd$biomass
    DF$carbon <- biomassd$carbon
    DF$co2 <- biomassd$co2
    
    growthd <- growthq(DF$species, DF$region, DF$dbh, DF$height)
    DF$biomassg <- growthd$biomass
    DF$carbong <- growthd$carbon
    DF$co2g <- growthd$co2
    values[["DF"]] <- DF
   # DF
  }, ignoreNULL = FALSE)
  
#   calc_results <- eventReactive(input$calc_results,
#     {
#     DF <- values[["DF"]]
#     biomassd <- biomassq(DF$species, DF$region, DF$dbh, DF$height)
#     DF$biomass <- biomassd$biomass
#     DF$carbon <- biomassd$carbon
#     DF$co2 <- biomassd$co2
#     values[["DF"]] <- DF
#     DF
#   }, ignoreNULL = FALSE)

  output$hot <- renderRHandsontable({
    #DF <- data()
    #DF <- calc_results()
    DF <- values[["DF"]]
#     biomassd <- biomassq(DF$species, DF$region, DF$dbh, DF$height)
#     DF$biomass <- biomassd$biomass
#     DF$carbon <- biomassd$carbon
#     DF$co2 <- biomassd$co2
    if (!is.null(DF))
      #rhandsontable(DF, useTypes = as.logical(input$useType), stretchH = "all")
     rhandsontable(DF, useTypes = FALSE, stretchH = "all", rowHeaders = NULL) %>%
      hot_col("species", type="autocomplete", source=speclist) %>%
      hot_col("region", type="dropdown", source=regions) %>%
      hot_col("biomass", type="numeric", readOnly = TRUE, format= '0.0000') %>%
      hot_col("carbon", type="numeric", readOnly = TRUE, format="0.0000") %>%
      hot_col("co2", type="numeric", readOnly = TRUE, format="0.0000") %>%
      hot_col("biomassg", type="numeric", readOnly = TRUE, format="0.0000") %>%
      hot_col("carbong", type="numeric", readOnly = TRUE, format="0.0000") %>%
      hot_col("co2g", type="numeric", readOnly = TRUE, format="0.0000")
  })
  
  output$download_table <- downloadHandler(
    filename = function() {
           paste('treedata-', Sys.Date(), '.csv', sep='')
        },
         content = function(file) {
           write.csv(values[["DF"]], file, row.names=FALSE)
         }
  )
})
