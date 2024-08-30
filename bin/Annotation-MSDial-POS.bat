@echo off

start /wait "" ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\02.0-MS2mzmlThermo-POS\ -o ..\01-mzmlThermo\2.1-annotation_data_POS\ -m ..\01-mzmlThermo\02.0-MS2mzmlThermo-POS\M2parametrePOS.txt

cd codes

python annotation-POS.py
echo data generated.

pause