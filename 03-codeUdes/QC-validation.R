# Function to install and load required packages
install_and_load <- function(packages) {
  for (pkg in packages) {
    if (!require(pkg, character.only = TRUE)) {
      install.packages(pkg, dependencies = TRUE)
      library(pkg, character.only = TRUE)
    }
  }
}

# List of required packages
required_packages <- c("Rtsne", "tidyr", "readxl", "ggplot2", "ggdendro", "scales", "vegan","proxy","dplyr")

# Install and load required packages
install_and_load(required_packages)

# Load required libraries
library(Rtsne)
library(tidyr)
library(dplyr)
library(readxl)
library(ggplot2)
library(ggdendro)
library(scales)
library(vegan)
library(proxy)

cat("PCA Analysis: Start\n")

# Function to read file based on type
read_file <- function(file_path, sheet_name = NULL) {
  # Check if file exists
  if (!file.exists(file_path)) {
    stop("File not found.")
  }
  
  # Extract file extension
  file_ext <- tools::file_ext(file_path)
  
  # Read file based on extension
  if (file_ext == "csv") {
    # Read CSV file
    data <- read.csv(file_path, stringsAsFactors = FALSE, sep = ';')
  }else {
    stop("Unsupported file format. Only CSV files are supported.")
  }
  
  return(data)
}

# Assign variables from config file
meta_POS_path <- "D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoPOS.csv"
POS_path <- "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_POS/02.1-datafiltered_POS.csv"
output_POS_path <- "D:/data/ThermoDataV2/V2/MSDial/04-codeOutput/POS"

meta_NEG_path <- "D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoNEG.csv"
NEG_path <- "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_NEG/02.1-datafiltered_NEG.csv"
output_NEG_path <- "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/NEG"

column <- "ID"
label_column <- "Condition"
conditions <- "QC1,QC2,QC3,QC4,QC5"
conditions <- strsplit(conditions, ",")[[1]]

meta_data_POS <- read_file(meta_POS_path)
meta_data_NEG <- read_file(meta_NEG_path)

POS_main_data <- read_file(POS_path)
NEG_main_data <- read_file(NEG_path)

filter_meta_data <- function(meta_data, column, conditions) {
  if (!is.data.frame(meta_data)) {
    stop("meta_data must be a data frame")
  }
  if (!is.character(column)) {
    stop("column must be a character vector")
  }
  if (!is.vector(conditions)) {
    stop("conditions must be a vector")
  }
  if (!(column %in% colnames(meta_data))) {
    stop(sprintf("Column '%s' not found in metadata.", column))
  }
  filtered_meta <- meta_data[meta_data[[column]] %in% conditions, , drop = FALSE]
  return(filtered_meta)
}

filtred_POS_metadata <- filter_meta_data(meta_data_POS,column,conditions)
filtred_NEG_metadata <- filter_meta_data(meta_data_NEG,column,conditions)

filtered_POSdata <- POS_main_data[POS_main_data$sample_name %in% filtred_POS_metadata$sample, ]
filtered_NEGdata <- NEG_main_data[NEG_main_data$sample_name %in% filtred_NEG_metadata$sample, ]
rownames(filtered_POSdata) <- filtered_POSdata[, 1]
filtered_POSdata <- filtered_POSdata[, -1]
rownames(filtered_NEGdata) <- filtered_NEGdata[, 1]
filtered_NEGdata <- filtered_NEGdata[, -1]

#Normalisation

normalized_df_POS <- as.data.frame(lapply(filtered_POSdata, scale))
rownames(normalized_df_POS) <-rownames(filtered_POSdata)
normalized_df_NEG <- as.data.frame(lapply(filtered_NEGdata, scale))
rownames(normalized_df_NEG) <-rownames(filtered_NEGdata)

#Calculate Pairwise Similarity Measures

distances_POS <- vegdist(normalized_df_POS, method = "euclidean")
distance_matrix_POS <- as.matrix(distances_POS)
correlation_matrix_POS <- cor(normalized_df_POS)
similarity_matrix_POS <- proxy::dist(normalized_df_POS, method = "cosine")

distances_NEG <- vegdist(normalized_df_NEG, method = "euclidean")
distance_matrix_NEG <- as.matrix(distances_NEG)
correlation_matrix_NEG <- cor(normalized_df_NEG)
similarity_matrix_NEG <- proxy::dist(normalized_df_NEG, method = "cosine")

#PCA

