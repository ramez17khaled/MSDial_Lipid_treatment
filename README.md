# MSDial_Lipid_Treatment

MSDial_Lipid_Treatment is an open-source tool designed for lipid biomarker detection and annotation following Orbitrap LC-MS/MS DDA analysis. The tool processes mzML format data and identifies biomarkers for two diseases (T and H), as well as common metabolites between them. Additionally, it provides statistical visualizations.

**Note:** Currently, the code is tailored to work only with the specific metadata conditions of this project. Future updates will support more general metadata and conditions.

## Installation

1. **Clone the repository** or **download the ZIP file**.
2. **Prepare your dataset:**
   - **Convert raw data to mzML format** using MSConvert:
     - Install ProteoWizard: [ProteoWizard](https://proteowizard.sourceforge.io/)
     - Convert MS1 data and save the output in:
       - `01.0-MS1mzmlThermo-POS` for positive mode (POS) data.
       - `01.0-MS1mzmlThermo-NEG` for negative mode (NEG) data.
     - Convert MS2 data and save the output in:
       - `02.0-MS2mzmlThermo-POS` for positive mode (POS) data.
       - `02.0-MS2mzmlThermo-NEG` for negative mode (NEG) data.
   - **Prepare metadata:**
     - Create a CSV file (use `;` as the delimiter) for each data mode (POS and NEG).
     - Save the files in the `02-Nico_metadata` directory.
   - **Install MSDIAL:**
     - Download and install `MSDIAL ver.4.9.221218 Windowsx64`: [MSDIAL](https://systemsomicslab.github.io/compms/msdial/main.html)
     - Place the MSDIAL installation in the `bin` directory and ensure the PATH is set correctly for execution in batch (.bat) files.
   - **Prepare the annotation databases:**
     - Download the MSP database for NEG and POS from MSDIAL and save it in the `01-mzmlThermo` directory.
     - Generate the in-house database for POS and NEG data is in the correct format (TXT).

## Parameters and Execution

1. **Configure parameters for feature extraction and annotation:**
   - Adjust parameters for feature extraction in NEG mode:  
     `01-mzmlThermo\01.0-MS1mzmlThermo-NEG\NEGparametre.txt`
   - Adjust parameters for feature extraction in POS mode:  
     `01-mzmlThermo\01.0-MS1mzmlThermo-POS\POSparametre.txt`
   - Adjust parameters for feature annotation in NEG mode:  
     `01-mzmlThermo\02.0-MS2mzmlThermo-NEG\M2parametreNEG.txt`
   - Adjust parameters for feature annotation in POS mode:  
     `01-mzmlThermo\02.0-MS2mzmlThermo-POS\M2parametrePOS.txt`

2. **Run analysis and annotation scripts:**
   - Execute `MSDial.bat` for feature extraction and statistical analysis.  
     _Note: Both NEG and POS datasets must be ready before running this step._
   - Execute `Annotation-MSDial-NEG.bat` for annotating NEG features extracted and selected after running `MSDial.bat`.
   - Execute `Annotation-MSDial-POS.bat` for annotating POS features extracted and selected after running `MSDial.bat`.

3. **Output:**
   - All statistical results and CSV files will be generated in the `04-codeOutput` directory.
