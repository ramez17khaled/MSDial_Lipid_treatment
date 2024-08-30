import importlib.util
import subprocess
import sys
import os

required_libraries = ['pandas','numpy', 'sklearn', 'seaborn', 'matplotlib']

for lib in required_libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        print(f"{lib} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set()
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

meta_file_pathPOS = "D:/data/ThermoDataV2/MSDial/02-Nico_metadata/thermoPOS.csv"
file_pathPOS = "D:/data/ThermoDataV2/MSDial/01-mzmlThermo/1.1-Data_POS/02.1-datafiltered_POS.csv"
output_pathPOS = "D:/data/ThermoDataV2/MSDial/04-codeOutput/POS"

meta_file_pathNEG = "D:/data/ThermoDataV2/MSDial/02-Nico_metadata/thermoNEG.csv"
file_pathNEG = "D:/data/ThermoDataV2/MSDial/01-mzmlThermo/1.1-Data_NEG/02.1-datafiltered_NEG.csv"
output_pathNEG = "D:/data/ThermoDataV2/MSDial/04-codeOutput/NEG"

column = "Duration"
hue = column
conditions = "T,C1,C2,H,QC"
condition = conditions.split(',')

def readcsv (path):
    path = os.path.normpath(path)
    if os.name =='nt':
        path =path.replace("\\","/")
    data = pd.read_csv(path, sep =';')
    return data

dataPOS = readcsv(file_pathPOS)
metadataPOS = readcsv(meta_file_pathPOS)
dataNEG = readcsv(file_pathNEG)
metadataNEG = readcsv(meta_file_pathNEG)

def merge (df,metadata):
    df = df.rename(columns={df.columns[0]:'sample'})
    df.set_index('sample', inplace=True)
    df['condition'] = df.index.map(metadata.set_index('sample')[column])
    return df

condition_dataPOS = merge(dataPOS,metadataPOS)
condition_dataPOS = condition_dataPOS.loc[condition_dataPOS['condition'].isin(condition)]
condition_dataNEG = merge(dataNEG,metadataNEG)
condition_dataNEG = condition_dataNEG.loc[condition_dataNEG['condition'].isin(condition)]
NPcondition_dataPOS = condition_dataPOS.to_numpy()
NPcondition_dataNEG = condition_dataNEG.to_numpy()
condition_NAMPOS = NPcondition_dataPOS[:, 0:2]
condition_NUMdataPOS = NPcondition_dataPOS[:, 2:]
condition_NAMNEG = NPcondition_dataNEG[:, 0:2]
condition_NUMdataNEG = NPcondition_dataNEG[:, 2:]

def QCselection(df):
    qc01_df = df[(~df.iloc[:, 0].str.contains('dil', case=False)) &
                      (df.iloc[:, 0].str.contains('QC', na=False))]
    return qc01_df

QCdataPOS = QCselection(dataPOS)
QCdataNEG = QCselection(dataNEG)

NPdataPOS = QCdataPOS.to_numpy()
NPdataNEG = QCdataNEG.to_numpy()
NAMPOS = NPdataPOS[:, 0]
NUMdataPOS = NPdataPOS[:, 1:]
NAMNEG = NPdataNEG[:, 0]
NUMdataNEG = NPdataNEG[:, 1:]

def PCAbarplot(X, title):
    x_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=3)
    pca_features = pca.fit_transform(x_scaled)
    plt.bar(
        range(1,len(pca.explained_variance_)+1),
        pca.explained_variance_
    )
    plt.plot(
        range(1,len(pca.explained_variance_ )+1),
        np.cumsum(pca.explained_variance_),
        c='red',
        label='Cumulative Explained Variance'
    )
    plt.legend(loc='upper left')
    plt.xlabel('Number of components')
    plt.ylabel('Explained variance (eignenvalues)')
    plt.title(title)

fig1 = plt.figure(figsize=(6, 6))
PCAbarplot(NUMdataNEG, 'QCNEG')
fig1.savefig(output_pathNEG+'/QCNEG_PCA_barplot.png', dpi=300)
fig2 = plt.figure(figsize=(6, 6))
PCAbarplot(NUMdataPOS, 'QCPOS')
fig2.savefig(output_pathPOS+'/QCPOS_PCA_barplot.png', dpi=300)
plt.show()

def perform_pca_and_plot(data_file, metadata_file, sample_id_col, group_col, group_name, conditions, color):
    """
    Perform PCA on the provided data and plot the results for a specific group.

    Parameters:
    - data_file: Path to the CSV file containing the data (features).
    - metadata_file: Path to the CSV file containing metadata (group labels).
    - sample_id_col: Name of the column containing sample IDs in both files.
    - group_col: Name of the column in the metadata file that contains group labels.
    - group_name: The specific group to plot (e.g., 'POS' or 'NEG').
    - color: Color to use for plotting the specific group.
    """
    # Load the data and metadata
    data_df = pd.read_csv(data_file, sep=';')
    data_df.rename(columns={data_df.columns[0]: sample_id_col}, inplace=True)
    metadata_df = pd.read_csv(metadata_file, sep=';')
    metadata_df = metadata_df[[sample_id_col, group_col]]

    # Merge data and metadata
    merged_df = pd.merge(data_df, metadata_df, on=sample_id_col)
    filtered_df = merged_df.loc[merged_df[group_col].isin (conditions)]

    # Separate features
    features_df = filtered_df.drop(columns=[sample_id_col, group_col])
    features = features_df.to_numpy()

    # Perform PCA
    pca = PCA(n_components=2)
    pca.fit(features)
    scores = pca.transform(features)
    loadings = pca.components_

    # Create a plot
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Loadings Plot
    axs[0].set_title(f"A) Loadings for {group_name}")
    axs[0].set_xlabel("PC1")
    axs[0].set_ylabel("PC2")
    axs[0].set_aspect("equal")
    axs[0].axhline(y=0, color="gray", linestyle="-")
    axs[0].axvline(x=0, color="gray", linestyle="-")
    axs[0].add_artist(plt.Circle((0, 0), radius=1, color="lightgray", fill=False))

    for i, loading in enumerate(loadings):
        axs[0].plot(loading[0], loading[1], "o-", markersize=5, color="navy", linewidth=1)
        axs[0].text(loading[0] + 0.02, loading[1] + 0.02, f"Feature {i+1}", fontsize=8)

    # Scores Plot
    axs[1].set_title(f"B) Scores for {group_name}")
    axs[1].set_xlabel("PC1")
    axs[1].set_ylabel("PC2")
    axs[1].set_aspect("equal")
    axs[1].axhline(y=0, color="gray", linestyle="-")
    axs[1].axvline(x=0, color="gray", linestyle="-")
    axs[1].add_artist(plt.Circle((0, 0), radius=10, color="lightgray", fill=False))

    axs[1].scatter(scores[:, 0], scores[:, 1], color=color, label=group_name, s=20)
    axs[1].legend(loc="lower right")
    
    plt.tight_layout()
    plt.show()

# Example usage
perform_pca_and_plot(
    data_file=file_pathPOS,
    metadata_file=meta_file_pathPOS,
    sample_id_col="sample",
    group_col=column,
    conditions=condition,
    group_name="POS",
    color="navy"
)

perform_pca_and_plot(
    data_file=file_pathNEG,
    metadata_file=meta_file_pathNEG,
    sample_id_col="sample",
    group_col=column,
    conditions=condition,
    group_name="NEG",
    color="cadetblue"
)
