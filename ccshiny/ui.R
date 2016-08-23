
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(rhandsontable)

shinyUI(fluidPage(

  # Application title
  titlePanel("Urban Forestry Carbon Calculator"),
  verticalLayout(
    rHandsontableOutput("hot", width=1000)),
    br(),
    downloadButton("download_table", "Download Table"),
    actionButton("calc_results", "Calculate!"),
    br(),
    fileInput("uploadedsheet", "Upload Spreadsheet")
))
