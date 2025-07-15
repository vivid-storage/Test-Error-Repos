library(shiny)
library(GenomicRanges)
library(SummarizedExperiment)
library(BiocGenerics)
library(AnnotationDbi)
library(edgeR)
library(GenomicFeatures)
library(ggplot2)
library(dplyr)

# Load a TxDb object using GenomicFeatures from AnnotationHub
txdb <- suppressWarnings(makeTxDbFromBiomart(
  biomart = "ensembl",
  dataset = "hsapiens_gene_ensembl",
  transcript_ids = NULL,
  circ_seqs = FALSE
))

shinyServer(function(input, output) {
  # Reactive expression to create GRanges object
  ranges <- reactive({
    GRanges(seqnames = input$chr, ranges = IRanges(start = input$start, end = input$end))
  })
  
  # Display summary of GRanges object
  output$range_summary <- renderPrint({
    summary(ranges())
  })
  
  # Display GRanges object as a table
  output$range_table <- renderTable({
    as.data.frame(ranges())
  })
  
  # Plot the ranges using ggplot2
  output$range_plot <- renderPlot({
    input$update  # Ensure the plot updates when the button is clicked
    
    # Create a data frame from GRanges
    df <- as.data.frame(ranges())
    
    # Generate a plot using ggplot2
    ggplot(df, aes(x = start, y = end)) +
      geom_point() +
      labs(title = "Genomic Ranges",
           x = "Start Position",
           y = "End Position") +
      theme_minimal()
  })
  
  # Generate a sample DGEList object for edgeR
  dgelist <- reactive({
    counts <- matrix(rnbinom(1000, mu = 10, size = 1), ncol = 5)
    group <- factor(c("Control", "Control", "Treatment", "Treatment", "Control"))
    DGEList(counts = counts, group = group)
  })
  
  # Display summary of edgeR DGEList object
  output$edger_summary <- renderPrint({
    summary(dgelist())
  })
  
  # Display summary of TxDb object
  output$genomicfeatures_summary <- renderPrint({
    summary(txdb)
  })
})
