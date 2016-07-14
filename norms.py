from sympy import *
from time import sleep
from sys import argv
import sys
import copy
import itertools


script, step = argv #step can be 'a' or 'b' (cf. Description section below)


#================================================================================#
#
#				NORM COMBINATORICS COMPUTATIONS
#
#================================================================================#


#----------------#
#  DESCRIPTION
#----------------#

#This program, when run, will consider all possible cases of x in O_1 (i.e. all choices
#of x not in N(5), 1+x in N(5)), and in each case attempt to work out the value of
#1+kx for k in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 1/5, -1/5], using the method of
#norm combinatorics. If step = 'a', the script will output the result of this
#computation. 

#If step ='b', the program will check, given x,y in O_1, what the possible value of
#1-xy is. It checks then whether all the possible values are in Norm(5) in order to
#verify the proof.


#---------------------------------------------------------------------------------#

#First some preliminary functions


#Defining the norm groups
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
		pass


#When doing various norm-decompositions, we end up working with values other than
#1,-1,2,-2,5,-5 and 10,-10. When encountering such values we can easily reduce it
#to one of those values by working out its square value. We did this here using the 
#characterisation of squares in Q_2 via mod 8 arithmetic.


#Given an integer x, this function returns u, n such that x = u*2^n, with u odd.
def factor2(x):

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
	


#This determines square value of integer x by checking the value of u modulo 8.	
def normalise(x):
	
	u, n = factor2(x)
	m = n % 2
	list = [1,-1,2,-2,5,-5,10,-10]
	new = [x for x in list if u*x % 8 == 1]
	sq = (2**m)*new[0]
	
	return sq
	
	
	

#Sometimes in our computations we will find that the value of 1+Nx is in a*Norm(b).
#This function works out what this set will be.
def normul(a, S):
	if type(S) == list:
		return [normalise(a*s) for s in S]
	else:
		pass
		#print 'Error, second argument is not a list'	
	

#This function multiplies numbers together, normalising everything modulo squares	
def f(a,b):
	if not(type(a) == int):
		print a
		print 'Error: input must be integer. You tried %r' % a
	elif not(type(b) == int):
		print b
		print 'Error: input must be integer. You tried %r' % b
	else:		
		return normalise(normalise(a)*normalise(b))	
							


#Calculates norm-group associated with decomposition 1+nx = (1+mx)+(n-m)x. 
#Here a = x, b = 1+mx	
def norm_com(a, b, n, m):  

	constraint_1 = normul(b, Norm(f(-(n-m), a*b)))
	constraint_2 = normul(1, Norm(f(-n, a)))
	intersection = set(constraint_1).intersection(set(constraint_2))
	
	return list(intersection)
	
	
#Calculates norm-group associated with decomposition 1+x/n based on knowledge of
#1+mx. Here a = x and b = m+x.
def norm_com_frac(a, b, n, m):

	constraint_1 = normul(n, Norm(-f(n,a)))
	constraint_2 = normul(normalise(n*m*m-m), Norm(-f(n*m-1,b)))
	intersection_1 = set(constraint_1).intersection(set(constraint_2))
	
	return list(intersection_1)	




#-----------------------------------------------------------------------------------#

#Now the main norm-combinatorics computation


#Defining a symbolic variable x so we can talk about things like 1+kx in Python
#unambiguously. The symbol y will be used only later when working out values of
#1-xy for x,y in O_1.

x = Symbol('x')
y = Symbol('y')


#This function will take as input a case, i.e. a choice of value of x and 1+x, and
#work out from this the values of 1+kx for k = 2,3,4,5,-1,-2,-3,-4,-5.

