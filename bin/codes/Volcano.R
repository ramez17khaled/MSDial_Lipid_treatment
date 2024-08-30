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
required_packages <- c("dplyr", "tidyr", "readxl", "ggplot2", "ggrepel","tibble", "VennDiagram")

# Print process start message
cat("Process started.\n")

# Install and load required packages
install_and_load(required_packages)

# Load required libraries
library(dplyr)
library(tidyr)
library(readxl)
library(ggplot2)
library(ggrepel)
library(tibble)
library(VennDiagram)

# Print message on package loading completion
cat("Packages loaded successfully.\n")

# Function to read file
read_file <- function(file_path, sheet_name = NULL) {
  if (!file.exists(file_path)) {
    stop("File not found.")
  }
  file_ext <- tools::file_ext(file_path)
  if (file_ext == "csv") {
    data <- read.csv(file_path, stringsAsFactors = FALSE, sep = ';')
  }else {
    stop("Unsupported file format. Only CSV files are supported.")
  }
  
  return(data)
}

# Read input file paths and conditions from config.txt
#config_file <- "config.txt"
#config <- read.table(config_file, sep = "=", stringsAsFactors = FALSE, strip.white = TRUE)

# Assign variables from config file
#meta_file_path <- trimws(config[grepl("^meta_file_path", config$V1), "V2"])
#file_path <- trimws(config[grepl("^file_path", config$V1), "V2"])
#sheet <- trimws(config[grepl("^sheet", config$V1), "V2"])
#output_path <- trimws(config[grepl("^output_path", config$V1), "V2"])
#method <- trimws(config[grepl("^method", config$V1), "V2"])
#column <- trimws(config[grepl("^column", config$V1), "V2"])
#conditions <- trimws(config[grepl("^conditions", config$V1), "V2"])

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
  
column <- 'Duration'
conditions1 <-"C2,T"
conditions2 <-"C1,H"
#conditions1 <- strsplit(conditions1, ",")[[1]]
#conditions2 <- strsplit(conditions2, ",")[[1]]

cat("Loading metadata...\n")
meta_data_POS <- read_file(meta_POS_path)
meta_data_NEG <- read_file(meta_NEG_path)

cat("Loading main data...\n")
POS_main_data <- read_file(POS_path)
NEG_main_data <- read_file(NEG_path)

process_and_merge_data <- function(meta_data_POS, meta_data_NEG, POS_main_data, NEG_main_data, column, conditions1, conditions2) {

  filter_meta_data <- function(meta_data, column, conditions) {

    conditions_list <- strsplit(conditions, ",")[[1]]

    filtered_metadata <- meta_data %>%
      filter(get(column) %in% conditions_list)
    return(filtered_metadata)
  }
  
  filtred_POS_metadata1 <- filter_meta_data(meta_data_POS, column, conditions1)
  filtred_POS_metadata2 <- filter_meta_data(meta_data_POS, column, conditions2)
  filtred_NEG_metadata1 <- filter_meta_data(meta_data_NEG, column, conditions1)
  filtred_NEG_metadata2 <- filter_meta_data(meta_data_NEG, column, conditions2)
  
  filtered_POSdata1 <- POS_main_data[POS_main_data$sample %in% filtred_POS_metadata1$sample, ]
  filtered_POSdata2 <- POS_main_data[POS_main_data$sample %in% filtred_POS_metadata2$sample, ]
  filtered_NEGdata1 <- NEG_main_data[NEG_main_data$sample %in% filtred_NEG_metadata1$sample, ]
  filtered_NEGdata2 <- NEG_main_data[NEG_main_data$sample %in% filtred_NEG_metadata2$sample, ]
  
  rownames(filtered_POSdata1) <- filtered_POSdata1[, 1]
  filtered_POSdata1 <- filtered_POSdata1[, -1]
  
  rownames(filtered_POSdata2) <- filtered_POSdata2[, 1]
  filtered_POSdata2 <- filtered_POSdata2[, -1]
  
  rownames(filtered_NEGdata1) <- filtered_NEGdata1[, 1]
  filtered_NEGdata1 <- filtered_NEGdata1[, -1]
  
  rownames(filtered_NEGdata2) <- filtered_NEGdata2[, 1]
  filtered_NEGdata2 <- filtered_NEGdata2[, -1]
  
  cat("Data filtered successfully.\n")
  
  merge_with_metadata <- function(data_df, filtered_metadata) {
    data_df <- data_df %>%
      tibble::rownames_to_column(var = "index") %>%
      rename(sample = index)
    merged_df <- data_df %>%
      left_join(filtered_metadata %>% select(sample, column), 
                by = "sample")
    merged_df <- merged_df %>%
      column_to_rownames(var = "sample")
    
    return(merged_df)
  }
  
  merged_POS_data1 <- merge_with_metadata(filtered_POSdata1, filtred_POS_metadata1)
  merged_POS_data2 <- merge_with_metadata(filtered_POSdata2, filtred_POS_metadata2)
  merged_NEG_data1 <- merge_with_metadata(filtered_NEGdata1, filtred_NEG_metadata1)
  merged_NEG_data2 <- merge_with_metadata(filtered_NEGdata2, filtred_NEG_metadata2)
  
  return(list(
    merged_POS_data1 = merged_POS_data1,
    merged_POS_data2 = merged_POS_data2,
    merged_NEG_data1 = merged_NEG_data1,
    merged_NEG_data2 = merged_NEG_data2
  ))
}

