required_packages <- c("dplyr", "tidyr", "readxl", "ggplot2", "ggrepel","tibble", "pheatmap")

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
library(pheatmap)
library(purrr)

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

meta_POS_path <-"D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoPOS.csv"
POS_path <-"D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_POS/02.1-datafiltered_POS.csv"
output_POS_path <-"D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/POS"

meta_NEG_path <-"D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoNEG.csv"
NEG_path <-"D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_NEG/02.1-datafiltered_NEG.csv"
output_NEG_path <-"D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/NEG"

column <- 'Duration'
conditions1 <-"T"
conditions2 <-"H"
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
  
  filtered_POSdata1 <- POS_main_data[POS_main_data$sample_name %in% filtred_POS_metadata1$sample, ]
  filtered_POSdata2 <- POS_main_data[POS_main_data$sample_name %in% filtred_POS_metadata2$sample, ]
  filtered_NEGdata1 <- NEG_main_data[NEG_main_data$sample_name %in% filtred_NEG_metadata1$sample, ]
  filtered_NEGdata2 <- NEG_main_data[NEG_main_data$sample_name %in% filtred_NEG_metadata2$sample, ]
  
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

melting <- function(df, condion_column = column) {
  melted_df <- df %>%
    pivot_longer(
      cols = -all_of(condion_column),  # Exclude the condition column
      names_to = 'Metabolite',       # Name of the metabolite
      values_to = 'Intensity'        # Intensity values
    ) %>%
    mutate(Condition = get(condion_column)) %>% # Add condition column
    select(Metabolite, Intensity, Condition)  # Select required columns
  
  return(melted_df)
}

melt_POS_data1 <- melting(merged_POS_data1)
melt_POS_data2 <- melting(merged_POS_data2)
melt_NEG_data1 <- melting(merged_NEG_data1)
melt_NEG_data2 <- melting(merged_NEG_data2)

