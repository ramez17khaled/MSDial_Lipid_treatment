library(limma)
library(tidyverse)
library(ggplot2)
library(ggrepel)
library(ggforce)

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

dataPOS <-read_file (InputcsvFilePOS)
dataNEG <-read_file (InputcsvFileNEG)


# Pivot the data to long format
POS_long <- pivot_longer(dataPOS,cols = starts_with("M"),
                         names_to = "Metabolite",
                         values_to = "Intensity")

# Extract the intensity values
expression_data <- POS_long$Intensity

# Extract batch information
batch <- dataPOS$batch

num_samples <- length(batch)
num_metabolites <- length(expression_data) / num_samples
expression_matrix <- matrix(expression_data, nrow = num_metabolites, ncol = num_samples, byrow = TRUE)

# Perform batch effect removal
dataPOS_corrected <- removeBatchEffect(expression_matrix, batch)

pca_dataPOS <- prcomp(t(dataPOS_corrected), scale = TRUE)

# PCA_POS dataframe creation
pca_dataPOS <- as.data.frame(pca_dataPOS$x)
pca_dataPOS$Etude <- dataPOS$Etude 
pca_dataPOS$sample_name <- dataPOS$sample_name
pca_dataPOS$Condition <- dataPOS$Condition
pca_dataPOS$ID <- dataPOS$ID
pca_dataPOS$Duration <- dataPOS$Duration
pca_dataPOS$SampleType <- dataPOS$SampleType
pca_dataPOS$batch <- dataPOS$batch
fpca_dataPOS = subset(pca_dataPOS, SampleType %in% c( 'QCDil', 'QC', 'blank','sample'))

# PCA processing
sample_colors <- c("sample" = "blue", "QC"="red", "QCDil"="orange", "blank" = "black")
condition_colore <- c("T2D" = "blue", "Controle"="red", "Hirschsprung's disease"="orange")
batch_colore <- c("b1" = "blue", "b2"="red", "b3"="orange","b4"="green")

# PCA pot creation
p_POS <- ggplot(fpca_dataPOS, aes(x = PC1, y = PC2, color = batch, label = Duration)) +
  geom_point() +
  xlab("PC1") + ylab("PC2") +
  ggtitle("Corr PCA POS") +
  scale_color_manual(values = batch_colore)  + 
  theme_minimal()+
  geom_text_repel(max.overlaps = Inf)
print(p_POS)
