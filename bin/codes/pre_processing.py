from tools import *
import os

current_directory = os.getcwd()
parent_directory1 = os.path.dirname(current_directory)
parent_directory = os.path.dirname(parent_directory1)
output_path_POS = os.path.join(parent_directory, '01-mzmlThermo', '1.1-Data_POS')
output_path_NEG = os.path.join(parent_directory, '01-mzmlThermo', '1.1-Data_NEG')
metadata_path_POS = os.path.join(parent_directory, '02-Nico_metadata')
metadata_df_POS = os.path.join(metadata_path_POS, 'thermoPOS.csv')
metadata_path_NEG = os.path.join(parent_directory, '02-Nico_metadata')
metadata_df_NEG = os.path.join(metadata_path_NEG, 'thermoNEG.csv')


dataPOS, dataNEG, metadataPOSDatai, metadataNEGDatai=  reading_alignData(output_path_POS, output_path_NEG, metadata_df_POS, metadata_df_NEG)

dataPOS = pd.DataFrame(dataPOS)
dataNEG = pd.DataFrame(dataNEG)


dataPOS = dataPOS.iloc[3:]
dataPOS = dataPOS.drop(dataPOS.columns[4:32], axis=1)
dataPOS = dataPOS.drop(columns=[dataPOS.columns[0], "Unnamed: 3"])
dataPOS = dataPOS.rename(columns=dataPOS.iloc[0]).drop(dataPOS.index[0])
dataPOS = dataPOS.reset_index(drop=True)
dataPOS = dataPOS.rename(columns={"Average Rt(min)": "Rt(min)", "Average Mz": "Mz"})

dataNEG = dataNEG.iloc[3:]
dataNEG = dataNEG.drop(dataNEG.columns[4:32], axis=1)
dataNEG = dataNEG.drop(columns=[dataNEG.columns[0], "Unnamed: 3"])
dataNEG = dataNEG.rename(columns=dataNEG.iloc[0]).drop(dataNEG.index[0])
dataNEG = dataNEG.reset_index(drop=True)
dataNEG = dataNEG.rename(columns={"Average Rt(min)": "Rt(min)", "Average Mz": "Mz"})

print(f'dataPOS is \n{len(dataPOS)}')
print (f'dataNEG is \n{len (dataNEG)}')
##POS

#creating metabolite column start with M
dataPOS = add_metabolite_column(dataPOS)
excludDataPOS = ['Rt(min)', 'Mz']
fdataPOS = filter_column(dataPOS, exclude=excludDataPOS)
#transposing => metabolites as columns name
tdataPOS = transpose_data(fdataPOS, 'metabolite')
#exclud machine blc
#exludRawPOS = exludRawPOS = ["sample_name == '240326JSO_POS_blc01'","sample_name == '240326JSO_POS_ISTD01'","sample_name == '240326JSO_POS_ISTD02'","sample_name == '240326JSO_POS_ISTD03'"]
#ftdataPOS = filter_rows (tdataPOS,exclude=exludRawPOS)
#metadata merging 
excludDataPOS = ['id natif', 'class', 'injectionOrder']
metadataPOSData = metadataPOSDatai
metadataPOSData = filter_column(metadataPOSData,exclude=excludDataPOS)
metadataPOSData.set_index('sample', inplace = True)
start_dataPOS = merge_data(tdataPOS, metadataPOSData)
print (f'startDataPos is \n {start_dataPOS.shape}')
# blank filtering 0 besed
blank_filtered_dataPOS= blank_filter(start_dataPOS, operation='!=', threshold=0)
print (f'blank_filtered_dataPOS is \n {blank_filtered_dataPOS.shape}')
# QC filtering: if 0 in 3/4 QC elimined
QC_blank_filterPOS = QC_filter (blank_filtered_dataPOS, 0)
QC_blank_filterPOS.index.name = 'sample'
print (f'QC_blank_filterPOS is \n {QC_blank_filterPOS.shape}')
# QCDil filtering CV <=10 elimined
raw_list = ["sample == 'QC_dil2_01'", "sample == 'QC_dil4_01'" , "sample == 'QC_dil8_01'"]
QCDil_QC_blank_filterPOS = cv_filter (QC_blank_filterPOS, raw_list, 10, "<=")
print (f'QCDil_QC_blank_filterPOS is \n {QCDil_QC_blank_filterPOS.shape}')
# metadata merging for filtered data
metacol=['class','SampleType', 'injectionOrder', 'id natif ']
metadataPOSDataf=filter_column(metadataPOSDatai,exclude=metacol)
metadataPOSDataf.set_index('sample', inplace = True)
QCDil_QC_blank_filterPOSf = merge_data(QCDil_QC_blank_filterPOS, metadataPOSDataf)
print (f'QCDil_QC_blank_filterPOSf is \n {QCDil_QC_blank_filterPOSf.shape}')
# caving in a csv
output_pathPOS = save_as_csv(QCDil_QC_blank_filterPOS, output_dir=output_path_POS, output_file="02.1-datafiltered_POS", file_conflict="replace")
print("CSV file saved at:", output_path_POS)


