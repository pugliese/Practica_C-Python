Os=(0 1 2 3 fast)
fs=(1 2 3 4 5 6 7 8 9)
filename="dat.txt"
Niter=1
Npart=216
Nstat=1000

for O in ${Os[@]}
do
  make rmv
  make clean >/dev/null
  make O=$O >/dev/null
  rm $filename
  echo "#" ${fs[@]} >> $filename
  echo "#" ${Os[@]} >> $filename
  python3 speed_test_python.py $Niter $Npart $Nstat $filename ${fs[@]}
done
