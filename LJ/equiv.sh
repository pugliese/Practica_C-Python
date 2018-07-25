Os=(0 3 fast)
filename="equiv.txt"
Npart=8

rm $filename
echo "#" ${Os[@]} >> $filename
for O in ${Os[@]}
do
  #make rmv
  make clean >/dev/null
  make O=$O >/dev/null
  python3 speed_test_python.py i $Npart $filename
done
