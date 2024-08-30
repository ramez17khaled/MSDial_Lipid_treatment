import importlib.util
import subprocess
import sys
import os
import csv
import re

required_libraries = ['pandas', 'numpy']

for lib in required_libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        print(f"{lib} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

import pandas as pd
import numpy as np

current_directory = os.getcwd()
parent_directory1 = os.path.dirname(current_directory)
parent_directory = os.path.dirname(parent_directory1)
annotated_data_pathNEG = os.path.join(parent_directory, '01-mzmlThermo','2.1-annotation_data_NEG')
statistical_data_pathNEG = os.path.join(parent_directory, '04-codeOutput','NEG')
output_pathNEG = os.path.join(parent_directory, '04-codeOutput', 'NEG')

annotated_data_NEG = [f for f in os.listdir(annotated_data_pathNEG) if f.startswith('AlignResult') and f.endswith('.msdial')]
if annotated_data_NEG:
    annotated_data_NEG = os.path.join(annotated_data_pathNEG, annotated_data_NEG[0])
else:
    print("No AlignmentResult found")
commun_higt_int_metabolite_NEG = os.path.join(statistical_data_pathNEG, 'common_higt_int_metabolites_T-H.csv')
different_metabolite_NEG = os.path.join(statistical_data_pathNEG, 'different_metabolites_T-H.csv')
commun_metabolite_NEG = os.path.join(statistical_data_pathNEG, 'common_metabolites_T-H.csv')
biomarcker_C1H_NEG = os.path.join(statistical_data_pathNEG, 'PLS_DA-results_top_metabolitesC1-H.csv')
biomarcker_C2T_NEG = os.path.join(statistical_data_pathNEG, 'PLS_DA-results_top_metabolitesC2-T.csv')

different_metabolite_NEG =pd.read_csv(different_metabolite_NEG)
different_metabolite_NEG['RT'] = different_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
different_metabolite_NEG['MZ'] = different_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
commun_higt_int_metabolite_NEG =pd.read_csv(commun_higt_int_metabolite_NEG)
commun_higt_int_metabolite_NEG['RT'] = commun_higt_int_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
commun_higt_int_metabolite_NEG['MZ'] = commun_higt_int_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
commun_metabolite_NEG =pd.read_csv(commun_metabolite_NEG)
commun_metabolite_NEG['RT'] = commun_metabolite_NEG['Metabolite'].apply(lambda x: 
    float(re.findall(r'T(\d+\.\d+)', x)[0]) if re.findall(r'T(\d+\.\d+)', x) else np.nan)
commun_metabolite_NEG['MZ'] = commun_metabolite_NEG['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
biomarcker_C1H_NEG =pd.read_csv(biomarcker_C1H_NEG, sep = '\t')
biomarcker_C1H_NEG['RT'] = biomarcker_C1H_NEG['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
biomarcker_C1H_NEG['MZ'] = biomarcker_C1H_NEG['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
biomarcker_C2T_NEG =pd.read_csv(biomarcker_C2T_NEG, sep = '\t')
biomarcker_C2T_NEG['RT'] = biomarcker_C2T_NEG['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
biomarcker_C2T_NEG['MZ'] = biomarcker_C2T_NEG['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))

annotated_data_NEG =pd.read_csv(annotated_data_NEG, sep = '\t')

def manipulate_annotated_data_NEG(df):
    """
    Manipulate the annotated data for NEG (NEGitive) mode.

    Parameters:
    annotated_data_NEG (pd.DataFrame): The input annotated data for NEG mode.

    Returns:
    pd.DataFrame: The manipulated annotated data for NEG mode.
    """
    annotated_data_manipul = df.iloc[3:]
    annotated_data_manipul = annotated_data_manipul.drop(annotated_data_manipul.columns[5:11], axis=1)
    annotated_data_manipul = annotated_data_manipul.drop(annotated_data_manipul.columns[6:29], axis=1)
    annotated_data_manipul = annotated_data_manipul.drop(columns=[annotated_data_manipul.columns[0]])
    annotated_data_manipul = annotated_data_manipul.rename(columns=annotated_data_manipul.iloc[0]).drop(annotated_data_manipul.index[0])
    annotated_data_manipul = annotated_data_manipul.reset_index(drop=True)
    annotated_data_manipul = annotated_data_manipul.rename(columns={"Average Rt(min)": "Rt(min)", "Average Mz": "Mz"})
    annotated_data_manipul['metabolite'] = 'M' + annotated_data_manipul['Mz'].astype(str) + 'T' + annotated_data_manipul['Rt(min)'].astype(str)
    return annotated_data_manipul

annotated_data_NEG_manipulated = manipulate_annotated_data_NEG(annotated_data_NEG)

filenameNEG = '/annotated-liste-NEG.csv'

full_pathNEG = annotated_data_pathNEG + filenameNEG

annotated_data_NEG_manipulated.to_csv(full_pathNEG, index=False)

print(f"annotated_data_NEG_manipulated saved to: {full_pathNEG}")

metabolite_annotated_NEG_dict = {}
def annotated_dictionnary_creating(df, dict):
    for index, row in df.iterrows():
        METABOLITE = row['metabolite']
        MZ = row['Mz']
        RT = row['Rt(min)']
        ANNOTATION = row['Metabolite name']
        FAMILY = row['Ontology']
        dict[METABOLITE] = {'Mz':MZ,
                            'Rt(min)':RT,
                            'Metabolite name':ANNOTATION,
                            'Family':FAMILY
                            }
    return dict

metabolite_annotated_NEG_dict = annotated_dictionnary_creating(annotated_data_NEG_manipulated,
                                                metabolite_annotated_NEG_dict)

print (f'metabolite_annotated_NEG_dict :\n{metabolite_annotated_NEG_dict}')

NEG_commun_higt_int_annotated = {k: v for k, v in metabolite_annotated_NEG_dict.items() 
                 if k in commun_higt_int_metabolite_NEG['Metabolite'].values}
NEG_commun_annotated = {k: v for k, v in metabolite_annotated_NEG_dict.items() 
                 if k in commun_metabolite_NEG['Metabolite'].values}
NEG_different_annotated = {k: v for k, v in metabolite_annotated_NEG_dict.items() 
                 if k in different_metabolite_NEG['Metabolite'].values}
NEG_biomarcker_C1H_annotated = {k: v for k, v in metabolite_annotated_NEG_dict.items() 
                 if k in biomarcker_C1H_NEG['Top 20 Metabolites'].values}
NEG_biomarcker_C2T_annotated = {k: v for k, v in metabolite_annotated_NEG_dict.items() 
                 if k in biomarcker_C2T_NEG['Top 20 Metabolites'].values}

print (f'NEG_commun_annotated :\n{NEG_commun_annotated}')
print (f'NEG_commun_higt_int_annotated :\n{NEG_commun_higt_int_annotated}')
print (f'NEG_different_annotated :\n{NEG_different_annotated}')
print (f'NEG_biomarcker_C1H_annotated :\n{NEG_biomarcker_C1H_annotated}')
print (f'NEG_biomarcker_C2T_annotated :\n{NEG_biomarcker_C2T_annotated}')

with open(os.path.join(output_pathNEG, 'NEG_commun_higt_int_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in NEG_commun_higt_int_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathNEG, 'NEG_commun_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in NEG_commun_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathNEG, 'NEG_different_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in NEG_different_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathNEG, 'NEG_biomarcker_C1H_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in NEG_biomarcker_C1H_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathNEG, 'NEG_biomarcker_C2T_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in NEG_biomarcker_C2T_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

print(f"NEG_commun_higt_int_annotated saved to: {output_pathNEG}")
print(f"NEG_commun_annotated saved to: {output_pathNEG}")
print(f"NEG_different_annotated saved to: {output_pathNEG}")
print(f"NEG_biomarcker_C1H_annotated saved to: {output_pathNEG}")
print(f"NEG_biomarcker_C2T_annotated saved to: {output_pathNEG}")
print ('DONE!')