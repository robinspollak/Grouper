from constraint import *
from coding import *
import signal
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
def handler(signum,frame):
    raise Exception("Tried to get solutions but timed out. Please be patient while the program continues!")
signal.signal(signal.SIGALRM, handler)
def handleConstraints(header,body):
    global participants,num_participants,interests,group_size,encode_dict,decode_dict,groupee_dict
    participants = header['Names']
    num_participants = len(header['Names'])
    group_size = int(header['GroupSize'])
    encode_dict,decode_dict = setupCoding(body)
    prob = Problem()
    interests = header['Interests']
    groupee_dict = {}
    for groupee in body:
        groupee_dict[groupee.name]=groupee
        prob.addVariable(groupee.name,range(num_participants))
    prob.addConstraint(AllDifferentConstraint())
    for groupee in body:
#        print("basic constraining %s"%(groupee.name))
        basicConstrain(prob,groupee)
    basic_constrained = getSolutions(prob)
    if type(basic_constrained)==list:
        return basic_constrained
    for groupee in body:
#        print("medium constraining %s"%(groupee.name))
        mediumConstrain(prob,groupee)
    medium_constrained = getSolutions(prob)
    if type(medium_constrained)==list:
        return medium_constrained
    for groupee in body:
#        print("high constraining %s"%(groupee.name))
        strictConstrain(prob,groupee)
    strict_constrained = getSolutions(prob)
    if type(strict_constrained)==list:
        return strict_constrained
    else:
        return "Not enough information to generate groups, too many possible options. Please add additional information!"


def listIntersect(list1,list2):
    return len(list(set(list1).intersection(set(list2))))

def getSolutions(prob):
    signal.alarm(15)
    try:
        base_solutions = prob.getSolutions()
        signal.alarm(0)
        solutions= uniquify(base_solutions)
        if len(solutions)>10:
            return -1
        return solutions
    except Exception as e:
        print(e)
        return(e)
def basicConstrain(prob,groupee):
    if 'DontWantToWorkWith' in groupee.fields:
        for groupee2 in groupee.fields['DontWantToWorkWith']:
            if groupee.name==groupee2:
                continue
            prob.addConstraint(notInSameGroup,(groupee.name,groupee2))
    for groupee2 in groupee_dict.values():
        if groupee==groupee2:
            continue
        if ('Interests' in groupee.fields and 'Interests' in groupee2.fields):
            interest_overlap = listIntersect(groupee.fields['Interests'],groupee2.fields['Interests'])
            if interest_overlap == 0:
                prob.addConstraint(notInSameGroup,(groupee.name,groupee2.name))
def mediumConstrain(prob,groupee):
    if 'WantToWorkWith' in groupee.fields:
        wantto = groupee.fields['WantToWorkWith'][0]
        prob.addConstraint(inSameGroup,(groupee.name,groupee.fields['WantToWorkWith'][0]))
    for groupee2 in groupee_dict.values():
        if groupee == groupee2:
            continue
        if ('Interests' in groupee.fields and 'Interests' in groupee2.fields):
            interest_overlap = listIntersect(groupee.fields['Interests'],groupee2.fields['Interests'])
            if interest_overlap>(len(interests)/2):
                prob.addConstraint(inSameGroup,(groupee.name,groupee2.name))

def strictConstrain(prob,groupee):
    if 'Position' in groupee.fields:
        for groupee2 in groupee_dict.values():
            if groupee==groupee2:
                continue
            if 'Position' in groupee2.fields:
                position_overlap = listIntersect(groupee.fields['Positions'],groupee2.fields['Positions'])
                if position_overlap>0:
                    prob.addConstraint(notInSameGroup,groupee.name,groupee.name)
    if 'WantToWorkWith' in groupee.fields:
        prob.addConstraint(inSameGroup,(groupee.name,groupee.fields['WantToWorkWith'][-1]))

def inSameGroup(a,b):
    for jumping_index in range(num_participants//group_size):
        lower = jumping_index*group_size
        upper = jumping_index*group_size + group_size
        if ( a>= lower and b>= lower and a < upper and b < upper):
            return True
        else:
            continue
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
    superfinalsolutions = [finalsolutions[0]]
    for solution in finalsolutions:
        for group in solution:
            if group not in superfinalsolutions[0]:
                superfinalsolutions.append(solution)
                break
    return superfinalsolutions
