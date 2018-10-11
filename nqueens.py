'''
Blake Ehrenbeck

Solving the nqueens problem with python!

This solution combines both the Least Constraining Value (LCV) heurisitc with Arc Consistency
To test only LCV without Arc Consistency please run as:
    python nqueens.py lcv

***Tested with Python 3.6.5***

'''

import sys
import random
import itertools
import sys

BOARD_SIZE = 20

 
def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
 

def make_arc_consistent(queens, n): 
    '''
    Implementation of the AC-3 algorithm
    '''
    def remove_inconsistent_values(queens_dict, arc):
        removed = False
        to_del = []
        for col in queens_dict[arc[0]]:
            # code is just modified under_attack  
            if any((abs(col - x) != abs(arc[0]-arc[1]))for i,x in enumerate(queens_dict[arc[1]])): # check for diag inconsistencies
                pass 
            else:
                removed = True
                to_del.append(col)
            
        
            possible = [x for x in queens_dict[arc[1]] if (abs(col - x) != abs(arc[0]-arc[1]))] 
            if len(set(possible) - set([col])) == 0: # check for vertical inconsistencies
                removed = True
                if col not in to_del:
                    to_del.append(col)
            
                     
        if not to_del:
            pass
        for item in to_del:
            queens_dict[arc[0]].remove(item)
        
        return removed
    
    # The queens_dict will hold the possible values for a column, format is row:[possible col values]
    queens_dict = {i:j for (i,j) in enumerate([[k for k in range(n)] for _ in range(n)]) } # build the queens dictonary by just initializing to all possible values

    
    for row,col in enumerate(queens):
        queens_dict[row] = [col] # if certain rows have already been assigned cols, fix them in the dict

    arc_q = list(itertools.permutations([i for i in range(n)],2)) # prepare a list of all the arcs, i.e. permutations of each row
    while arc_q:
        arc = arc_q.pop(0)
        if remove_inconsistent_values(queens_dict, arc): # if a value was removed from the possibilities add back neighboring arcs
            for k in range(n): 
                if k != arc[0] and k != arc[1]:
                    
                    arc_q.append((arc[0],k))
   
                         
    return queens_dict 
        

def least_constraining_cols(cols,queens,n):
    '''
    Returns an ordered list of columns by the number of constraints to remaining variables
    '''
    choice_dict = {col : 0 for col in cols}
    for choice in cols:
        for j in range(len(queens)+1, n):
            for col in range(n):
                # similar to under_attack but pretending we put down choice in the queens list
                if col in queens+[choice] or any(abs(col - x) == abs(j-i) for i,x in enumerate(queens+[choice])):
                    choice_dict[choice] += 1
    return [choice[0] for choice in sorted(choice_dict.items(),key=lambda x : x[1])] 

def solve(queens, n):
    
    lcv_only = False

    if(len(sys.argv)==2):
        if sys.argv[1] == 'lcv':
            lcv_only = True
    
    if lcv_only:
        print("LCV ONLY MODE")
    
    num_assignments = 0
    def rsolve(queens,n):
            
        nonlocal num_assignments
        if n == len(queens):
            print("Made " + str(num_assignments) + " assignments.")
            return queens
        else:
            
            
            if len(queens) == 0: # just step through one by one for the very first row
                for j in range(n):
                    num_assignments += 1
                    newqueens =  rsolve(queens+[j], n)
                    if newqueens != []:
                        return newqueens
                  
            
            queens_dict = make_arc_consistent(queens, n) # get a dictionary with consistent cols for a row 
            
            if (not lcv_only):
                if any(domain == [] for domain in queens_dict.values()): # if a row doesn't have a consistent col, short circuit
                    
                    return []
                
                if all(len(domain) == 1 for domain in queens_dict.values()): # if there's only one possible column for each row -> found a solution!
                    for j in range(len(queens),n):
                        num_assignments += 1
                        queens.append(queens_dict[j][0])
                    newqueens = rsolve(queens, n)
                    return newqueens
            

            
            if(lcv_only):
                choices = [choice for choice in range(n) if not under_attack(choice, queens)] # get a list of cols not under attack
                choices = least_constraining_cols(choices, queens, n) # get back an ordered list by number of constraints each possible col causes
            else:
                choices = least_constraining_cols(queens_dict[len(queens)], queens,n) # same as above but w/ a limited consistent domain

                   
  
            for i in choices: # same as original provided code, but choices are limited and ordered
               
                if not under_attack(i,queens): 
                    num_assignments += 1
                    newqueens = rsolve(queens+[i],n)
                    if newqueens != []:
                        return newqueens
            return [] # FAIL
    return rsolve(queens, n)

def print_board(queens):
    row = 0
    n = len(queens)
    for pos in queens:
        for i in range(pos):
            sys.stdout.write( ". ")
        sys.stdout.write( "Q ")
        for i in range((n-pos)-1):
            sys.stdout.write( ". ")
        sys.stdout.write("\n")    
        print

ans = solve([],BOARD_SIZE)
print_board(ans)
