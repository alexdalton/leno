timeout 3s lc3sim -s testFiles/runtest1 > testFiles/yourOut1
timeout 3s diff -b testFiles/yourOut1 testFiles/ourOut1 > testFiles/diff1

timeout 3s lc3sim -s testFiles/runtest2 > testFiles/yourOut2
timeout 3s diff -b testFiles/yourOut2 testFiles/ourOut2 > testFiles/diff2

timeout 3s lc3sim -s testFiles/runtest3 > testFiles/yourOut3
timeout 3s diff -b testFiles/yourOut3 testFiles/ourOut3 > testFiles/diff3

timeout 3s lc3sim -s testFiles/runtest4 > testFiles/yourOut4
timeout 3s diff -b testFiles/yourOut4 testFiles/ourOut4 > testFiles/diff4

timeout 3s lc3sim -s testFiles/runtest5 > testFiles/yourOut5
timeout 3s diff -b testFiles/yourOut5 testFiles/ourOut5 > testFiles/diff5

timeout 3s lc3sim -s testFiles/runtest6 > testFiles/yourOut6
timeout 3s diff -b testFiles/yourOut6 testFiles/ourOut6 > testFiles/diff6
