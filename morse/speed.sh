for O in 0 1 2 3 fast
do
  make clean >/dev/null
  make O=$O >/dev/null
  echo 'O'$O':'
  python3 speed_test_python.py 1 216 1000
done
