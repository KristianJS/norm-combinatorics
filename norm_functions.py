import sys
import copy
from sympy import *


'''
This script defines functions that will be used repeatedly in the norm combinatorics.

References to Propositions etc. refer to the paper "Recovering Valuations on Demushkin Fields".
'''



#Definition of the norm groups (a = +/1, +-2, +-5, +-10) (c.f. Proposition 3.2)
def Norm(a):
    
    if a == -1:
        return [1, 2, 5, 10]
    elif a == 2:
        return [1, -1, 2, -2]
    elif a == -2:
        return [1, 2, -5, -10]
    elif a == 5:
        return [1, -1, 5, -5]
    elif a == -5:
        return [1, 5, -2, -10]
    elif a == 10:
        return [1, -1, 10, -10]
    elif a == -10:
        return [1, -2, -5, 10]
    elif a == 1:
        return [1, -1, 2, -2, 5, -5, 10, -10]   
    else:
        sys.exit("Error in Norm: you tried Norm(%s) but I don't know how to deal with that!" % a)




'''
When doing various norm-decompositions, we end up working with integers other than
1,-1,2,-2,5,-5 and 10,-10. When encountering such numbers we can easily reduce it
to one of those 8 numbers by working out its value mod squares. The following functios 
do just that, using the characterisation of squares in Q_2 via mod 8 arithmetic.
'''

#Given an integer x, this function returns u, n such that x = u*2^n, with u odd.
def factor2(x):

    #Keep dividing by 2 until we get an odd number.
    n = 1
    while n <= abs(x):
        if not(x % 2**n == 0):
            return x, n-1
        else:
            if not(x/(2**n) % 2 == 0):
                return x/(2**n), n
            else:
                pass
        n += 1              
    


#This determines value of integer x modulo squares by checking the value of u modulo 8.
def normalise(x):
    
    #print x
    u, n = factor2(x)
    m = n % 2
    
    #The possible values
    l = [1,-1,2,-2,5,-5,10,-10]
    
    #Find which value is equivalent to the odd part of x modulo 8 (precisely one such number)
    new = [x for x in l if u*x % 8 == 1]
    
    #This gives us the desired answer
    sq = (2**m)*new[0]
    
    return sq
    
    
    

#Sometimes in our computations we will find that the value of 1+Nx is in a*Norm(b).
#This function works out what this set will be.
def normul(a, S):
    if type(S) == list:
        return [normalise(a*s) for s in S]
    else:
        #pass
        sys.exit("Error in normul: second argument is not a list!")   
    

#This function multiplies two integers together, normalizing everything modulo squares.   
def f(a,b):
    if not(type(a) == int):
        sys.exit("Error in f: input must be integer. You tried %r" % a)
    elif not(type(b) == int):
        sys.exit("Error: input must be integer. You tried %r' % b")
    else:       
        return normalise(normalise(a)*normalise(b)) 
                            


#Calculates norm-group associated with decomposition y = 1 + nx = (1 + mx) + (n - m)x.
#In other words, given such a y, the function returns the possible square values of y from the
#two constraints due to y=1+mx and y=(1+mx)+(n-m)x, for some integers m and n. 
#This is therefore computing the set C^n_m(x) defined in the paper.
def norm_com(a, b, n, m):  

    #Here a = x, b = 1+mx

    #The constraint from 1+nx
    constraint_1 = normul(1, Norm(f(-n, a)))
    
    #The constraint from (1+mx)*[1+(n-m)x/(1+mx)]
    #If we don't know 1+mx, then we don't get anything
    constraint_2 = normul(b, Norm(f(-(n-m), a*b)))

    #Intersect both constraints
    intersection = set(constraint_1).intersection(set(constraint_2))
    
    return list(intersection)
    
    

#This function constrains the square value of y=n+x given knowledge of 1+mx, integers n,m.
#Uses the decompositions y=n(1+x/n) and the following:
#
#Let 1+mx=b modulo squares. Then 
#
#   (1/m)+x=mb mod squares, and so 
#
#   n+x=mb*[a square]-(1/m)+n = (nm-1)/m + mb*[a square]
#
#and this final expression lives in m(nm-1)N((nm-1)b)
#This is therefore computing the set F^n_m(x) defined in the paper.
#Here a=x, b=1+mx
def norm_com_frac(a, b, n, m):

    #Constraint coming from 1+x/n
    constraint_1 = normul(n, Norm(-f(n,a)))
    
    #The second constraint explained above
    constraint_2 = normul(normalise(n*m*m-m), Norm(-f(n*m-1,b)))
    
    
    #Intersect both of these
    intersection_1 = set(constraint_1).intersection(set(constraint_2))
    
    return list(intersection_1)


#Given a choice of values (mod squares) of x, 1+x, 1+y, this function works out the possible 
#square values of 1-xy using the a-decomposition (a = +-1, +-2, +-3, +-4, +-5):
#
#   1-xy = (1+ay)[1+(1+x/a)*(-ay/(1+ay))]
#        = (1+ax)[1+(1+y/a)*(-ax/(1+ax))]
#
#Here b=1+ay, b2=1+y/a, c=1+ax, c2=1+x/a
#This is therefore computing the set D_a(x,y) defined in the paper.
def decomposition_a(x, y, a, b, c, b2, c2):

    #The basic constraint from 1-xy being in Norm(xy)
    constraint_1 = Norm(f(x,y))
    
    #The two constraints coming from the a-decomposition
    constraint_2 = normul(b, Norm(f(c2, b*a*y)))
    constraint_3 = normul(c, Norm(f(b2, c*a*x)))
    
    #Intersect all these constraints
    intersection_1 = set(constraint_1).intersection(set(constraint_2))
    intersection_2 = intersection_1.intersection(set(constraint_3))
    
    return list(intersection_2)


    
#Two useful function which swaps x's to y's (and vice versa) in a dictionary of symbolic values
def swap_x_to_y(case):
    
    x = Symbol('x')
    y = Symbol('y')
    
    sym = x
    sym_swap = y
  
    #If a 'y' is already in there we don't need to swap
    if y in list(case.keys()):
        return case
    else:
  
        case_copy = copy.deepcopy(case)
        case_swap = {}
   
  
        known_scalars = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5] \
                                           if (1+scalar*x in case)]
        known_scalars_frac = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5] \
                                           if (1+x/scalar in case)]


        for k in known_scalars:
            case_swap[sym_swap] = case_copy[sym]
            case_swap[1+k*sym_swap] = case_copy[1+k*sym]
        for k in known_scalars_frac:
            case_swap[sym_swap] = case_copy[sym]
            case_swap[1+sym_swap/k] = case_copy[1+sym/k]
    
        return case_swap
        
    
def swap_y_to_x(case):
    
    #print case
    
    x = Symbol('x')
    y = Symbol('y')
    
    sym = y
    sym_swap = x
  
    #If an 'x' is already in there we don't need to swap
    if x in list(case.keys()):
        return case
    else:
  
        case_copy = copy.deepcopy(case)
        case_swap = {}
        
    
        known_scalars = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5,1/5,-1/5] \
                                           if 1+scalar*sym in case]
                              
        for k in known_scalars:
            case_swap[sym_swap] = case_copy[sym]
            case_swap[1+k*sym_swap] = case_copy[1+k*sym]
        
        return case_swap
    
