Os=(0)
Niter=(1 5 10 50)
filename="estabilizacion.txt"
Npart_bas=2
Npart_it=10
Nstat=100

rm $filename
for O in ${Os[@]}
do
  #make rmv
  make clean >/dev/null
  make O=$O >/dev/null
  python3 speed_test_python.py e $Npart_bas $Npart_it $Nstat $filename ${Niter[@]}
done