visualize_common_metabolites <- function(df1, 
                                         df2, 
                                         condition1_name = 'Condition1',
                                         condition2_name = 'Condition2',
                                         Delta = 2,
                                         Threshold = 10,
                                         output_dir = '.', 
                                         output_file_heatmap_common = 'heatmap_common_metabolites.png',
                                         output_file_heatmap_different = 'heatmap_different_metabolites.png',
                                         output_file_heatmap_commfilt = 'heatmap_commun_high_int_metabolites.png',
                                         output_file_common_csv = 'common_metabolites.csv',
                                         output_file_diff_csv = 'different_metabolites.csv',
                                         output_file_heatmap_commfilt_csv = 'common_high_int_metabolites.csv') {
  
  common_metabolites <- intersect(df1$Metabolite, df2$Metabolite)
  
  df1_common <- df1 %>% filter(Metabolite %in% common_metabolites)
  df2_common <- df2 %>% filter(Metabolite %in% common_metabolites)
  
  combined_df <- df1_common %>%
    inner_join(df2_common, by = 'Metabolite', suffix = c('_cond1', '_cond2'))
  
  heatmap_data <- combined_df %>%
    select(Metabolite, Condition_cond1, Condition_cond2, Intensity_cond1, Intensity_cond2) %>%
    pivot_longer(cols = starts_with('Intensity'), 
                 names_to = 'Condition_Type', 
                 values_to = 'Intensity') %>%
    mutate(
      Condition = ifelse(grepl('1$', Condition_Type), Condition_cond1, Condition_cond2)
    ) %>%
    select(Metabolite, Condition, Intensity) %>%
    pivot_wider(names_from = Condition, values_from = Intensity, names_prefix = 'Condition_') %>%
    rename_with(~ gsub("Condition_", "", .), starts_with("Condition_"))
  
  heatmap_data <- heatmap_data %>%
    rowwise() %>%
    mutate(
      Avg_Condition1 = mean(c_across(all_of(condition1_name)), na.rm = TRUE),
      Avg_Condition2 = mean(c_across(all_of(condition2_name)), na.rm = TRUE)
    ) %>%
    select(Metabolite, Avg_Condition1, Avg_Condition2)
  
  log_transform <- function(x) {
    log(x + 1)
  }
  
  heatmap_data_transformed <- heatmap_data %>%
    mutate(
      Avg_condition1 = map_dbl(Avg_Condition1, log_transform),  
      Avg_condition2 = map_dbl(Avg_Condition2, log_transform)    
    ) %>%
    select(Metabolite, Avg_condition1, Avg_condition2)
  
  heatmap_data_final <- as.data.frame(heatmap_data_transformed)
  
  heatmap_data_final <- heatmap_data_final %>%
    rename(
      !!condition1_name := Avg_condition1,
      !!condition2_name := Avg_condition2
    )
  
  heatmap_data_final <- heatmap_data_final %>%
    rowwise() %>%
    mutate(
      delta = abs(get(condition1_name) - get(condition2_name))
    )

  common_df <- heatmap_data_final %>% filter(delta <= Delta)
  different_df <- heatmap_data_final %>% filter(delta > Delta)
  common_filtered_df <- common_df %>%
    filter(
      !!sym(condition1_name) > Threshold |
        !!sym(condition2_name) > Threshold
    )
  
  heatmap_matrix_common <- common_df %>%
    select(-Metabolite, -delta) %>%
    as.matrix()
  colnames(heatmap_matrix_common) <- colnames(common_df %>% select(-Metabolite, -delta))
  
  heatmap_matrix_diff <- different_df %>%
    select(-Metabolite, -delta) %>%
    as.matrix()
  colnames(heatmap_matrix_diff) <- colnames(different_df %>% select(-Metabolite, -delta))
  
  heatmap_matrix_comfilt <- common_filtered_df %>%
    select(-Metabolite, -delta) %>%
    as.matrix()
  colnames(heatmap_matrix_comfilt) <- colnames(common_filtered_df %>% select(-Metabolite, -delta))
  
  annotation_common <- data.frame(Condition = colnames(heatmap_matrix_common))
  rownames(annotation_common) <- colnames(heatmap_matrix_common)
  
  annotation_diff <- data.frame(Condition = colnames(heatmap_matrix_diff))
  rownames(annotation_diff) <- colnames(heatmap_matrix_diff)
  
  annotation_commfilt <- data.frame(Condition = colnames(heatmap_matrix_comfilt))
  rownames(annotation_commfilt) <- colnames(heatmap_matrix_comfilt)
  
  pheatmap(heatmap_matrix_common, filename = file.path(output_dir, output_file_heatmap_common), 
           main = 'Heatmap of Common Metabolites Intensities', 
           color = colorRampPalette(c("blue", "white", "red"))(50),
           annotation_col = annotation_common)
  
  pheatmap(heatmap_matrix_diff, filename = file.path(output_dir, output_file_heatmap_different), 
           main = 'Heatmap of Different Metabolites Intensities', 
           color = colorRampPalette(c("blue", "white", "red"))(50),
           annotation_col = annotation_diff)
  
  pheatmap(heatmap_matrix_comfilt, filename = file.path(output_dir, output_file_heatmap_commfilt), 
           main = 'Heatmap of Metabolites with High Intensities', 
           color = colorRampPalette(c("blue", "white", "red"))(50),
           annotation_col = annotation_commfilt)
  
  common_df_clean <- common_df %>%
    mutate(across(where(is.list), ~ unlist(.)))
  
  different_df_clean <- different_df %>%
    mutate(across(where(is.list), ~ unlist(.)))
  
  common_filtered_df_clean <- common_filtered_df %>%
    mutate(across(where(is.list), ~ unlist(.)))
  
  write.csv(common_df_clean, file = file.path(output_dir, output_file_common_csv), row.names = FALSE)
  write.csv(different_df_clean, file = file.path(output_dir, output_file_diff_csv), row.names = FALSE)
  write.csv(common_filtered_df_clean, file = file.path(output_dir, output_file_heatmap_commfilt_csv), row.names = FALSE)
  
  return(list(common = common_df, different = different_df, common_high_int = common_filtered_df))
}


commun_POS_data <- visualize_common_metabolites(melt_POS_data1,melt_POS_data2,
                                                condition1_name = 'T',
                                                condition2_name = 'H',
                                                Delta = 2,
                                                Threshold = 16,
                                                output_dir = output_POS_path, 
                                                output_file_heatmap_common = 'heatmap_common_metabolites_T-H.png',
                                                output_file_heatmap_different = 'heatmap_different_metabolites_T-H.png',
                                                output_file_heatmap_commfilt = 'heatmap_commun hign int_metabolites_T-H.png',
                                                output_file_common_csv = 'common_metabolites_T-H.csv',
                                                output_file_diff_csv = 'different_metabolites_T-H.csv',
                                                output_file_heatmap_commfilt_csv = 'common_higt_int_metabolites_T-H.csv')

commun_NEG_data <- visualize_common_metabolites(melt_NEG_data1,melt_NEG_data2,
                                                condition1_name = 'T',
                                                condition2_name = 'H',
                                                Delta = 2,
                                                Threshold = 12,
                                                output_dir = output_NEG_path, 
                                                output_file_heatmap_common = 'common_metabolites_T-H.png',
                                                output_file_heatmap_different = 'different_metabolites_T-H.png',
                                                output_file_heatmap_commfilt = 'commun_hign_int_metabolites_T-H.png',
                                                output_file_common_csv = 'common_metabolites_T-H.csv',
                                                output_file_diff_csv = 'different_metabolites_T-H.csv',
                                                output_file_heatmap_commfilt_csv = 'common_higt_int_metabolites_T-H.csv')