##NEG

#creating metabolite column start with M
dataNEG = add_metabolite_column(dataNEG)
excludDataNEG = ['Rt(min)', 'Mz']
fdataNEG = filter_column(dataNEG, exclude=excludDataNEG)
#transposing => metabolites as columns name
tdataNEG = transpose_data(fdataNEG, 'metabolite')
#exclud machine blc
#exludRawNEG = ["sample_name == '240326JSO_NEG_ISTD05'","sample_name == '240326JSO_NEG_ISTD06'","sample_name == '240326JSO_NEG_blc03'"]
#ftdataNEG = filter_rows (tdataNEG,exclude=exludRawNEG)
#metadata merging 
excludDataNEG = ['id natif', 'class', 'injectionOrder']
metadataNEGData = metadataNEGDatai
metadataNEGData = filter_column(metadataNEGData,exclude=excludDataNEG)
metadataNEGData.set_index('sample', inplace = True)
start_dataNEG = merge_data(tdataNEG, metadataNEGData)
print (f'start_dataNEG is \n {start_dataNEG.shape}')
# blank filtering 0 besed
blank_filtered_dataNEG= blank_filter(start_dataNEG, operation='!=', threshold=0)
print (f'blank_filtered_dataNEG is \n {blank_filtered_dataNEG.shape}')
# QC filtering: if 0 in 3/4 QC elimined
QC_blank_filterNEG = QC_filter (blank_filtered_dataNEG, 0)
QC_blank_filterNEG.index.name = 'sample'
print (f'QC_blank_filterNEG is \n {QC_blank_filterNEG.shape}')
# QCDil filtering CV <=10 elimined
raw_list = ["sample == 'QC_dil2_neg01'", "sample == 'QC_dil4_neg01'" , "sample == 'QC_dil8_neg01'"]
QCDil_QC_blank_filterNEG = cv_filter (QC_blank_filterNEG, raw_list, 10, "<=")
print (f'QCDil_QC_blank_filterNEG is \n {QCDil_QC_blank_filterNEG.shape}')
# metadata merging for filtered data
metacol=['class','SampleType', 'injectionOrder', 'id natif ']
metadataNEGDataf=filter_column(metadataNEGDatai,exclude=metacol)
metadataNEGDataf.set_index('sample', inplace = True)
QCDil_QC_blank_filterNEGf = merge_data(QCDil_QC_blank_filterNEG, metadataNEGDataf)
print (f'QCDil_QC_blank_filterNEGf is \n {QCDil_QC_blank_filterNEGf.shape}')
# caving in a csv
output_pathNEG = save_as_csv(QCDil_QC_blank_filterNEG, output_dir=output_path_NEG, output_file="02.1-datafiltered_NEG", file_conflict="replace")
print("CSV file saved at:", output_path_NEG)