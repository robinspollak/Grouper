from solver import *


"""
This function passes off data to the constraint solver and then handles the results. It checks for corner cases and formats the response string
which is then passed back to the engine to be returned to the user.
"""
def process(header,body):
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
                ret_string+=". "+(assignRoles(header['Positions'],solution[index])[:-2])
            groups.append(ret_string)
        return_solutions.append('\n\n\n'.join(groups))
    return '\nAlternate Solution:\n'.join(return_solutions)
"""
This function gets the entries shared by two lists, only including each entry once
"""
def intersectLists(lists):
    return list(set.intersection(*list(map(set,lists))))
"""
This function assigns roles/positions to people given a group. It passes an addition to the
return string to the process function
"""
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
        ret_string+='%s has been assigned the role of %s, '%(item[0],(item[1] if item[1]!='' else 'none'))
    return ret_string


