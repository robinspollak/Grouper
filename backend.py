from coding import *
from solver import *
def process(header,body):
    encode_dict,decode_dict = setupCoding(body)
    encoded = encode(body,encode_dict)
    decoded = decode(encoded,decode_dict)
    solutions = handleConstraints(header,body)
    if type(solutions) == str:
        return solutions
    if len(solutions)==0:
        return "There are no optimal groups for the given participants! Try disallowing participants from specifying a lot of people they dont want to work with"
    return_solutions = []
    for solution in solutions:
        groups = []
        for index in range(len(solution)):
            ret_string = ''
            ret_string+=("Group %d is "%(index+1))
            ret_string+=", ".join(list(map(lambda x: x.name,solution[index])))
            mutual_interests = intersectLists(list(map(lambda x:x.fields['Interests']\
            ,[groupee for groupee in solution[index] if 'Interests' in groupee.fields]\
            )))
            ret_string+=" and they have mutual interest in %s"%(", ".join(mutual_interests))
            if 'Positions' in header:
                ret_string+=". "+assignRoles(header['Positions'],solution[index])
            groups.append(ret_string)
        return_solutions.append('\n\n\n'.join(groups))
    return '\nAlternate Solution:\n'.join(return_solutions)

def intersectLists(lists):
    return list(set.intersection(*list(map(set,lists))))

def assignRoles(positions, groupees):
    if len(positions)>len(groupees):
        print(Warning("There are more positions than members of the group, some will be left unassigned"))
    elif len(positions)<len(groupees):
        print(Warning("There are more members of the group than positions, some members will not have a position"))
    role_dict = {}
    groupees_list = list(map(lambda x: x.name,groupees))
    assigned_dict = {}
    for position in positions:
        role_dict[position]=[] # ensure all roles are in dict, even if no one specified it
    for groupee in groupees:
        assigned_dict[groupee.name]=''
        if 'Positions' in groupee.fields:
            for position in groupee.fields['Positions']:
                if position in role_dict:
                    role_dict[position].append(groupee.name)
                else:
                    print(Warning('A participant specified interest in a position is not included in the header, this preference will be ignored.'))
    iter_keys = list(role_dict.keys())
    for key in iter_keys:
        if len(role_dict[key])>=1:
            groupee = role_dict[key][0]
            if groupee in groupees_list:
                assigned_dict[groupee]=key
                groupees_list.remove(groupee)
    remaining_roles = [role for role in iter_keys if role not in assigned_dict.values()]
    use_for_iterate = (remaining_roles if len(remaining_roles)<=len(groupees_list) else groupees_list)
    for index in range(len(use_for_iterate)):
        assigned_dict[groupees_list[index]]=remaining_roles[index]
    ret_string = ''
    for item in assigned_dict.items():
        ret_string+='%s has been assigned the role of %s, '%(item[0],item[1])
    return ret_string


