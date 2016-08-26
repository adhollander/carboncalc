
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(rhandsontable)

shinyUI(fluidPage(

  # Application title
#   titlePanel("Urban Forestry Carbon Calculator"),
#   verticalLayout(
#     rHandsontableOutput("hot", width=1000)),
#     br(),
#     downloadButton("download_table", "Download Table"),
#     actionButton("calc_results", "Calculate!"),
#     br(),
#     fileInput("uploadedsheet", "Upload Spreadsheet")
# ))
  titlePanel("Urban Forestry Carbon Calculator"),
  tabsetPanel(
      tabPanel("Biomass/Growth", 
        fluidRow(
          column(7,
          rHandsontableOutput("hot", height=300),
          br(),
          actionButton("calc_results", "Calculate!"),
          br(),
          flowLayout(
          downloadButton("download_table", "Download Table"),
          fileInput("uploadedsheet", "Upload Spreadsheet"))),
        column(5, h2("Intro text")))),
      tabPanel("Buildings", h2("Building stuff")),
      tabPanel("Future growth", h2("Future tree characteristics")),
      tabPanel("Future energy", h2("Future building energy characteristics")),
      tabPanel("Graphs", h2("Some graphs"))
  )))