def step1_check(case): 

	#case is a dictionary associating x to its square value, 1+x to its square value
	C = case

	#This works out value of 1+Nx
	def determine(N):
    
    	#At first sight the possible square value of 1+Nx could be anything:
		possible_vals = {1,-1,2,-2,5,-5,10,-10}
		
		#We start by constraining 1+Nx based on the values known in C. Each time we loop
		#through this function we will update C so that we can put more and more initial
		#constraints on it
			
		known_scalars = [scalar for scalar in [1,2,3,4,5,-1,-2,-3,-4,-5] \
										   if 1+scalar*x in C]
		
		
		for scalar in known_scalars:
			if not(N == scalar):
			
				#print "1+%dx = %d" % (scalar, C[1+scalar*x])
				#print "ERROR TEST: "
				#print N, scalar, C[1+scalar*x], C[x], f(-(N-scalar), C[x]*C[1+scalar*x])
				#print normul(C[1+scalar*x], Norm(f(-(N-scalar), C[x]*C[1+scalar*x])))
				
				possible_vals = possible_vals.intersection(\
				                              norm_com(C[x], C[1+scalar*x], N, scalar))
			else:
				pass
		
		possible_vals_list = list(possible_vals)		
		
		#We now form a list of constrained values of 1+Nx. The idea is that currently
		#we haven't constrained more than the values in possible_vals_list above. We now
		#perform some computations to see if we can rule out any of those values. If we
		#can't, we add those values to constrained_vals. If we can, we don't. In this way
		#we form a new list of possible values of 1+Nx, which hopefully will end up
		#containing only a single element.
		
		constrained_vals_N = []
	
		#If the existing constraints from C already determine the value of 1+Nx, we are
		#done:
		
		#print "Possible values of 1+%dx are: " % N + str(possible_vals_list)
		
		if len(possible_vals_list) == 1:
		
			#print "Didn't need to do anything extra! 1+%dx must be in " % N \
			#	   + str(possible_vals_list) 
				   
			return possible_vals_list
			
		#Otherwise we need to do the extra computations as indicated above.
			
		else:	
			#print "1+%dx must be in " % N + str([ps for ps in possible_vals])

			#The strategy is as follows: our constraints have given us some number of
			#possible values for 1+Nx. For each such value, we look at what constraints
			#are now put on 1+(N+1)x. Again, there will be a limited number of possible
			#cases here (usually 1 or 2). For each of THESE cases we then look at possible
			#values for 1+mx (m=2,3,4,5,-1,-2,-3,-4,-5). At this point there are enough
			#constraints so we are essentially guaranteed to pin these values down. If any
			#of these values are impossible (i.e. if the list of possible values for some 
			#1+mx is []), we have a contradiction, ruling out that choice of 1+(N+1)x. If 
			#all choices of 1+(N+1)x yield a contradiction, we have ruled out the initial 
			#choice of 1+Nx. In this way we rule out various possible values of 1+Nx until
			#we end up with just one possible value. This is the desired result.
			
			#This is done to work out, from x and 1+x, the value of 1+2x, 1+3x, 1+4x
			#and 1+5x. Then the negative values are worked out from these.
			
			for val in possible_vals:

				C[1+N*x] = val #updating our case based on this assumption
				
				#Initially 1+(N+1)x can be anything:
				constraints = {1,-1,2,-2,5,-5,10,-10} 
				
				#Then we constrain it based on the current state of C
				for M in range(1, N+1):
					if not(N+1 == M):
						constraints = constraints.\
									  intersection(norm_com(C[x], C[1+M*x], N+1, M))
					else:
						pass
				
				constraint_list = list(constraints)
			
			
				#print "Given 1+%dx=%d, 1+%dx must be in " % (N,val, N+1) + \
				#		str(constraint_list)
				#print "Let's check each possibility in turn."
				
				cases_tested = 0
				
				#Now we loop through possible values of 1+(N+1)x
				for val_2 in constraint_list:
		
					C[1+(N+1)*x] = val_2

					possible_contradictions = []
		
					#Then we look to fill possible_contradictions with lists containing
					#possible values of 1+kx.
					
					range_to_consider = [4, 5, -1, -2, -3, -4, -5]
					for n in [r for r in range_to_consider if not(r == N+1)]:
		
						try:
							new_constraints = {1,-1,2,-2,5,-5,10,-10}
						
							for L in range(1,N+2):
								if not(n == L):
									new_constraints = new_constraints.\
									intersection(norm_com(C[x], C[1+L*x], n, L))
								else:
									pass
							
							#For transparency we attach a label to each list to indicate
							#what 1+kx the constraints are attached to
							new_constraint_set = new_constraints.union({'1+%dx' % n})
							
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
						pass
		
					#Otherwise we have found a contradiction, so we update our
					#cases_tested to reflect this
					else:
					#	print "Contradiction obtained! 1+%dx can't be %r. Contradiction \
					#         was found by considering: " % (N+1,val_2) \
					#		+ str(contradictions)	
				
						cases_tested += 1
				
				#If we have obtained a contradiction in all cases, we have ruled out
				#this possibility of 1+Nx, so we DON'T append it to our constrained
				#values of 1+Nx
				
				if 	cases_tested == len(constraint_list):
					pass
					
				#If we failed to find a contradiction in all cases, we were unable to
				#rule out this choice of 1+Nx, so it is still a possible value. Therefore
				#we append it to the constrained values:
					
				else:
					constrained_vals_N.append(val)
			
		
			#print "Conclusion: 1+%dx must be in " % N + str(constrained_vals_N)	
			#print C				
			return constrained_vals_N	


	#This then runs the above for values 2,3,4,5.
	def positives():

		forced_positive_values = []
	
		for s in range(2,6):
			
			new = determine(s)
			
			#'new' is a list of the possible values of 1+Nx. If this list has one element,
			#we have successfully constrained the value: 1+Nx has value the unique
			#element in 'new'. Otherwise we return an Error.
			
			if len(new)==1:
				new_pos = new[0]
			else:
				sys.exit("Error: failed to constrain value!")	
				
			forced_positive_values.append(new_pos)
			
			#Finally we append the value of 1+Nx we have worked out to our dictionary
			#so it can be used to constrain the next values
			
			C[1+s*x] = new_pos
		
		if step == 'a':	
			print "Positive values: " + str(forced_positive_values)
		else:
			pass	
		#print C



	#Then for negative values. The negative values are actually worked out through
	#initial constraints alone, based on already having determined the positive values.
	
	def negatives():

		forced_negative_values = []
		
		for S in [-1, -2, -3, -4, -5]:
			
			new = determine(S)
			
			if len(new)==1:
				new_neg = new[0]
			else:
				sys.exit("Error: failed to constrain value!")
					
			#new_neg = determine(S)[0]
			forced_negative_values.append(new_neg)
			C[1+S*x] = new_neg
	
		if step == 'a':
			print "Negative values: " + str(forced_negative_values)
		else:
			pass	
		#print C

	def all_forced_values():

		positives()
		negatives()
		
		return C
		
	all_forced_values()
	return C


