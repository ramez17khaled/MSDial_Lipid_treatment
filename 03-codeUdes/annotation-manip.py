import pandas as pd
import numpy as np
import re
import os

#differant_metabolite_POS = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/POS/different_metabolites_T-H.csv"
#commun_higt_int_metabolite_POS = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/POS/common_higt_int_metabolites_T-H.csv"
annotated_data_POS = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/2.1-annotation_data_POS/POS_Height_0_2024_08_07_11_01_43.csv"
output_POS = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/2.1-annotation_data_POS"

#differant_metabolite_NEG = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/NEG/different_metabolites_T-H.csv"
#commun_higt_int_metabolite_NEG = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/NEG/common_higt_int_metabolites_T-H.csv"
#annotated_data_NEG = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/2.1-annotation_data_NEG/NEG_Height_0_2024_08_07_11_41_42.csv"
#output_NEG = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/2.1-annotation_data_NEG"

#differant_metabolite_POS =pd.read_csv(differant_metabolite_POS)
#differant_metabolite_POS['RT'] = differant_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
#commun_higt_int_metabolite_POS =pd.read_csv(commun_higt_int_metabolite_POS)
#commun_higt_int_metabolite_POS['RT'] = commun_higt_int_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
annotated_data_POS =pd.read_csv(annotated_data_POS)

#differant_metabolite_NEG =pd.read_csv(differant_metabolite_NEG)
#differant_metabolite_NEG['RT'] = differant_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
#commun_higt_int_metabolite_NEG =pd.read_csv(commun_higt_int_metabolite_NEG)
#commun_higt_int_metabolite_NEG['RT'] = commun_higt_int_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
#annotated_data_NEG =pd.read_csv(annotated_data_NEG)

def manipulate_annotated_data_POS(df):
    """
    Manipulate the annotated data for POS (Positive) mode.

    Parameters:
    annotated_data_POS (pd.DataFrame): The input annotated data for POS mode.

    Returns:
    pd.DataFrame: The manipulated annotated data for POS mode.
    """
    annotated_data_manipul = df.iloc[3:]
    annotated_data_manipul = annotated_data_manipul.drop(annotated_data_manipul.columns[5:11], axis=1)
    annotated_data_manipul = annotated_data_manipul.drop(annotated_data_manipul.columns[6:29], axis=1)
    annotated_data_manipul = annotated_data_manipul.drop(columns=[annotated_data_manipul.columns[0]])
    annotated_data_manipul = annotated_data_manipul.rename(columns=annotated_data_manipul.iloc[0]).drop(annotated_data_manipul.index[0])
    annotated_data_manipul = annotated_data_manipul.reset_index(drop=True)
    annotated_data_manipul = annotated_data_manipul.rename(columns={"Average Rt(min)": "Rt(min)", "Average Mz": "Mz"})
    annotated_data_manipul['metabolite'] = 'M' + annotated_data_manipul['Mz'].astype(str).str.split('.').str[0] + 'T' + annotated_data_manipul['Rt(min)'].astype(str)
    return annotated_data_manipul

annotated_data_POS_manipulated = manipulate_annotated_data_POS(annotated_data_POS)
#annotated_data_NEG_manipulated = manipulate_annotated_data_POS(annotated_data_NEG)
#annotated_data_POS_manipulated

filenamePOS = '/annotated-liste-POS.csv'
#filenameNEG = '/annotated-liste-NEG.csv'

full_pathPOS = output_POS + filenamePOS
#full_pathNEG = output_NEG + filenameNEG
annotated_data_POS_manipulated.to_csv(full_pathPOS, index=False)
#annotated_data_NEG_manipulated.to_csv(full_pathNEG, index=False)
print(f"annotated_data_POS_manipulated saved to: {full_pathPOS}")
#print(f"annotated_data_NEG_manipulated saved to: {full_pathNEG}")