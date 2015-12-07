from coding import *
from solver import *
def process(header,body):
    encode_dict,decode_dict = setupCoding(body)
    encoded = encode(body,encode_dict)
    decoded = decode(encoded,decode_dict)
    solutions = handleConstraints(header,body)
    if len(solutions)==0:
        return "There are no optimal groups for the given participants! Try disallowing participants from specifying a lot of people they dont want to work with"
    return_solutions = []
    for solution in solutions:
        groups = []
        for index in range(len(solution)):
            ret_string = ''
            ret_string+=("Group %d is "%(index))
            ret_string+=",".join(list(map(lambda x: x.name,solution[index])))
            mutual_interests = intersectLists(list(map(lambda x:x.fields['Interests']\
            ,[groupee for groupee in solution[index] if 'Interests' in groupee.fields]\
            )))
            ret_string+=" and they have mutual interests %s"%(",".join(mutual_interests))
            groups.append(ret_string)
        return_solutions.append('\n'.join(groups))
    return '\nAlternate Solution:\n'.join(return_solutions)

def intersectLists(lists):
    return list(set.intersection(*list(map(set,lists))))

