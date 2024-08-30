import importlib.util
import subprocess
import sys
import os

# List of required libraries
required_libraries = ['tkinter', 'pandas', 'numpy', 'scikit-learn', 'matplotlib']

# Check if each library is installed
for lib in required_libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        print(f"{lib} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Now import the required libraries
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

current_directory = os.getcwd()
parent_directory1 = os.path.dirname(current_directory)
parent_directory = os.path.dirname(parent_directory1)
metadata_path = os.path.join(parent_directory, '02-Nico_metadata')
data_pathPOS = os.path.join(parent_directory, '01-mzmlThermo','1.1-Data_POS')
data_pathNEG = os.path.join(parent_directory, '01-mzmlThermo','1.1-Data_NEG')

meta_file_pathPOS = os.path.join(metadata_path, 'thermoPOS.csv')
file_pathPOS = os.path.join(data_pathPOS, '02.1-datafiltered_POS.csv')
output_pathPOS = os.path.join(parent_directory, '04-codeOutput', 'POS')


meta_file_pathNEG = os.path.join(metadata_path, 'thermoNEG.csv')
file_pathNEG = os.path.join(data_pathNEG, '02.1-datafiltered_NEG.csv')
output_pathNEG = os.path.join(parent_directory, '04-codeOutput', 'NEG')

column = "Duration"
hue = column
conditions = "C1,H"
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
    df[column] = df['sample'].map(metadata.set_index('sample')[column])
    return df

merged_dataPOS = merge(dataPOS, metadataPOS)
merged_dataNEG = merge(dataNEG, metadataNEG)

def conditionsSelection(df):
    na_df = df.dropna()
    filtered_df = na_df.loc[na_df[column].isin(condition)]
    filtered_df.set_index('sample',inplace=True)
    return filtered_df

filtered_dataPOS = conditionsSelection(merged_dataPOS)
filtered_dataNEG = conditionsSelection(merged_dataNEG)

print ('data is ready !')

def perform_pls_da_analysis(ThermoPOSData, output_dir='.', output_filename='PLSDA-results'):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Paths for PDF and CSV files
    pdf_path = os.path.join(output_dir, f'{output_filename}.pdf')
    csv_path = os.path.join(output_dir, f'{output_filename}_top_metabolites.csv')

    # Extract features and target
    X = ThermoPOSData.drop('Duration', axis=1)  # Features (metabolites)
    y = ThermoPOSData['Duration']  # Target (conditions)

    # Encode the target labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

    # Initialize PLS-DA model with 2 components
    pls_da = PLSRegression(n_components=2)

    # Fit the model
    pls_da.fit(X_train, y_train)

    # Transform data to the PLS-DA space
    X_train_pls = pls_da.transform(X_train)
    X_test_pls = pls_da.transform(X_test)

    # Predict on the test set
    y_pred = pls_da.predict(X_test)
    y_pred_class = (y_pred > 0.5).astype(int).flatten()

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred_class)
    conf_matrix = confusion_matrix(y_test, y_pred_class)

    print(f"Accuracy: {accuracy}")
    print(f"Confusion Matrix:\n{conf_matrix}")

    # Prepare for saving plots to PDF
    with PdfPages(pdf_path) as pdf:
        # PLS-DA plot
        plt.figure(figsize=(10, 7))
        plt.scatter(X_train_pls[:, 0], X_train_pls[:, 1], c=y_train, cmap='viridis', label='Train')
        plt.scatter(X_test_pls[:, 0], X_test_pls[:, 1], c=y_test, cmap='coolwarm', marker='x', label='Test')
        plt.xlabel('PLS Component 1')
        plt.ylabel('PLS Component 2')
        plt.title('PLS-DA Plot')
        plt.legend()
        pdf.savefig()  # Save the current figure into the PDF
        plt.close()

        # Plotting the loadings (feature contributions)
        loadings = pls_da.x_loadings_
        sorted_indices = np.argsort(np.abs(loadings[:, 0]))[::-1]
        top_n = 20  # Number of top metabolites to display
        top_indices = sorted_indices[:top_n]
        top_metabolites_array = np.array([X.columns[i] for i in top_indices])
        top_metabolites_df = pd.DataFrame(top_metabolites_array, columns=['Top 20 Metabolites'])
        top_metabolites_df.to_csv(csv_path, index=False)

        plt.figure(figsize=(12, 8))
        for i in top_indices:
            plt.arrow(0, 0, loadings[i, 0], loadings[i, 1], color='r', alpha=0.5)
            plt.text(loadings[i, 0], loadings[i, 1], X.columns[i], fontsize=12, ha='center', va='center')
        plt.xlabel('PLS Component 1')
        plt.ylabel('PLS Component 2')
        plt.title('PLS-DA Loadings Plot (Top 20 Metabolite Contributions)')
        plt.grid()
        plt.xlim(loadings[:, 0].min() - 0.01, loadings[:, 0].max() + 0.01)
        plt.ylim(loadings[:, 1].min() - 0.01, loadings[:, 1].max() + 0.01)
        pdf.savefig()  # Save the current figure into the PDF
        plt.close()

        # ROC curve
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)

        plt.figure(figsize=(10, 7))
        plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc='lower right')
        pdf.savefig()  # Save the current figure into the PDF
        plt.close()


    print("Top 20 Metabolites saved to:", csv_path)


perform_pls_da_analysis(filtered_dataPOS, output_dir=output_pathPOS, output_filename='PLS_DA-results')
perform_pls_da_analysis(filtered_dataNEG, output_dir=output_pathNEG, output_filename='PLS_DA-results')