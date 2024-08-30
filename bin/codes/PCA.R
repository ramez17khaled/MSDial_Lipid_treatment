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
required_packages <- c("dplyr", "tidyr", "readxl", "ggplot2", "ggrepel", "rgl", "limma", "reshape2")

# Install and load required packages
install_and_load(required_packages)

# Load required libraries
library(dplyr)
library(tidyr)
library(readxl)
library(ggplot2)
library(ggrepel)
library(rgl)
library(limma)
library(reshape2)

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
current_directory <- getwd()
parent_directory1 <- dirname(current_directory)
parent_directory <- dirname(parent_directory1)

metadata_path <- file.path(parent_directory, '02-Nico_metadata')
data_pathPOS <- file.path(parent_directory, '01-mzmlThermo', '1.1-Data_POS')
data_pathNEG <- file.path(parent_directory, '01-mzmlThermo', '1.1-Data_NEG')

meta_POS_path <- file.path(metadata_path, 'thermoPOS.csv')
POS_path <- file.path(data_pathPOS, '02.1-datafiltered_POS.csv')
output_POS_path <- file.path(parent_directory, '04-codeOutput', 'POS')

meta_NEG_path <- file.path(metadata_path, 'thermoNEG.csv')
NEG_path <- file.path(data_pathNEG, '02.1-datafiltered_NEG.csv')
output_NEG_path <- file.path(parent_directory, '04-codeOutput', 'NEG')

column <- "Duration"
label_column <- "Condition"
conditions <- "T,H,C2,C1,QC"
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

filtered_POSdata <- POS_main_data[POS_main_data$sample %in% filtred_POS_metadata$sample, ]
filtered_NEGdata <- NEG_main_data[NEG_main_data$sample %in% filtred_NEG_metadata$sample, ]
rownames(filtered_POSdata) <- filtered_POSdata[, 1]
filtered_POSdata <- filtered_POSdata[, -1]
rownames(filtered_NEGdata) <- filtered_NEGdata[, 1]
filtered_NEGdata <- filtered_NEGdata[, -1]

remove_zero_variance_columns <- function(data) {
  data <- apply(data, 2, as.numeric)
  data <- as.data.frame(data)
  variances <- apply(data, 2, var)
  zero_variance_columns <- names(variances[variances == 0])
  data_cleaned <- data[, variances != 0]
  return(data_cleaned)
}
remove_zero_variance_columns(filtered_POSdata)
remove_zero_variance_columns(filtered_NEGdata)

perform_pca <- function(data, meta_data, batch_column, label_column = NULL, log_transform = FALSE, filename = NULL, directory = NULL) {
  if (log_transform) {
    data <- log(data + 1)
  }
  data <- scale(data)
  pca_result <- prcomp(data)
  pc_scores <- as.data.frame(pca_result$x[, 1:3])
  pc_scores$batch <- meta_data[[batch_column]] 
  if (!is.null(label_column)) {
    pc_scores$label <- meta_data[[label_column]]
  }
  pca_plot <- ggplot(pc_scores, aes(x = PC1, y = PC2, color = batch)) +
    geom_point(size = 3) +
    labs(title = "PCA Plot", x = "PC1", y = "PC2") +
    theme_minimal() +
    theme(legend.position = "right")
  if (!is.null(label_column)) {
    pca_plot <- pca_plot + geom_text_repel(aes(label = label))
  }
  file_path <- file.path(directory, filename)
  print(paste("Saving plot to:", file_path))  
  ggsave(filename = file_path, plot = pca_plot, width = 10, height = 8, dpi = 300)
  return(pca_plot)
}
pca_plot_POS <- perform_pca(filtered_POSdata, filtred_POS_metadata, column,log_transform = TRUE, filename = "full_pca_plot_POS.png", directory = output_POS_path)
pca_plot_NEG <- perform_pca(filtered_NEGdata, filtred_NEG_metadata, column,log_transform = TRUE, filename = "full_pca_plot_NEG.png", directory = output_NEG_path)
pca_plot_POS
pca_plot_NEG

