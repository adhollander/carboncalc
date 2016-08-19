
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
    rHandsontableOutput("hot", width=900)),
    br(),
    downloadButton("download_table", "Download Table"),
    actionButton("calc_results", "Calculate!")
  ))
  # Sidebar with a slider input for number of bins
#   sidebarLayout(
#     sidebarPanel(
#       sliderInput("bins",
#                   "Number of bins:",
#                   min = 1,
#                   max = 50,
#                   value = 30)
#     ),
# 
#     # Show a plot of the generated distribution
#     mainPanel(
#       plotOutput("distPlot")
#     )
#   )
#))
# 
# shinyUI(fluidPage(
#   titlePanel("Handsontable"),
#   sidebarLayout(
#     sidebarPanel(
#       helpText("Handsontable demo output. Column add/delete does work ",
#                "for tables with defined column properties, including type."),
#       radioButtons("useType", "Use Data Types", c("TRUE", "FALSE"))
#     ),
#     mainPanel(
#       rHandsontableOutput("hot", width = 500)
#     )
#   )
# ))
