Os=(0 1 2 3 fast)
fs=(1 4 5 9)
filename="data.txt"
Niter=1
Npart=216
Nstat=1000

rm $filename
echo "#" ${fs[@]} >> $filename
echo "#" ${Os[@]} >> $filename
echo "#" $Npart >> $filename
for O in ${Os[@]}
do
  #make rmv
  make clean >/dev/null
  make O=$O >/dev/null
  python3 speed_test_python.py $Niter $Npart $Nstat $filename ${fs[@]}
done
