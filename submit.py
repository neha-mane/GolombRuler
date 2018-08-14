#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

import time
import copy
'''
global counterBT
counterBT = 0
global counterFC
counterFC = 0'''

#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    #Initializes domain, assignment and correct dictionary
    domain = [[1 for x in range(L + 1)] for x in range(M)]
    assignment = dict() #Dictionary to store all assignments
    correct = dict() #Dictionary to store consistent assignments at any point
    for i in range(M):
        assignment[i] = -1

    #Check if the assignment is consistent
    def check_consistent(initial_assignment):
        temp_assignment = copy.deepcopy(initial_assignment) #copy of dictionary to work on

        #Checks if the temp_assignment is in correct
        for key in temp_assignment.keys():
            if key in correct.keys() and temp_assignment[key] == correct[key]:
                return correct[temp_assignment[key]]

        #Calculates distances between the two values and check if they are unique and consistent with the solution
        distances = []
        for i in range(M):
            for j in range(M - 1 - i):
                x = temp_assignment[M - 1 - i]
                y = temp_assignment[(M - 1 - i) - (j + 1)]
                if x == -1 or y == -1:
                    continue
                else:
                    distances.append(x-y)
        distances.sort()
        temp = -1
        for i in range(len(distances)):
            if distances[i] == temp:
                correct[tuple(temp_assignment.items())] = False
                return False
            temp = distances[i]

        #Assigns false correctness to values that don't follow constraints
        for i in range(1, len(temp_assignment)):
            if temp_assignment[i] == -1 or temp_assignment[i - 1] == -1:
                continue
            if not (temp_assignment[i] > temp_assignment[i - 1]):
                correct[tuple(temp_assignment.items())] = False
                return False

        #If not returned as false from above assigns true and returns True
        correct[tuple(temp_assignment.items())] = True
        return True

    #the main backtrack function
    def backtrack(assignment):
        if not(-1 in assignment.values()) and check_consistent(assignment):
            return assignment
        var = 0
        #Gets possible values from the domain for the first unassigned variable
        for i in range(M):
            if assignment[i] == -1:
                var = i
                break
        possible_values = list()
        for i in range(len(domain[var])):
            if domain[var][i] != 0:
                possible_values.append(i)

        for value in possible_values:
            #global counterBT
            #counterBT += 1
            #Checks if the assignment is consistent and only then assigns the value and check for further partial assignments
            if check_consistent(assignment):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not False:
                    return result
                #Reassign value to -1
                assignment[var] = -1
        return False

    answer = backtrack(assignment)
    if answer:
        return L, answer.values()#, counterBT
    else:
        return -1, []

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    # Initializes domain, assignment and correct dictionary
    domain = [[1 for x in range(L + 1)] for x in range(M)]
    assignment = dict()  # Dictionary to store all assignments
    correct = dict()  # Dictionary to store consistent assignments at any point
    for i in range(M):
        assignment[i] = -1

    # Check if the assignment is consistent
    def check_consistent(initial_assignment):
        temp_assignment = copy.deepcopy(initial_assignment)  # copy of dictionary to work on

        # Checks if the temp_assignment is in correct
        for key in temp_assignment.keys():
            if key in correct.keys() and temp_assignment[key] == correct[key]:
                return correct[temp_assignment[key]]

        # Calculates distances between the two values and check if they are unique and consistent with the solution
        distances = []
        for i in range(M):
            for j in range(M - 1 - i):
                x = temp_assignment[M - 1 - i]
                y = temp_assignment[(M - 1 - i) - (j + 1)]
                if x == -1 or y == -1:
                    continue
                else:
                    distances.append(x - y)
        distances.sort()
        temp = -1
        for i in range(len(distances)):
            if distances[i] == temp:
                correct[tuple(temp_assignment.items())] = False
                return False
            temp = distances[i]

        # Assigns false correctness to values that don't follow constraints
        for i in range(1, len(temp_assignment)):
            if temp_assignment[i] == -1 or temp_assignment[i - 1] == -1:
                continue
            if not (temp_assignment[i] > temp_assignment[i - 1]):
                correct[tuple(temp_assignment.items())] = False
                return False

        # If not returned as false from above assigns true and returns True
        correct[tuple(temp_assignment.items())] = True
        return True

    def BtFc(domain, assignment):
        if not(-1 in assignment.values()) and check_consistent(assignment):
            return assignment
        var = 0
        #Gets unassigned variable
        for i in range(M):
            if assignment[i] == -1:
                var = i
                break
        #Check the possible values from the domain for the unassigned variable
        possible_val = list()
        for i in range(len(domain[var])):
            if domain[var][i] != 0:
                possible_val.append(i)
        #For every such possible value check if it fulfils the criteria and then assign it
        for value in possible_val:
            #global counterFC
            #counterFC += 1
            if check_consistent(assignment):
                #counterFC += 1
                assignment[var] = value
                #Copies the domain for future reference if it fails, domain needs to be reverted back
                newdomain = copy.deepcopy(domain)
                #This set will store the what we will infer from the domain values of a particular variable
                inferenced_set = set()
                for i in range(len(domain)):
                    if i == var or assignment[i] != -1:
                        continue
                    for j in range(len(domain[i])):
                        if domain[i][j] == 0:
                            continue
                        if not(check_consistent(assignment)):
                            domain[i][j] = 0
                    if domain[i].count(1) == 0:
                        break
                    elif domain[i].count(1) == 1:
                        inferenced_set.add((i, domain[i].index(1))) #Adds all such inferred values
                #For the inferred values store them in assignment
                for val in inferenced_set:
                    assignment[val[0]] = val[1]
                #counterFC += 1
                #call the forward checking function
                result = BtFc(domain, assignment)
                if result is not False:
                    #counterFC += 1
                    return result
                #Reassign value to -1 and change the domain back
                assignment[var] = -1
                domain = copy.deepcopy(newdomain)
                for val in inferenced_set:
                    assignment[val[0]] = -1
        return False

    answer = BtFc(domain, assignment)
    if answer:
        return L, answer.values()#,counterFC
    return -1, []



#Trial call to BT
L, M = 6, 4
#L, M = 7, 4
#L, M = 11, 5
#L, M = 20, 6
#L, M = 25, 7
#L, M = 34, 8
#L, M = 17, 6
ret = BT(L, M)
prevret = ret
temp = ret
L = L - 1

#If ruler exists, finds the optimal L for that M
while temp[0] > 1:
    temp = BT(L, M)
    if temp[0] == -1:
        ret = prevret
        break
    else:
        prevret = temp
        L = L - 1
print "Backtracking - ", ret

#Trial call for FC
L, M = 6, 4
#L, M = 7, 4
#L, M = 11, 5
#L, M = 20, 6
#L, M = 25, 7
#L, M = 34, 8
#L, M = 17, 6
ret = FC(L, M)
prevret = ret
temp = ret
L = L - 1

#If ruler exists, finds the optimal L for that M
while temp[0] > 1:
    temp = FC(L, M)
    if temp[0] == -1:
        ret = prevret
        break
    else:
        prevret = temp
        L = L - 1
print "Forward Checking - ", ret

#Bonus: backtracking + constraint propagation
#def CP(L, M):
    #"*** YOUR CODE HERE ***"
    #return -1,[]

