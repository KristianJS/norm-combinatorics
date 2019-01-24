import sys
import os
from sympy import *
from norm_checkcriteria import check_valuation_criterion
from norm_functions import swap_x_to_y, swap_y_to_x
x = Symbol('x')
y = Symbol('y')



'''
====================================================================================================

                            EXPLANATION OF PROOF GENERATION

====================================================================================================

This script generates a full proof that in Case A, the ring O(N(5)), as defined in section 4,
is a valuation, by verifying the criteria of Lemma 4.1 in all possible cases.

We simply enumerate all the cases of pairs x,y in O_1 and check the criteria as follows:

    1) Norm combinatorics is first used to evaluate 1+kx, 1+ky for k=2,3,4,5,-1,-2,-3,-4,-5,1/5,-1/5
    2) Then the decompositions D_a(x,y) for a=1,-1,5,-5 are intersected.
    3) The resulting set is examined: if it's a subset of N(5) this case has been verified.
    
If all cases are verified, the proof is complete.

The computations are output in several text-files.

 * DetermineValuesCaseN.txt (N=1,...,8) ---> this file shows the computations that work out the values
                                             of 1+kx for various k, in case n
                                         
 * ProofOfProposition.txt ------------ ----> this file shows the verification of the norm criteria of
                                             Lemma 4.1 in all cases, proving Lemma 4.6.
                                         
Therefore the 9 text files produced give a full proof.

The cases are numbered as follows:
'''

case_1 = {x : 2, 1+x : 1} 
case_2 = {x : 2, 1+x : -5}
case_3 = {x : -2, 1+x : 1}
case_4 = {x : -2, 1+x : -1}
case_5 = {x : 10, 1+x : 1}
case_6 = {x : 10, 1+x: -5}
case_7 = {x : -10, 1+x : 1}
case_8 = {x : -10, 1+x : -1}


#####################################################################################################
#                                 Proceeding as outlined
#####################################################################################################

print 100*'='
print "Generating proof of Proposition 4.6..."


#We increment verified_cases for each succesfully verified case
verified_cases = 0


#The output file
f = open('ProofOfProposition.txt', 'w+')


#Writing some stuff to it
f.write(100*'=' + '\n')
f.write(100*'=' + '\n')
f.write(100*'=' + '\n')
f.write('\n')
f.write(35*' ' + "PROOF OF PROPOSITION 4.6\n")
f.write('\n')
f.write(100*'=' + '\n')
f.write(100*'=' + '\n')
f.write(100*'=' + '\n')
f.write("We need to show that for every possible pair of x,y in O_1, the value of 1-xy is in N(5).\n")
f.write("We proceed case by case.\n")
f.write("Recall, as explained in the paper, we can WLOG assume x ~ 2.\n")
f.write("Therefore, the following cases are indeed exhaustive.\n")

#All the pairs (with x~2): add the pair-numbering as well for naming text files
pairs = [ (case_1, case_1, (1,1)),\
          (case_1, case_2, (1,2)),\
          (case_1, case_3, (1,3)),\
          (case_1, case_4, (1,4)),\
          (case_1, case_5, (1,5)),\
          (case_1, case_6, (1,6)),\
          (case_1, case_7, (1,7)),\
          (case_1, case_8, (1,8)),\
          (case_2, case_2, (2,2)),\
          (case_2, case_3, (2,3)),\
          (case_2, case_4, (2,4)),\
          (case_2, case_5, (2,5)),\
          (case_2, case_6, (2,6)),\
          (case_2, case_7, (2,7)),\
          (case_2, case_8, (2,8))]
          

#Looping over these
for pair in pairs:
    case_x = pair[0]
    case_y = pair[1]
    casenums = pair[2]
    
    #We need to rename the 'x' to 'y' in the case_y dictionary
    case_y = swap_x_to_y(case_y)
    
    #Now we can check
    truth_val = check_valuation_criterion(case_x, case_y, casenums, f)
    
    if truth_val:
        verified_cases += 1
    else:
        pass

#If we verified all cases we are done
f.write(100*'=' + '\n')
f.write(100*'=' + '\n')
f.write('\n')
if verified_cases == len(pairs):
    f.write("All cases have been succesfully verified. This completes the proof. QED.\n")
    f.write('\n')
    f.write(100*'=' + '\n')
    f.write(100*'=') 
    print "Success! Proof details have been logged in ProofOfProposition.txt"
    print 100*'='
else:
    f.write("Failed to verify all cases. Proof was not succesful!\n")
    print "Proof did not succeed!"
    print 100*'='

#Close the file
f.close()





