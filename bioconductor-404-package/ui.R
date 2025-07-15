library(shiny)

shinyUI(fluidPage(
  titlePanel("Shiny with CRAN and Bioconductor Packages"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("CRAN and Bioconductor packages."),
      selectInput("chr", "Select Chromosome:", choices = c("chr1", "chr2", "chr3")),
      numericInput("start", "Start Position:", value = 1, min = 1),
      numericInput("end", "End Position:", value = 1000, min = 1),
      actionButton("update", "Update Plot")
    ),
    
    mainPanel(
      verbatimTextOutput("range_summary"),
      tableOutput("range_table"),
      plotOutput("range_plot"),
      verbatimTextOutput("edger_summary"),
      verbatimTextOutput("genomicfeatures_summary")
    )
  )
))