result <- process_and_merge_data(meta_data_POS, meta_data_NEG, POS_main_data, NEG_main_data, column, conditions1, conditions2)

merged_POS_data1<-result$merged_POS_data1
merged_POS_data2<-result$merged_POS_data2
merged_NEG_data1<-result$merged_NEG_data1
merged_NEG_data2<-result$merged_NEG_data2

# Function to generate volcano plot
generate_volcano_plot <- function(data, condition1_col, condition1_val, condition2_col, condition2_val, title) {
  metabolite_data <- colnames(data)[!colnames(data) %in% c(condition1_col, condition2_col)]

  condition1_data <- data %>% filter(!!sym(condition1_col) == condition1_val)
  condition1_data <- condition1_data %>%
    select(-one_of(condition1_col))
  condition1_data <- lapply(condition1_data, function(col) {
    as.numeric(col)
  })

  condition2_data <- data %>%
    filter(!!sym(condition2_col) == condition2_val)
  condition2_data <- condition2_data %>%
    select(-one_of(condition2_col))
  condition2_data <- lapply(condition2_data, function(col) {
    as.numeric(col)
  })

  fold_change <- sapply(metabolite_data, function(col) {
    mean_condition1 <- mean(condition1_data[[col]], na.rm = TRUE)
    mean_condition2 <- mean(condition2_data[[col]], na.rm = TRUE)
    fold_change <- mean_condition2 / mean_condition1
    return(fold_change)
  })
  
  fold_change_df <- data.frame(Metabolite = names(fold_change), Fold_Change = fold_change)

  p_values <- sapply(metabolite_data, function(col) {
    if (length(unique(condition1_data[[col]])) < 2 || length(unique(condition2_data[[col]])) < 2) {
      return(NA) 
    }
    t_test_result <- tryCatch({
      t.test(condition1_data[[col]], condition2_data[[col]])$p.value
    }, error = function(e) {
      return(NA)  
    })
    return(t_test_result)
  })
  
  p_values_df <- data.frame(Metabolite = names(p_values), P_Value = p_values)

  volcano_df <- merge(p_values_df, fold_change_df, by = "Metabolite")
  volcano_df$log2FoldChange <- log2(volcano_df$Fold_Change)

  volcano_df$diffexpressed <- "NO"
  volcano_df$diffexpressed[volcano_df$log2FoldChange > 0.3 & volcano_df$P_Value < 0.05] <- "UP"
  volcano_df$diffexpressed[volcano_df$log2FoldChange < -0.3 & volcano_df$P_Value < 0.05] <- "DOWN"

  cat("Generating volcano plot...\n")
  volcano_plot <- ggplot(volcano_df, aes(x = log2FoldChange, y = -log10(P_Value), col = diffexpressed, label = Metabolite)) +
    geom_vline(xintercept = c(-0.3, 0.3), col = "gray", linetype = 'dashed') +
    geom_hline(yintercept = -log10(0.05), col = "gray", linetype = 'dashed') +
    geom_point(size = 1) +
    geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "orange") + # Add significance threshold line
    labs(color = 'Severe', x = "log2(FC)", y = "-log10(P-Value)", title = title) +
    theme_minimal() +
    theme(panel.background = element_rect(fill = "white", color = NA)) +
    scale_color_manual(values = c("blue", "gray", "red"),
                       labels = c("Downregulated", "Not significant", "Upregulated"))
  
  return(list(volcano_plot = volcano_plot, volcano_data = volcano_df))
}

