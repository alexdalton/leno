#!bin/bash

bash ~/Scripts/ece198KL/lateSub.sh -d "2014-01-29 22:00" > results.txt
echo "Compilation Results" >> results.txt
echo "********************" >> results.txt
lc3as prog1.asm >> results.txt
lc3as testone.asm
lc3as testtwo.asm
lc3as testthree.asm
lc3sim -s runtestone > myoneout
lc3sim -s runtesttwo > mytwoout
lc3sim -s runtestthree > mythreeout
echo "" >> results.txt

echo "Testoneout diff:" >> results.txt
echo "********************" >> results.txt
diff -B myoneout testoneout >> results.txt
echo "" >> results.txt

echo "Testtwoout diff:" >> results.txt
echo "********************" >> results.txt
diff -B mytwoout testtwoout >> results.txt
echo "" >> results.txt

echo "Testthreeout diff:" >> results.txt
echo "********************" >> results.txt
diff  -B mythreeout testthreeout >> results.txt