#A function that will simply return the updated dictionary of cases, for later
#convenience
def step1_cases(case):

	return step1_check(case)
	
	


#-----------------------------------------------------------------------------------#


#step1_check({x : 2, 1+x : 1})
#step1_check({x : 2, 1+x : -5})
#step1_check({x : -2, 1+x : 1})
#step1_check({x : -2, 1+x : -1})
#step1_check({x : 10, 1+x : 1})
#step1_check({x : 10, 1+x : -5})
#step1_check({x : -10, 1+x : 1})
#step1_check({x : -10, 1+x : -1})


	

#---------------------------------------------------------------------------------#


#Now fractional values. Here, to avoid extra complications, we will only work
#out the values of 1+x/5 and 1-x/5. We will do so using only the constraints imposed
#from knowing values of 1+kx, k=-5,...5. 


def step2_check(case):
	
	#As before, case is a dictionary associating x to its square value, 1+x to its 
	#square value. We now flesh out this dictionary to include the values of 1+kx, 
	#k=-5,...5, that we worked out above
	
	D = step1_cases(case)
	
	#In case you want to explicitly see what these area in the output, unhash the next 
	#line:
	
	#print D
	
	#This works out value of 1+x/N. We will really determine N+x, and then divide out at
	#the end
	def determine_frac(N):
    
		possible_vals = {1,-1,2,-2,5,-5,10,-10}
			
		known_scalars = [1,2,3,4,5,-1,-2,-3,-4,-5] 
		
				
		for scalar in known_scalars:
			if not(N*scalar == 1):
				
				#We do try/except to avoid having to add loads more values to the 
				#normalise function. This tells it to only check constraints where we
				#don't need to add more such values.
				
				try: 
					possible_vals = possible_vals.intersection(\
				                              norm_com_frac(D[x], D[1+scalar*x], N, scalar))
				                              
				except:
					pass
					                              
			else:
				pass
		
		possible_vals = possible_vals.intersection(set(Norm(5)))
		possible_vals_list = list(possible_vals)		
		
		#We're not going to do more constraining now. In fact what we have is already
		#enough. This isn't clear already, but is visible in the output.
		
		return possible_vals_list
		

	def positive_fracs():
	
		new_pos_frac = determine_frac(5)
		actual_new_pos_frac = [f(5,value) for value in new_pos_frac]
		
		#print "Value of 5+x is in " + str(new_pos_frac)	
		if step == 'a':
			print "Value of 1+x/5 is in " + str(actual_new_pos_frac)
		else:
			pass	
		
		if len(actual_new_pos_frac)==1:
			D[1+x/5] = actual_new_pos_frac[0]
		else:
			pass	


	
	def negative_fracs():

		
		new_neg_frac = determine_frac(-5)
		actual_new_neg_frac = [f(-5,value) for value in new_neg_frac]
		
		#print "Value of -5+x is in " + str(new_neg_frac)
		if step == 'a':
			print "Value of 1-x/5 is in " + str(actual_new_neg_frac)
		else:
			pass
			
		if len(actual_new_neg_frac)==1:
			D[1-x/5] = actual_new_neg_frac[0]
		else:
			pass	


	def all_forced_fracs():

		positive_fracs()
		negative_fracs()

	
	all_forced_fracs()
	return D
	
	
	
def step2_cases(case):

	return step2_check(case)
	
	




#=====================================================================================#
#=====================================================================================#


#Now we actually perform the computations.


