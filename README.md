# norm-combinatorics
---Proof verification for the paper "Recovering Valuations on Demushkin Fields"---

The program has two parts, 'a' and 'b'.

Running "python norms.py 'a'" will prompt the program to attempt to calculate, given as input the square class of x and 1+x, the square classes of 1+ax, where a = 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 1/5, -1/5. 

Running "python norms.py 'b'" will prompt the program to attempt to verify that for any x, y in O_1, that 1-xy is in N(5).

In both cases, the program is told to terminate if it is unable to verify any single computation. The fact that it completes provides the proof verification. 
