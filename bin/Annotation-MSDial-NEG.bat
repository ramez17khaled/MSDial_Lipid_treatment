@echo off

start /wait "" ".\MSDIAL ver.4.9.221218 Windowsx64\MsdialConsoleApp.exe" lcmsdda -i ..\01-mzmlThermo\02.0-MS2mzmlThermo-NEG\ -o ..\01-mzmlThermo\2.1-annotation_data_NEG\ -m ..\01-mzmlThermo\02.0-MS2mzmlThermo-NEG\M2parametreNEG.txt

cd codes

python annotation-NEG.py
echo data generated.

pause

