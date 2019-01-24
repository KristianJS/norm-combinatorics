from sympy import *
from time import sleep
from sys import argv
import sys
import copy
import itertools
from norm_functions import norm_com, norm_com_frac, normalise
init_printing()



'''
This script contains the key norm combinatorics functions used.

(1) norm_combinatorics_int:

    Takes as input an integer N, values of x and 1+kx (mod squares) for all integers k where 1+kx 
    is known. Tries to work out the possible square values of 1+Nx using the yoga of norm
    combinatorics.
    
(2) norm_combinatorics_frac:
    
    Takes as input values of x and 1+mx (mod squares), m some integer, along with an integer n.
    Tries to work out the possible values of n+x (mod squares) using the fractional constraint.
    This immediately gives the value of 1+x/n (mod squares).
    
'''




#Defining a symbolic variable x so we can talk about things like 1+kx in Python unambiguously.
x = Symbol('x')




#Function which attempts to pin down value of 1+Nx from values of x and 1+kx (k=1,2,...)
#Input is a dictionary known_cases = {x : val_1, 1+x : val_2, 1+kx : val_k, ...}, giving the values
#of x, 1+x and 1+kx (mod squares) for any integer k where the value of 1+kx is known.
#Returns a list containing the possible values of 1+Nx (mod squares) deduced via norm combinatorics.
#The argument 'outfile' is the textfile where all the output gets written to.
def norm_combinatorics_int(known_cases, N, outfile):
    

    #Renaming dictionary and outfile for ease of use
    C = known_cases
    f = outfile
       
    #A priori the possible value of 1+Nx could be anything:
    possible_vals = {1,-1,2,-2,5,-5,10,-10}
        
    #We start by constraining 1+Nx based on the values known in C.     
    known_scalars = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5] \
                                           if 1+scalar*x in C]
        
    
    #Write some text to file
    f.write(100*'=')
    f.write('\n')
    if N > 0:
        f.write("            *** Attempting to pin down value of 1+%sx (mod squares). ***\n" % N)
    elif N == -1:
        f.write("            *** Attempting to pin down value of 1-x (mod squares). ***\n")
    else:
        f.write("            *** Attempting to pin down value of 1-%sx (mod squares). ***\n" % (-N))
    f.write('\n')
    f.write("This is what we know so far:\n")
    
    
    string = '    '
    basicstring = string + '%r ~ %s, %r ~ %s' % (x, C[x], 1+x, C[1+x])
    for key in C.keys():
        string += '%r ~ %s, ' % (key, C[key])

    f.write('\n' + string[:-2] + '.\n')
    f.write('\n')
    
    #If N is a known scalar then we're done already
    if N in known_scalars:
        f.write("N=%s is already known. Returning its value.\n" % (1+N*x))
        return [C[1+N*x]] #Return in a list for consistency!
    
    
    #Otherwise we carry on
    else:
        pass
        
    
    #Constrain for each known scalar, one at a time
    for scalar in known_scalars:

        constraint_from_scalar = norm_com(C[x], C[1+scalar*x], N, scalar)
        possible_vals = possible_vals.intersection(constraint_from_scalar)

    #Turn the set back into a list      
    possible_vals_list = list(possible_vals)        
        
  
    #If these initial constraints already determine the value of 1+Nx, we are done:
    f.write("Applying first-order constraints shows that the possible values of %r are: " \
            % (1+N*x) + str(possible_vals_list) +'.\n')
        
    if len(possible_vals_list) == 1:
        
        f.write("Didn't need to do anything extra!\n")
        f.write(100*'-')
        f.write('\n')
        f.write("Conclusion: %s ==> %r ~ " % (basicstring[4:], 1+N*x) + \
                                              str(possible_vals_list[0]) + '.\n')        
        return possible_vals_list
     
            
    #Otherwise we need to do some more work. 
    #We have an initial list of constrained values of 1+Nx, based on the 'first-order' 
    #constraints coming from already known scalars. We now perform some computations to see 
    #if we can rule out any of the values in this list by going down a level to 'second-order'
    #constraints. In this way we form a new list of possible values of 1+Nx, which hopefully
    #will end up containing only a single element.
                     
    else:
        f.write("Thus first-order constraints did not suffice to pin down the value uniquely.\n")
        f.write("Let's attempt second-order constraints as well.\n")

        #The strategy is as follows: our constraints have given us some number of
        #possible values for 1+Nx. For each such value, we look at what constraints
        #are now put on 1+(N+1)x, using both constraints from C and our new constrain
        #from our assumption about 1+Nx. Again, there will be a limited number of possible
        #cases here. For each of THESE cases we then look at possible values for 1+mx
        #(m=2,3,4,5,-1,-2,-3,-4,-5). At this point there are enough constraints that we are
        #essentially guaranteed to pin these values down. If any of these values are impossible
        #(i.e. if the list of possible values for some #1+mx is empty), we have a 
        #contradiction, ruling out that choice of 1+(N+1)x. If all choices of 1+(N+1)x yield a
        #contradiction, we have ruled out the initial choice of 1+Nx. In this way we will try
        #to rule out all possible values of 1+Nx bar one. This remaining value then must
        #necessarily be the unique value of 1+Nx (mod squares).
            
            
        #This is the list we hope to populate with only one final number
        constrained_vals_N = []
            
            
        #Looping over the possible values of 1+Nx to see if we can obtain a contradiction.
        for val in possible_vals:
            f.write(100*'-')
            f.write('\n')
            f.write("Assume that %r ~ %s.\n" % (1+N*x, val))
            f.write('\n')
                
            #Create a copy of C and known_scalars that we can work with
            C_new = C.copy()
            known_scalars_new = known_scalars
                
            #Updating both using our assumption about 1+Nx
            C_new[1+N*x] = val 
            known_scalars_new.append(N)
                
            #There are no initial constraints on 1+(N+1)x
            constraints = {1,-1,2,-2,5,-5,10,-10} 
                
            #Then we constrain it based on the current state of C_new
            for M in known_scalars_new:
                    
                #Have to omit cases where M==N+1 and N+1=0 as the constraint is useless there
                if M in [N+1]:
                    pass
                else:
                    if N+1 == 0:
                        pass
                    else:
                        #print N+1, M
                        constraint_from_M = norm_com(C_new[x], C_new[1+M*x], N+1, M)
                        constraints = constraints.intersection(constraint_from_M)
                    
            #Turn the set into a list
            constraints_list = list(constraints)
                
            #It may be that our assumption immediately gives a contradiction in that 1+(N+1)x may
            #not have any possible values available! In this case we have already ruled out this
            #value of 1+Nx
            
            if constraints_list == []:
		        
		        f.write("    ---> Contradiction obtained! Intersecting the constraints on %r gives the empty set.\n" % (1+(N+1)*x))
		        f.write("    (In this case, we have the following assumptions in place:\n")
		        f.write("     %s\n" % C_new)
		        f.write("     Use the basic constraints on %r coming from these.)\n" % (1+(N+1)*x))
		        f.write('\n')
		        f.write("Hence the possibility that %r ~ %s can be ruled out.\n" % (1+N*x, val))
                

		    #Otherwise we need to go deeper still
            else:
                f.write("Given %r ~ %s, first-order constraints show that %r must be in " \
                         % (1+N*x, val, 1+(N+1)*x) + str(constraints_list) + '.\n')
                f.write("Let's consider each possibility in turn.\n")
                
                
                #Now we loop through the possible values of 1+(N+1)x
                cases_tested = 0
                for val_2 in constraints_list:
                    
                    f.write("    Assume %r ~ %s.\n" % (1+(N+1)*x, val_2))
                    
                    #Again updating known cases
                    C_new[1+(N+1)*x] = val_2
                    known_scalars_new.append(N+1)

        
                    #Then we look to obtain a contradiction by considering possible values of
                    #1+kx, for different values of k. Any contradictions obtained get added to
                    #the following list:
                    possible_contradictions = []
                                        
                    #The values of k we will consider
                    range_to_consider = [4, 5, -1, -2, -3, -4, -5]
                    
                    #We don't want to consider N+1 however because we get a meaningless constraint
                    if N+1 in range_to_consider:
                        range_to_consider.remove(N+1)
                    
                    #Now loop over the range
                    for n in range_to_consider:
                        try:
                            #No initial constraints
                            new_constraints = {1,-1,2,-2,5,-5,10,-10}
                           
                            for L in known_scalars_new:
                            
                                #As always avoiding meaningless constraints
                                if L == n:
                                    pass
                                
                                else:
                                    constraint_from_L = norm_com(C_new[x], C_new[1+L*x], n, L)
                                    new_constraints = new_constraints.intersection(constraint_from_L)
                                    

                            #For transparency we attach a label to each list to indicate
                            #what 1+kx the constraints are attached to
                            new_constraint_set = new_constraints.union({'%r' % (1+n*x)})
                            new_constraint_list = list(new_constraint_set)
                                        
                            possible_contradictions.append(new_constraint_list)

                        except:
                            pass
                    

                    #A contradiction is a list in possible_contradictions which is empty,
                    #meaning it has length 1, given that all the lists have their label
                    #in them:                  
                    contradictions = [y for y in possible_contradictions if len(y) == 1]
                   
                    
                    #If there were no contradictions, move on
                    if contradictions == []:
                        f.write("    ---> No contradictions obtained via second order constraints.\n")
        
                    #Otherwise we have found a contradiction, so we update our cases_tested to
                    #reflect this
                    else:
                        f.write("    ---> Contradiction obtained! %r can't be %s. Contradiction was found by considering " % (1+(N+1)*x,val_2) + str(contradictions[0][0]) + '.\n')
                        f.write("         (In this case, we have the following assumptions in place:\n")
                        f.write("          %s\n" % C_new)
                        f.write("          Use the basic constraints on %s coming from these.)\n" % str(contradictions[0][0]))
                        cases_tested += 1
                    
                #If we have obtained a contradiction in all cases, we have ruled out
                #this possibility of 1+Nx, so we DON'T append it to our constrained
                #values of 1+Nx                
                if cases_tested == len(constraints_list):
                    f.write('\n')
                    f.write("Hence we have ruled out the possibility that %r ~ %s!\n" \
                             % (1+N*x, val))
                   
                #If we failed to find a contradiction in all cases, we were unable to
                #rule out this choice of 1+Nx, so it is still a possible value. Therefore
                #we append it to the final constrained values:                
                else:
                    f.write('\n')
                    f.write("Hence the possibility that %r ~ %s cannot be ruled out.\n" \
                                 % (1+N*x, val))
                    constrained_vals_N.append(val)
            
            
    #Write some concluding texts summarizing what we have learned
    f.write(100*'-')
    f.write('\n')
    if len(constrained_vals_N) == 1:
        f.write("Conclusion: %s ==> %r ~ " % (basicstring[4:], 1+N*x) + \
                                              str(constrained_vals_N[0]) + '\n')
    else:
        f.write("Conclusion: %r must be in " % (1+N*x) + str(constrained_vals_N) + '\n')
    f.write(100*'=')
    f.write('\n')
            
    #Return the final list of possible values
    return constrained_vals_N
    

