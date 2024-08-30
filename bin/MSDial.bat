@echo off

set LOGFILE=..\04-codeOutput\execution_log.txt

echo Execution started at %date% %time% > %LOGFILE%

cd ..\01-mzmlThermo
mkdir 1.1-Data_POS >> %LOGFILE% 2>&1
mkdir 1.1-Data_NEG >> %LOGFILE% 2>&1

cd ..\bin

echo Running MSDial with POS parameters >> %LOGFILE%
echo Command: ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\01.0-MS1mzmlThermo-POS\ -o ..\01-mzmlThermo\1.1-Data_POS\ -m ..\01-mzmlThermo\01.0-MS1mzmlThermo-POS\POSparametre.txt >> %LOGFILE%
echo Parameters used: >> %LOGFILE%
type ..\01-mzmlThermo\01.0-MS1mzmlThermo-POS\POSparametre.txt >> %LOGFILE%
start /wait "" ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\01.0-MS1mzmlThermo-POS\ -o ..\01-mzmlThermo\1.1-Data_POS\ -m ..\01-mzmlThermo\01.0-MS1mzmlThermo-POS\POSparametre.txt >> %LOGFILE% 2>&1

echo Running MSDial with NEG parameters >> %LOGFILE%
echo Command: ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\01.0-MS1mzmlThermo-NEG\ -o ..\01-mzmlThermo\1.1-Data_NEG\ -m ..\01-mzmlThermo\01.0-MS1mzmlThermo-NEG\NEGparametre.txt >> %LOGFILE%
echo Parameters used: >> %LOGFILE%
type ..\01-mzmlThermo\01.0-MS1mzmlThermo-NEG\NEGparametre.txt >> %LOGFILE%
start /wait "" ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\01.0-MS1mzmlThermo-NEG\ -o ..\01-mzmlThermo\1.1-Data_NEG\ -m ..\01-mzmlThermo\01.0-MS1mzmlThermo-NEG\NEGparametre.txt >> %LOGFILE% 2>&1

echo Executing data reading script... >> %LOGFILE% 2>&1

cd codes

python pre_processing.py >> %LOGFILE% 2>&1
echo Data processed. >> %LOGFILE% 2>&1

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" QC-validation.R >> %LOGFILE% 2>&1
echo QC studied. >> %LOGFILE% 2>&1

python sigDiff.py >> %LOGFILE% 2>&1
echo QCDil studied. >> %LOGFILE% 2>&1

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" PCA.R >> %LOGFILE% 2>&1
echo PCA generated. >> %LOGFILE% 2>&1

python PLS-Da.py >> %LOGFILE% 2>&1
echo PLS-Da studied. >> %LOGFILE% 2>&1

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" Volcano.R >> %LOGFILE% 2>&1
echo Volcano generated. >> %LOGFILE% 2>&1

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" common-metabo-heatmap.R >> %LOGFILE% 2>&1
echo Common_metabo generated. >> %LOGFILE% 2>&1

echo Execution completed at %date% %time%. >> %LOGFILE% 2>&1
pause