plot_pca_save <- function(data, output_path, file_name = 'pca_plot.png', center = TRUE, scale. = TRUE, title = 'PCA Plot', xlab = 'PC1', ylab = 'PC2') {
  pca_result <- prcomp(data, center = center, scale. = scale.)
  pca_df <- as.data.frame(pca_result$x)
  pca_df$sample <- rownames(data)
  p <- ggplot(pca_df, aes(x = PC1, y = PC2, label = sample)) +
    geom_point() +
    geom_text(vjust = -0.5, hjust = 0.5) +
    labs(title = title, x = xlab, y = ylab) +
    theme_minimal()
  file_path <- file.path(output_path, file_name)
  ggsave(filename = file_path, plot = p, width = 8, height = 6, dpi = 300)
  return(p)
}

plot_pca_save(normalized_df_POS, output_path = output_POS_path, file_name = 'pca_plot_POS.png', title = 'PCA of POS QC Samples')
plot_pca_save(normalized_df_NEG, output_path = output_NEG_path, file_name = 'pca_plot_NEG.png', title = 'PCA of NEG QC Samples')

#t-SNE

plot_tsne_save <- function(data, output_path, file_name = 'tsne_plot.png', perplexity = 30, title = 't-SNE Plot', xlab = 'tSNE1', ylab = 'tSNE2') {
  tsne_result <- Rtsne(data, dims = 2, pca = TRUE, check_duplicates = FALSE, perplexity = perplexity)
  tsne_df <- as.data.frame(tsne_result$Y)
  tsne_df$sample <- rownames(data)
  p <- ggplot(tsne_df, aes(x = V1, y = V2, label = sample)) +
    geom_point() +
    geom_text(vjust = -0.5, hjust = 0.5) +
    labs(title = title, x = xlab, y = ylab) +
    theme_minimal()
  file_path <- file.path(output_path, file_name)
  ggsave(filename = file_path, plot = p, width = 8, height = 6, dpi = 300)
  return(p)
}

plot_tsne_save(normalized_df_POS, output_path = output_POS_path, file_name = 'tsne_plot_POS.png', perplexity = 1, title = 't-SNE of POS QC Samples')
plot_tsne_save(normalized_df_NEG, output_path = output_NEG_path, file_name = 'tsne_plot_NEG.png', perplexity = 1, title = 't-SNE of NEG QC Samples')

#Clustering Analysis

plot_dendrogram <- function(distances, method = 'ward.D2', plot_title = 'Hierarchical Clustering Dendrogram',output_dir  = NULL, filename = 'dendrogram_plot.png') {
  hc <- hclust(distances, method = method)
  dendrogram_data <- ggdendro::dendro_data(hc, type = "rectangle")
  p <- ggplot() +
    geom_segment(data = dendrogram_data$segments, aes(x = x, xend = xend, y = y, yend = yend), color = "black") +
    geom_text(data = dendrogram_data$labels, aes(x = x, y = y, label = label), size = 2.3, hjust = 1, angle = 90) +
    labs(title = plot_title,
         x = 'Samples',
         y = 'Height') +
    theme_minimal() +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text.x = element_text(size = 10, angle = 90, hjust = 1),
      axis.text.y = element_text(size = 10),
      axis.title = element_text(size = 12, face = "bold"),
      plot.title = element_text(size = 14, face = "bold"),
      plot.margin = unit(c(1,1,1,1), "cm")
    )
  full_path <- file.path(output_dir, filename)
  ggsave(filename = full_path, plot = p, width = 10, height = 8, dpi = 300)
  return(p)
}

plot_dendrogram(distances_POS,plot_title = 'Hierarchical Clustering POS Dendrogram', output_dir  = output_POS_path, filename = 'POS_dendrogram_plot.png')
plot_dendrogram(distances_NEG,plot_title = 'Hierarchical Clustering NEG Dendrogram', output_dir  = output_NEG_path, filename = 'NEG_dendrogram_plot.png')

#boxplot 

boxPlotSignificant <- function(df, output_dir = NULL, filename = 'boxplot_significant.png') {
  df <- df %>%
    tibble::rownames_to_column(var = "condition")
  df_melt <- df %>%
    pivot_longer(cols = -condition, names_to = 'metabolite', values_to = 'intensity') %>%
    mutate(intensity_log = log(intensity))
  p <-ggplot(df_melt, aes(x = condition, y = intensity_log, fill = condition)) +
    geom_boxplot() +
    scale_x_discrete(labels = function(x) { toupper(x) }) +
    ylab("Log Intensity") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))
  print(p)
  full_path <- file.path(output_dir, filename)
  ggsave(filename = full_path, plot = p, width = 10, height = 8, dpi = 300)
}

boxPlotSignificant(filtered_POSdata, output_dir=output_POS_path, filename='POS_QC_boxplot.png')
boxPlotSignificant(filtered_NEGdata, output_dir=output_NEG_path, filename='NEG_QC_boxplot.png')
