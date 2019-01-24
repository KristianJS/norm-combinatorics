import sys
import copy
from sympy import *
from norm_functions import decomposition_a, swap_x_to_y, swap_y_to_x
from norm_combinatorics import norm_combinatorics_int, norm_combinatorics_frac
init_printing()



'''
This script contains the function used to check the criteria of Proposition 4.6.

That is, we want to check that if x,y are in O_1, then 1-xy is in N(5). This will complete 
the proof that O_1 union O_2 is a valuation ring.

This is split into two functions. The first, 'determine_values', starts with a choice of x in O_1 
(i.e. a choice of values of x and 1+x mod squares) and tries to determine the values of 1+kx for
k=+-1,+-2,+-3,+-4,+-5.

The second, 'check_valuation_criterion', takes as input a pair x,y in O_1 (i.e. choices of the values
of x,1+x,y,1+y mod squares). It uses 'determine_values' on both x and y to get extra information
and then proceeds to try to check if 1-xy is in N(5).
'''



#Defining symbolic variables x, y.
x = Symbol('x')
y = Symbol('y')


#The function doing the check.
#Input is a dictionary {x : val_x, 1+x : val_{1+x}} where x ~ val_x, 1+x ~ val_{1+x}.
#The function attempts to work out values of 1+kx, 1+ky (k=+-1,+-2,+-3,+-4,+-5,+-1/5) by
#looping over the norm combinatorics functions repeatedly.
#Returns an updated dictionary with any values 1+kx added that it succesfully worked out.
#The argument casenum is just for ordering the cases so output files can be uniquely ordered.
def determine_values(case, casenum):

    #Rename the dictionary for ease of use
    C = case
    
    #File where output gets written to
    f = open('DetermineValuesCase%s.txt' % casenum, 'w+')
    
    
    #If this input came from a 'y' case, we switch it to an x
    if y in C.keys():
        C = swap_y_to_x(C)
        swap_back = True
    else:
        swap_back = False


    #Print some text
    f.write(100*'=')
    f.write('\n')
    f.write("                        CASE CONSIDERED: x~%s, 1+x~%s\n" % (C[x], C[1+x]))
    f.write(100*'=')
    f.write('\n')
    f.write("GOAL: determine values of 1+kx for various integers k.\n")
    f.write("We'll do them one at a time.\n")

    #Loop over the values of k we want to work out. First integer values.
    for k in [2,3,4,5,-2,-3,-4,-5,-1]:
        
        #Just call norm_combinatorics_int
        possible_vals_k = norm_combinatorics_int(C, k, f)
        
        #If we did succesfully constraint to one value, add it to C
        if len(possible_vals_k) == 1:
            #print "Uniquely constrained value of 1+%sx: adding it to known cases." % k
            C[1+k*x] = possible_vals_k[0]
        
        else:
            f.write("Failed to uniquely constrain value of 1+%sx. Moving on to next value." % k)
     
    #Then the two fractional values
    for k in [5, -5]:
    
        #Just call norm_combinatorics_frac
        possible_vals_k = norm_combinatorics_frac(C, k, f)
        
        #If we uniquely constrained the value, add it to C
        if len(possible_vals_k) == 1:
            C[1+(x/k)] = possible_vals_k[0]
        else:
            f.write("Failed to uniquely constrain value of %r. Moving on to next value." % (1+(x/N)))
    
    #Summarize what we have learned
    string = '    '
    for key in C.keys():
        string += '%r ~ %s, ' % (key, C[key])

    
    f.write(100*'=')
    f.write('\n')
    f.write(100*'=')
    f.write('\n')
    f.write("In summary, we have that in this case, norm combinatorics implies:\n")
    for key in C.keys():
        if key in [x, 1+x]:
            pass
        else:
            f.write('    %r ~ %s\n' % (key, C[key]))
    
    f.write(100*'=')
    f.close()

    #If the original case was a 'y' case, we swap it back now
    if swap_back:
        C = swap_x_to_y(C)

    #Return the (hopefully) fleshed out dictionary    
    return C
    

#Input: (1) choice of x and y in O_1 (i.e. choices of x, 1+x, y, 1+y mod squares)
#       (2) a tuple casenums (casenum_x, casenum_y) indicating the numbering for this case 
#       (2) a file 'outfile' where the output gets written to
#Output: True or False depending on whether 1-xy is necessarily in N(5) or not.
def check_valuation_criterion(case_x, case_y, casenums, outfile):


    #Make deep copy of dictionaries to avoid aliasing errors!!!
    C_x = copy.deepcopy(case_x)
    C_y = copy.deepcopy(case_y)
    
    
    #Get casenumbers from the casenum tuple
    casenum_x = casenums[0]
    casenum_y = casenums[1]
    
    #File where output gets written to
    f = outfile
    
    #Print some text
    f.write(100*'=')
    f.write('\n')
    f.write("                   CASE CONSIDERED: x~%s, 1+x~%s, y~%s, 1+y~%s\n" 
                                % (C_x[x], C_x[1+x], C_y[y], C_y[1+y]))
        
    f.write(100*'=')
    f.write('\n')
    f.write("GOAL: check if 1-xy is necessarily in N(5).\n")
    f.write(100*'-')
    f.write('\n')
    
    #First get all the info on 1+kx, 1+ky from norm combinatorics
    C_x = determine_values(C_x, casenum_x)
    C_y = determine_values(C_y, casenum_y)

    
    f.write("Norm combinatorics shows that in this case we have the following:\n")
    f.write('\n')
    for key in C_x.keys():
        if key in [x, 1+x]:
            pass
        else:
            f.write('    %r ~ %s\n' % (key, C_x[key]))
    f.write('\n')
    for key in C_y.keys():
        if key in [y, 1+y]:
            pass
        else:
            f.write('    %r ~ %s\n' % (key, C_y[key]))
    f.write('\n')      
    f.write("(see the files DetermineValuesCase%s.txt and DetermineValuesCase%s.txt for details)\n" \
             % (casenum_x, casenum_y))  
    
    
    #To begin with the value of 1-xy could be anything
    possible_vals = {1,-1,2,-2,5,-5,10,-10}
    
    #Then we constrain it using the a-decomposition for different a:
    f.write('\n')
    f.write("Now we will intersect the constraints coming from the a-decomposition (a=1,-1,5,-5).\n")
    f.write('\n')
    for a in [1, -1, 5, -5]:
    
        #Constraint from the a-decomposition
        new_constraint = decomposition_a(C_x[x], C_y[y], a, C_y[1+a*y], C_x[1+a*x])
        f.write("    Constraint from %s-decomposition: %s\n" % (a, list(new_constraint)))
        
        possible_vals = possible_vals.intersection(set(new_constraint))
        
    f.write('\n')
    f.write('Intersecting all of these shows that 1-xy is in ' + str(list(possible_vals)) + '.\n')
    
    #Check if it's a subset of N(5)
    N_5 = {1, -1, 5, -5}
    truth_value = possible_vals.issubset(N_5)
    
    #Write to file it is succeeded
    if truth_value:
        f.write('This is a subset of N(5)! Hence 1-xy is in N(5)\n')
    else:
        f.write('Unable to verify that this case satisfies the criterion.\n')
    
     
    #Return the truth value
    return truth_value
    
    
determine_values({x : 2, 1+x: 1}, 1)


