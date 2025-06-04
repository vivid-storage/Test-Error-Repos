library(ComplexHeatmap)
library(InteractiveComplexHeatmap)
library(shiny)

data(rand_mat) # simply a random matrix
ht1 = Heatmap(rand_mat, name = "mat",
              show_row_names = FALSE, show_column_names = FALSE)
ht1 = draw(ht1)

ui = fluidPage(
  h3("Interactive ComplexHeatmap Shiny app"),
  p("This is an interactive heatmap visualization on a random matrix."),
  InteractiveComplexHeatmapOutput()
)

server = function(input, output, session) {
  makeInteractiveComplexHeatmap(input, output, session, ht1)
}

shinyApp(ui, server)
