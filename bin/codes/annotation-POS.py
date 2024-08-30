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
annotated_data_pathPOS = os.path.join(parent_directory, '01-mzmlThermo','2.1-annotation_data_POS')
statistical_data_pathPOS = os.path.join(parent_directory, '04-codeOutput','POS')
output_pathPOS = os.path.join(parent_directory, '04-codeOutput', 'POS')

annotated_data_POS = [f for f in os.listdir(annotated_data_pathPOS) if f.startswith('AlignResult') and f.endswith('.msdial')]
if annotated_data_POS:
    annotated_data_POS = os.path.join(annotated_data_pathPOS, annotated_data_POS[0])
else:
    print("No AlignmentResult found")
commun_higt_int_metabolite_POS = os.path.join(statistical_data_pathPOS, 'common_higt_int_metabolites_T-H.csv')
different_metabolite_POS = os.path.join(statistical_data_pathPOS, 'different_metabolites_T-H.csv')
commun_metabolite_POS = os.path.join(statistical_data_pathPOS, 'common_metabolites_T-H.csv')
biomarcker_C1H_POS = os.path.join(statistical_data_pathPOS, 'PLS_DA-results_top_metabolitesC1-H.csv')
biomarcker_C2T_POS = os.path.join(statistical_data_pathPOS, 'PLS_DA-results_top_metabolitesC2-T.csv')

different_metabolite_POS =pd.read_csv(different_metabolite_POS)
different_metabolite_POS['RT'] = different_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
different_metabolite_POS['MZ'] = different_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
commun_higt_int_metabolite_POS =pd.read_csv(commun_higt_int_metabolite_POS)
commun_higt_int_metabolite_POS['RT'] = commun_higt_int_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
commun_higt_int_metabolite_POS['MZ'] = commun_higt_int_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
commun_metabolite_POS =pd.read_csv(commun_metabolite_POS)
commun_metabolite_POS['RT'] = commun_metabolite_POS['Metabolite'].apply(lambda x: 
    float(re.findall(r'T(\d+\.\d+)', x)[0]) if re.findall(r'T(\d+\.\d+)', x) else np.nan)
commun_metabolite_POS['MZ'] = commun_metabolite_POS['Metabolite'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
biomarcker_C1H_POS =pd.read_csv(biomarcker_C1H_POS, sep = '\t')
biomarcker_C1H_POS['RT'] = biomarcker_C1H_POS['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
biomarcker_C1H_POS['MZ'] = biomarcker_C1H_POS['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))
biomarcker_C2T_POS =pd.read_csv(biomarcker_C2T_POS, sep = '\t')
biomarcker_C2T_POS['RT'] = biomarcker_C2T_POS['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'T(\d+\.\d+)', x)[0]))
biomarcker_C2T_POS['MZ'] = biomarcker_C2T_POS['Top 20 Metabolites'].apply(lambda x: float(re.findall(r'M(\d+\.\d+)', x)[0]))

annotated_data_POS =pd.read_csv(annotated_data_POS, sep = '\t')

def manipulate_annotated_data_POS(df):
    """
    Manipulate the annotated data for POS (POSitive) mode.

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
    annotated_data_manipul['metabolite'] = 'M' + annotated_data_manipul['Mz'].astype(str) + 'T' + annotated_data_manipul['Rt(min)'].astype(str)
    return annotated_data_manipul

annotated_data_POS_manipulated = manipulate_annotated_data_POS(annotated_data_POS)

filenamePOS = '/annotated-liste-POS.csv'

full_pathPOS = annotated_data_pathPOS + filenamePOS

annotated_data_POS_manipulated.to_csv(full_pathPOS, index=False)

print(f"annotated_data_POS_manipulated saved to: {full_pathPOS}")

metabolite_annotated_POS_dict = {}
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

metabolite_annotated_POS_dict = annotated_dictionnary_creating(annotated_data_POS_manipulated,
                                                metabolite_annotated_POS_dict)

print (f'metabolite_annotated_POS_dict :\n{metabolite_annotated_POS_dict}')

POS_commun_higt_int_annotated = {k: v for k, v in metabolite_annotated_POS_dict.items() 
                 if k in commun_higt_int_metabolite_POS['Metabolite'].values}
POS_commun_annotated = {k: v for k, v in metabolite_annotated_POS_dict.items() 
                 if k in commun_metabolite_POS['Metabolite'].values}
POS_different_annotated = {k: v for k, v in metabolite_annotated_POS_dict.items() 
                 if k in different_metabolite_POS['Metabolite'].values}
POS_biomarcker_C1H_annotated = {k: v for k, v in metabolite_annotated_POS_dict.items() 
                 if k in biomarcker_C1H_POS['Top 20 Metabolites'].values}
POS_biomarcker_C2T_annotated = {k: v for k, v in metabolite_annotated_POS_dict.items() 
                 if k in biomarcker_C2T_POS['Top 20 Metabolites'].values}

print (f'POS_commun_annotated :\n{POS_commun_annotated}')
print (f'POS_commun_higt_int_annotated :\n{POS_commun_higt_int_annotated}')
print (f'POS_different_annotated :\n{POS_different_annotated}')
print (f'POS_biomarcker_C1H_annotated :\n{POS_biomarcker_C1H_annotated}')
print (f'POS_biomarcker_C2T_annotated :\n{POS_biomarcker_C2T_annotated}')

with open(os.path.join(output_pathPOS, 'POS_commun_higt_int_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in POS_commun_higt_int_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathPOS, 'POS_commun_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in POS_commun_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathPOS, 'POS_different_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in POS_different_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathPOS, 'POS_biomarcker_C1H_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in POS_biomarcker_C1H_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

with open(os.path.join(output_pathPOS, 'POS_biomarcker_C2T_annotated.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Metabolite ID', 'Mz', 'Rt(min)', 'Metabolite name', 'Family']
    writer.writerow(headers)
    for metabolite_id, metabolite_info in POS_biomarcker_C2T_annotated.items():
        row = [metabolite_id, metabolite_info['Mz'], metabolite_info['Rt(min)'], metabolite_info['Metabolite name'], metabolite_info['Family']]
        writer.writerow(row)

print(f"POS_commun_higt_int_annotated saved to: {output_pathPOS}")
print(f"POS_commun_annotated saved to: {output_pathPOS}")
print(f"POS_different_annotated saved to: {output_pathPOS}")
print(f"POS_biomarcker_C1H_annotated saved to: {output_pathPOS}")
print(f"POS_biomarcker_C2T_annotated saved to: {output_pathPOS}")
print ('DONE!')