sconditions1 <- strsplit(conditions1, ",")[[1]]
sconditions2 <- strsplit(conditions2, ",")[[1]]

volcano_POS_results1 <- generate_volcano_plot(merged_POS_data1, column, sconditions1[1], column, sconditions1[2],conditions1)
volcano_POS_plot1 <- volcano_POS_results1$volcano_plot
volcano_POS_data1 <- volcano_POS_results1$volcano_data
volcano_POS_results2 <- generate_volcano_plot(merged_POS_data2, column, sconditions2[1], column, sconditions2[2],conditions2)
volcano_POS_plot2 <- volcano_POS_results2$volcano_plot
volcano_POS_data2 <- volcano_POS_results2$volcano_data

volcano_NEG_results1 <- generate_volcano_plot(merged_NEG_data1, column, sconditions1[1], column, sconditions1[2],conditions1)
volcano_NEG_plot1 <- volcano_NEG_results1$volcano_plot
volcano_NEG_data1 <- volcano_NEG_results1$volcano_data
volcano_NEG_results2 <- generate_volcano_plot(merged_NEG_data2, column, sconditions2[1], column, sconditions2[2],conditions2)
volcano_NEG_plot2 <- volcano_NEG_results2$volcano_plot
volcano_NEG_data2 <- volcano_NEG_results2$volcano_data

POS_output_file1 <- paste0(output_POS_path, "/volcano_POS1.csv")
write.csv(volcano_POS_data1, file = POS_output_file1, row.names = FALSE)
POS_output_file2 <- paste0(output_POS_path, "/volcano_POS2.csv")
write.csv(volcano_POS_data2, file = POS_output_file2, row.names = FALSE)
POS_output_plot1 <- paste0(output_POS_path, "/volcano_plotPOS1.png")
ggsave(filename = POS_output_plot1, plot = volcano_POS_plot1, device = "png")
POS_output_plot2 <- paste0(output_POS_path, "/volcano_plotPOS2.png")
ggsave(filename = POS_output_plot2, plot = volcano_POS_plot2, device = "png")


NEG_output_file1 <- paste0(output_NEG_path, "/volcano_NEG1.csv")
write.csv(volcano_NEG_data1, file = NEG_output_file1, row.names = FALSE)
NEG_output_file2 <- paste0(output_NEG_path, "/volcano_NEG2.csv")
write.csv(volcano_NEG_data2, file = NEG_output_file2, row.names = FALSE)
NEG_output_plot1 <- paste0(output_NEG_path, "/volcano_plotNEG1.png")
ggsave(filename = NEG_output_plot1, plot = volcano_NEG_plot1, device = "png")
NEG_output_plot2 <- paste0(output_NEG_path, "/volcano_plotNEG2.png")
ggsave(filename = NEG_output_plot2, plot = volcano_NEG_plot2, device = "png")

cat("Volcano plot generated successfully for conditions:", conditions1, "\n")
cat("Volcano plot generated successfully for conditions:", conditions2, "\n")
cat ('DONE!')



