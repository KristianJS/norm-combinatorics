# norm-combinatorics

*** DESCRIPTION ***

Proof verification for the paper "Recovering Valuations on Demushkin Fields"
(written by J. Koenigsmann and K. Strommen; code produced by K. Strommen)

The Python scripts here contain code to carry out the norm-combinatorics algorithm
outlined in the paper, in order to prove Lemma 4.4 and Proposition 4.5, they key
computational results of the paper which prove the existence of a non-trivial
valuation.

The algorithm is described in the paper. 


*** REQUIRED PACKAGES ***

The only necessary package is sympy: https://www.sympy.org/en/index.html
With conda/mamba, this can be installed with 'conda install sympy'.

*** HOW TO USE THESE SCRIPTS ***

The proof can be generated by running 

> python GenerateProof.py

Several text-files are created, with the main one being ProofOfProposition.txt,
which contains the proof of Proposition 4.5, including references to the files 
DetermineValuesCaseN.txt (N=1,...8), which contain in essence the content of 
Lemma 4.4. The reader can simply read ProofOfProposition.txt, which tells
you at the relevant points which of the DetermineValues files to refer to.


*** NOTES ON CODE STRUCTURE ***

norm_functions.py defines a number of key functions that are used repeatedly
to compute various norm-groups and products of norm-groups by integers.

norm_combinatorics.py contains the main components of the algorithm, which
takes a choice of x in O_1 and tries to constrain the values of 1+ax for various
values of a. Fractional values of a are treated separately.

norm_checkcriteria.py is essentially a wrapper for carrying out the above
components recursively, and also contains the main code used to check the 
criterion of Proposition 4.6 for a specific choice of x and y in O_1.

Finally, GenerateProof.py is essentially a wrapper which loops the above functions
over all the possible cases, thereby completing the proof.




