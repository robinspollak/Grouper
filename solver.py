from constraint import *
from coding import *
#add a variable for each groupee and then make the allowed values range(len(groupees))
#then make compare take in the number of people and the groupsize as an argument
#TO LIMIT DONTWANTTO, WANTTO
#and say that groupee a and groupee b cannot be in the same group by making group 1: 0,1,2 group 2: 3,4,5 groupe 3:6,7,8 etc
#then add a constraint for each com
#

participants = []
num_participants = 0
group_size = 0
encode_dict = {}
decode_dict = {}
groupee_dict = {}
def handleConstraints(header,body):
    global participants,num_participants,group_size,encode_dict,decode_dict,groupee_dict
    participants = header['Names']
    num_participants = len(header['Names'])
    group_size = int(header['GroupSize'])
    encode_dict,decode_dict = setupCoding(body)
    prob = Problem()
    groupee_dict = {}
    for groupee in body:
        groupee_dict[groupee.name]=groupee
        prob.addVariable(groupee.name,range(len(header['Names'])))
    prob.addConstraint(AllDifferentConstraint())
    for groupee in body:
        basicConstrain(prob,groupee)
    return uniquify(prob.getSolutions())

def listIntersect(list1,list2):
    return len(list(set(list1).intersection(set(list2))))

def basicConstrain(prob,groupee):
    if 'DontWantToWorkWith' in groupee.fields:
        for groupee2 in groupee.fields['DontWantToWorkWith']:
            prob.addConstraint(notInSameGroup,(groupee.name,groupee2))
    for groupee2 in groupee_dict.values():
        if ('Interests' in groupee.fields and 'Interests' in groupee2.fields):
            interest_overlap = listIntersect(groupee.fields['Interests'],groupee2.fields['Interests'])
            if interest_overlap == 0:
                prob.addConstraint(notInSameGroup,(groupee.name,groupee2.name))

def inSameGroup(a,b):
    for jumping_index in range(num_participants//group_size):
        lower = jumping_index*group_size
        upper = jumping_index*group_size + group_size
        if ( a>= lower and b>= lower and a < upper and b < upper):
            return True
        else:
            return False
def notInSameGroup(a,b):
    return not inSameGroup(a,b)

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def uniquify(solutions):
    solutions = list(map(lambda x: list(x.items()),solutions))
    newsolutions = []
    for solution in solutions:
        solution.sort(key=lambda x: x[1])
        newsolutions.append(chunks(solution,group_size))
    solutions = []
    for solution in newsolutions:
        newsolution = []
        for group in solution:
            group.sort()
            newsolution.append(list((map(lambda x:groupee_dict[x[0]],group))))
        solutions.append(newsolution)
    finalsolutions = []
    for solution in solutions:
        if solution not in finalsolutions:
            finalsolutions.append(solution)
    return finalsolutions



#part two gather information about problem to decide how big the groups are, either pass as arguments or rearrange imports?
#need group size, length of list of names


#problem.addConstrint(lambda a,b: a!=b, [a,b])
