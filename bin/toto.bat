
cd codes

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" QC-validation.R
echo QC studied.

python sigDiff.py
echo QCDil studied.

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" PCA.R
echo PCA generated.

python PLS-Da.py
echo PLS-Da studied.

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" Volcano.R
echo volcano generated.

"C:\Program Files\R\R-4.1.3\bin\Rscript.exe" common-metabo-heatmap.R
echo commun_metabo generated.

echo Execution completed.
pause