#All possible cases
cases = [ {x : 2, 1+x : 1}, {x : 2, 1+x : -5}, {x : -2, 1+x : 1}, {x : -2, 1+x : -1}, \
		  {x : 10, 1+x : 1}, {x : 10, 1+x: -5}, {x : -10, 1+x : 1}, {x : -10, 1+x : -1} ]



#Testing all cases one at a time and printing the output.

def main1():
	
	for case in cases:
		print 37*'-'
		print "Case = " + str(case)
		step2_check(case)
		#sleep(0.5)


#And we're done!



#=====================================================================================#
#=====================================================================================#


#Next goal is to check that if x,y are in O_1, then 1-xy is in N(5). This will 
#complete the proof that O_1 union O_2 is a valuation ring.


#This function works out the possible square values of 1-xy using the a-decomposition.
#Here b is 1+ay, c is 1+ax.
def decomposition_a(x, y, a, b, c):

	constraint_1 = Norm(f(x,y))
	constraint_2 = normul(b, Norm(f(c, b*a*y)))
	constraint_3 = normul(c, Norm(f(b, c*a*x)))
	intersection_1 = set(constraint_1).intersection(set(constraint_2))
	intersection_2 = intersection_1.intersection(set(constraint_3))
	
	return list(intersection_2)


#print f(-1,(-1)*(-5)*1*(-10))
#print normul(-1, Norm(f(-1, (-1)*(-5)*1*(-10))))	
#print decomposition_a(2, -10, 1, -1, -5)
#{x : 2, 1+x : -5}, {x : -10, 1+x : -1}




def step3_check(case_x, case_y):

	#Importing the currently known values of 1+kx and 1+ky for this particular case,
	#k in [1, -1, 2, -2, ..., 1/5, -1/5].
	case_x_copy = copy.deepcopy(case_x)
	case_y_copy = copy.deepcopy(case_y)
	C_x = step2_cases(case_x_copy)
	C_y = {}
	C_y[y] = case_y_copy[x]
	C_y[1+y] = case_y_copy[1+x]
		
	for k in [-5,-4,-3,-2,-1, 2,3,4,5]:
		
		C_y[1+k*y] = step2_cases(case_y_copy)[1+k*x]
		
	C_y[1+y/5] = step2_cases(case_y_copy)[1+x/5]
	C_y[1-y/5] = step2_cases(case_y_copy)[1-x/5]
	
	
	#To begin with the value of 1-xy could be anything
	possible_vals = {1,-1,2,-2,5,-5,10,-10}
	
	#Then we constrain it using the a-decomposition for different a:
	for a in [1, -1, 5, -5]:
		
		try:
			new_constraint = decomposition_a(C_x[x], C_y[y], a, C_y[1+a*y], C_x[1+a*x]) 
			possible_vals = possible_vals.intersection(set(new_constraint))
		
		except:
			pass
			
	possible_vals_list = list(possible_vals)
	
	#We then return the constrained values of 1-xy. If successful this will be a list
	#containing only elements beloning to Norm(5)
	return possible_vals_list
		
	


#Now we check all the cases one by one.

			

def main2():
	
	case_count = 0
	truth_count = 0
	for case_x in cases:
	
		for case_y in cases:
			
			case_x_copy = copy.deepcopy(case_x)
			case_y_copy = copy.deepcopy(case_y)
			case_y_edit = {}
			case_y_edit[y] = case_y_copy[x]
			case_y_edit[1+y] = case_y_copy[1+x]
			value_xy = step3_check(case_x_copy, case_y_copy)
			
			case_count += 1
			
			if all(value in Norm(5) for value in value_xy):
				truth_count += 1
			else:
				pass	
			
			print "Case: " + str(case_x_copy) + ", " + str(case_y_edit)
			print "Value of 1-xy is in " + str(value_xy)
			print 45*"-"
	
		
	if truth_count == case_count:
		print "ALL CASES VERIFIED. QED"
	else:
		print "Verification failed"	



def main():
	
	sleep(0.5)
	
	print "BEGINNING PROOF VERIFICATION"
	
	sleep(1.0)
	
	print "First we compute, for each possible case of x in O_1,"\
		   +" the values of 1+kx, for k = -5, -4, ..., 5, 1/5, -1/5"
	print 40*"="
	
	sleep(5.0)
	
	main1()
	
	print 40*"="
	
	sleep(5.0)
	
	print "Next, we compute the values of 1-xy for all possible choices of $x,y in O_1$"
	
	sleep(3.0)
	
	main2()
	
	sleep(2.0)
	
	print "PROOF COMPLETE"
	print 40*"="
	

#main1()

#main2()	 

if step == 'a':
	main1()
	
elif step == 'b':
	main2()	
	
else:
	sys.exit("Error: step must be 'a' or 'b'")	
	
	
	
		   
	
	
	




