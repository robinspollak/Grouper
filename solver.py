from constraint import *
from coding import *
#
#add a variable for each groupee and then make the allowed values range(len(groupees))
#then make compare take in the number of people and the groupsize as an argument
#TO LIMIT DONTWANTTO, WANTTO
#and say that groupee a and groupee b cannot be in the same group by making group 1: 0,1,2 group 2: 3,4,5 groupe 3:6,7,8 etc
#then add a constraint for each com
#


def handleConstraints(header,body):
    encode_dict,decode_dict = setupCoding(body)
    prob = Problem()
    groupee_dict = {}
    for groupee in body:
        groupee_dict[groupee.name]=groupee
        prob.addVariable(groupee.name,list(range(int(header['GroupSize']))))
    prob.addConstraint(AllDifferentConstraint())
    for groupee in body:
        constrainFromGivens(groupee)

def constrainFromGivens(groupee):
    print("hi")

def selectFor(groupee1,groupee2,num_participants,groupsize):
    for jumping_index in range(num_participants/groupsize): # for each group
        print(jumping_index * groupsize)

def selectAgainst(groupee):
    return "hi"


#problem.addVariable("a",[1,2,3])
#problem.addVariable("b",[1,2,3])


#part two gather information about problem to decide how big the groups are, either pass as arguments or rearrange imports?
#need group size, length of list of names


#problem.addConstrint(lambda a,b: a!=b, [a,b])
