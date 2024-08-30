import importlib.util
import subprocess
import sys
import os

required_libraries = ['pandas', 'scipy', 'seaborn', 'matplotlib', 'itertools']

for lib in required_libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        print(f"{lib} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

meta_file_pathPOS = "D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoPOS.csv"
file_pathPOS = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_POS/02.1-datafiltered_POS.csv"
output_pathPOS = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/POS"

meta_file_pathNEG = "D:/data/ThermoDataV2/MSDial/V2/02-Nico_metadata/thermoNEG.csv"
file_pathNEG = "D:/data/ThermoDataV2/MSDial/V2/01-mzmlThermo/1.1-Data_NEG/02.1-datafiltered_NEG.csv"
output_pathNEG = "D:/data/ThermoDataV2/MSDial/V2/04-codeOutput/NEG"

columne = "id"
hue = columne
conditions = "Dil8,Dil4,Dil2,QC1"
condition = conditions.split(',')


def readcsv (path):
    path = os.path.normpath(path)
    if os.name =='nt':
        path =path.replace("\\","/")
    data = pd.read_csv(path, sep =';')
    return data

dataPOS = readcsv(file_pathPOS)
dataNEG = readcsv(file_pathNEG)

def statisticalSignificance (df):
    df_melt = pd.melt(df, id_vars=[df.columns[0]], var_name='metabolite', value_name='intensity')
    df_melt.columns = ['condition', 'metabolite', 'intensity']
    df_melt['intensity_log'] = np.log(df_melt['intensity'])
    col = 'intensity_log'
    data = [
        df_melt[(df_melt['condition'].str.contains('dil2', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('dil4', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('dil8', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('QC', na=False)) & (df_melt['condition'].str.contains('01', na=False)) & (~df_melt['condition'].str.contains('dil', na=False))][col],
    ]
    dil_df = df_melt[(df_melt['condition'].str.contains('dil', case=False))]
    qc01_df = df_melt[(~df_melt['condition'].str.contains('dil', case=False)) &
                      (df_melt['condition'].str.contains('QC', na=False)) & 
                      (df_melt['condition'].str.contains('01', na=False))]
    df_label = pd.concat([dil_df,qc01_df])
    unique_values = df_label['condition'].unique() 
    ls = list(range(1, len(data) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    for combination in combinations:
        data1 = data[combination[0] - 1]
        data2 = data[combination[1] - 1]
        # Significance
        U, p = stats.mannwhitneyu(data1, data2, alternative='two-sided')
        if p < 0.05:
            significant_combinations.append([combination, p])

    print(significant_combinations)
    return significant_combinations 

significant_combinationsPOS = statisticalSignificance(dataPOS)
significant_combinationsNEG = statisticalSignificance(dataNEG)  

def plot_significance_bars(significant_combinations, y_range, top):
    for i, significant_combination in enumerate(significant_combinations):
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        level = len(significant_combinations) - i
        bar_height = (y_range * 0.07 * level) + top
        bar_tips = bar_height - (y_range * 0.02)
        plt.plot(
            [x1, x1, x2, x2],
            [bar_tips, bar_height, bar_height, bar_tips], lw=1, c='k'
        )
        p = significant_combination[1]
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        text_height = bar_height + (y_range * 0.01)
        plt.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k')

def boxPlotSignificant(df, significant_combinations):
    df_melt = pd.melt(df, id_vars=[df.columns[0]], var_name='metabolite', value_name='intensity')
    df_melt.columns = ['condition', 'metabolite', 'intensity']
    df_melt['intensity_log'] = np.log(df_melt['intensity'])
    col = 'intensity_log'
    data = [
        df_melt[(df_melt['condition'].str.contains('dil2', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('dil4', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('dil8', na=False))][col],
        df_melt[(df_melt['condition'].str.contains('QC', na=False)) & (df_melt['condition'].str.contains('01', na=False)) & (~df_melt['condition'].str.contains('dil', na=False))][col],
    ]
    dil_df = df_melt[(df_melt['condition'].str.contains('dil', case=False))]
    qc01_df = df_melt[(~df_melt['condition'].str.contains('dil', case=False)) &
                      (df_melt['condition'].str.contains('QC', na=False)) & 
                      (df_melt['condition'].str.contains('01', na=False))]
    df_label = pd.concat([dil_df,qc01_df])
    unique_values = df_label['condition'].unique()
    print(f'unique value are :\n{unique_values}')

    ax = plt.axes()
    dp = ax.boxplot(data, widths=0.6, patch_artist=True)
    ax.set_ylabel(r'log intensity')
    xticklabels = unique_values
    xticklabels = [label.title() for label in xticklabels]
    ax.set_xticklabels(xticklabels)
    ax.tick_params(axis='x', which='major', length=0)
    xticks = [0.5] + [x + 0.5 for x in ax.get_xticks()]
    ax.set_xticks(xticks, minor=True)
    ax.tick_params(axis='x', which='minor', length=3, width=1)
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    top = ax.get_ylim()[1]
    plot_significance_bars(significant_combinations, y_range, top)

    return ax


plt.figure(figsize=(8, 6))
axPOS = boxPlotSignificant(dataPOS, significant_combinationsPOS)
plt.title('Positive Data')
plt.savefig(output_pathPOS + '/sig-boxplot-POS.png', bbox_inches='tight')
plt.show(block=False)
plt.show(block=False)

plt.figure(figsize=(8, 6))
axNEG = boxPlotSignificant(dataNEG, significant_combinationsNEG)
plt.title('Negative Data')
plt.savefig(output_pathNEG + '/sig-boxplot-POS.png', bbox_inches='tight')
plt.show()






