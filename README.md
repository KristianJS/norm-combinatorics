# norm-combinatorics
---Proof verification for the paper "Recovering Valuations on Demushkin Fields"---

The program has two parts, 'a' and 'b'.

Running "python norms.py 'a'" will prompt the program to attempt to calculate, given as input the square class of x and 1+x in O_1, the square classes of 1+ax, where a = 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 1/5, -1/5. The output will be, for each possible case x in O_1:

"Positive values", an array showing the computed values, in order, of 1+2x, 1+3x, 1+4x and 1+5x;
"Negative values", an array showing the computed values, in order, of 1-x, 1-2x, 1-3x, 1-4x, 1-5x;
The possible values of 1+x/5;
The possible values of 1-x/5

It is easy to verify by sight that all the output values are in N(5).

Running "python norms.py 'b'" will prompt the program to attempt to verify that for any x, y in O_1, that 1-xy is in N(5). It simply runs over all possible combinations of x,y (it does not appeal to symmetry and therefore there are twice as many computations as required) and uses all possible a-decompositions to attempt to pin down the value of 1-xy. It then checks if every output value is in N(5): if yes, it prints a "QED" line. Otherwise it prints an Error message.

In both cases, the program is told to terminate if it is unable to verify any single computation. The fact that it completes provides the proof verification. 
