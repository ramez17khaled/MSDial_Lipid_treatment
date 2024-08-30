# MSDial_Lipid_treatment
This program is an open source project, dedicate to lipids biomarckers detection and annotation after an orbitrap LC-MS/MS DDA analysis.
it take mzml format and return the biomarckers for two desies T and H and the commun metabolites between T and H. Further more, many statistical results will be visualisated.
Codes are adapted to work only with conditions in metadata of this project ! Improuvment will be come to handel other metadata and conditions.
Installation:
1- clone the repository or downlowad the zip firmat
2- prepare your dataset : 
 a- convert your row data to mzml format using MSConvert :
  - Proteowizard install : 'https://proteowizard.sourceforge.io/'
  - convert in MS1 and save the output to '01.0-MS1mzmlThermo-POS' for POS data and '01.0-MS1mzmlThermo-NEG' for NEG data
  - convert i MS2 and save the output to '02.0-MS2mzmlThermo-POS' for POS data and '02.0-MS2mzmlThermo-NEG' for NEG data
 b- Prepare your metadata in a csv file (with ';') for each data mode (POS and NEG) and save the files in '02-Nico_metadata'
 c- install 'MSDIAL ver.4.9.221218 Windowsx64' :  'https://systemsomicslab.github.io/compms/msdial/main.html'
 d- save the 'MSDIAL ver.4.9.221218 Windowsx64' in 'bin' (validate the PATH for execution in bat files)
 e- prepare the databases to use in the annotation process :
  - check the txt forma for inhouse DB for POS and NEG separatly
  - AND/OR download msp DB from MSDila : 'https://systemsomicslab.github.io/compms/msdial/main.html' and save it is '01-mzmlThermo'
3- Parameters and execution :
 a- adapte the parameters in '01-mzmlThermo\01.0-MS1mzmlThermo-NEG\NEGparametre.txt' for features extraction in NEG mode
 b- adapte the parameters in '01-mzmlThermo\01.0-MS1mzmlThermo-POS\POSparametre.txt' for features extraction in POS mode
 c- adapte the parameters in '01-mzmlThermo\02.0-MS2mzmlThermo-NEG\M2parametreNEG.txt' for features annotation in NEG mode
 d- adapte the parameters in '01-mzmlThermo\02.0-MS2mzmlThermo-POS\M2parametrePOS.txt' for features annotation in POS mode
 e- execute 'MSDial.bat' for features extraction and statistical analysis (both NEG and POS dataset must be ready !)
 f- execute 'Annotation-MSDial-NEG.bat' for data annotaion of NEG features extracted and selected after 'MSDial.bat' execution
 g- execute 'Annotation-MSDial-POS.bat' for data annotaion of POS features extracted and selected after 'MSDial.bat' execution
 h- all statistical results and csv output will be generated in '04-codeOutput'