#Function to determine 1+x/N given known values of x and 1+kx for any integer k where this is known.
#Returns a list of possible values of 1+x/N
#Computations go via determining N+x and then multiplying final value by N
def norm_combinatorics_frac(known_cases, N, outfile):

    x = Symbol('x')

    #Renaming dictionary/outfile for ease of use
    C = known_cases
    f = outfile
    
    #A priori the possible value of N+x could be anything:
    possible_vals = {1,-1,2,-2,5,-5,10,-10}
    
    #We start by constraining N+x based on the values 1+kx known in C. The permissible k are:   
    known_scalars = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5] \
                                          if 1+scalar*x in C]
    
    
    #Write some text to screen
    f.write(100*'=')
    f.write('\n')
    f.write("            *** Attempting to pin down value of %s+x (mod squares). ***\n" % N)
    f.write('\n')
    f.write("This is what we know so far:\n")
    f.write('\n')
    
    string = '    '
    basicstring = string + '%r ~ %s, %r ~ %s' % (x, C[x], 1+x, C[1+x])
    for key in C.keys():
        string += '%r ~ %s, ' % (key, C[key])

    f.write(string[:-2] + '.\n')
    f.write('\n')  
       
    #Loop over these and add constraints using norm_com_frac         
    for scalar in known_scalars:
    
        #Omit 1/N as this gives a meaningless constraint
        if not(N*scalar == 1):
            constraint_from_scalar = norm_com_frac(C[x], C[1+scalar*x], N, scalar)
            #print scalar
            #print constraint_from_scalar
            possible_vals = possible_vals.intersection(constraint_from_scalar)
                                     
        else:
            pass
        
        
    possible_vals_list = list(possible_vals)
    
    #Turn constraint on N+x into constraint on 1+x/N
    possible_vals_list_mult = [normalise(N*elt) for elt in possible_vals_list] 
    
    #print possible_vals_list
    #print possible_vals_list_mult
        
    if len(possible_vals_list) == 1:
        #We get value of 1+x/N by multiplying by N and normalising
        val = possible_vals_list_mult[0]
        f.write("First-order constraints show that %s+x ~ %s\n" % (N, possible_vals_list[0]))
        f.write(100*'-'+'\n')
        f.write("Conclusion: %s ==> %r ~ " % (basicstring[4:], N+x) + \
                                              str(possible_vals_list[0]) + '\n')
        f.write(31*' ' + "==> %r ~ %s" % (1+(x/N), val) + '.\n')
    else:
        #We do not perform second-order constraints as first-order is already enough.      
        f.write("First-order constraints show that %s+x must be in %s\n" % (N, possible_vals_list))

    return possible_vals_list_mult
   
