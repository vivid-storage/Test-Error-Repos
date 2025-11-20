library(shiny)
library(ggplot2)
library(naniar)

# Define UI for application
ui <- fluidPage(
  titlePanel("Simple Shiny App using naniar"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("obs",
                  "Number of observations:",
                  min = 1,
                  max = 1000,
                  value = 500)
    ),
    mainPanel(
      plotOutput("missPlot")
    )
  )
)

# Define server logic
server <- function(input, output) {
  output$missPlot <- renderPlot({
    # Generate a random dataset with missing values
    set.seed(123)
    data <- data.frame(
      x = rnorm(input$obs),
      y = rnorm(input$obs)
    )
    data[sample(1:input$obs, 50), "x"] <- NA
    data[sample(1:input$obs, 30), "y"] <- NA
    
    # Create a missingness plot using naniar
    gg_miss_var(data)
  })
}

# Run the application
shinyApp(ui = ui, server = server)
