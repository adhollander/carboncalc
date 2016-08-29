
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
          column(12, h2("Introduction"),
                 p("The Urban Forestry Carbon Calculator is designed to help urban foresters estimate climate change benefits from their trees."))),
        fluidRow(
          br(),
          column(12, rHandsontableOutput("hot", height=300, width=900))),
        fluidRow(
          column(1, actionButton("calc_results", "Calculate!")),
          column(2, offset=1,
             verticalLayout(
              downloadButton("download_table", "Download Table"),
              fileInput("uploadedsheet", "Upload Spreadsheet"))),
          column(7, offset=1,
             verticalLayout(
               checkboxInput("future_values", "Compute future values"),
               numericInput("num_years", "Number of years", value=10, min=0, max=100)
             )))),
      tabPanel("Buildings", h2("Building stuff")),
      tabPanel("Future growth", h2("Future tree characteristics")),
      tabPanel("Future energy", h2("Future building energy characteristics")),
      tabPanel("Graphs", h2("Some graphs"))
  )))