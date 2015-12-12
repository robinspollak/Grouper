from groupee import *

"""
A function that replaces new line and tab characters with characters readable by the parser. Also strips white spaces.
"""
def prepass(string):
    chars = repr(string)
    return_string = ''
    for index in range(1,len(repr(string))-1):
        if chars[index]=='\\':
            special_char = chars[index:index+2]
            if special_char == '\\n':
                return_string+=';'
            if special_char == '\\t':
                return_string+='~'
        try:
            if chars[index-1]=='\\':
                continue
        except:
            pass
        else:
            if chars[index]!='\\':
                return_string+=chars[index]
    return_string+=';'
    return return_string.replace(" ","")

"""
Reads the header into a dictionary and changes the data types of some data
"""
def intake_header(rawdata):
	header_fields = {}
	for field in rawdata.fields:
		try:
			data = int(field.data[0])
		except:
			data = list(field.data)
		header_fields[str(field.name)] = data
	return header_fields

"""
Reads the parsed body and creates a groupeestruct for each groupee and returns a list of them
"""
def intake_body(rawdata):
	groupees = []
	for groupee in rawdata.groupees:
		fields_dict = {}
		for field in groupee.fields:
			try:
				data = int(field.data[0])
			except:
				data = list(map(lambda x:str(x),list(field.data)))
			fields_dict[str(field.name)] = data
		groupees.append(GroupeeStruct(str(groupee.name),fields_dict))
	return groupees

"""
Checks for some stuff that will make Grouper break that I can discern before the program runs
"""
def validate(header,body):
	if 'Names' not in header:
		return Exception("Grouper Syntax Error: please include a list of names to be grouped in your header")
	body_names = list(map(lambda x:x.name,body))
	for name in header['Names']:
		if name not in body_names:
			print(("Warning: %s does not have a Groupee entry and will not be grouped"%(name)))
	if 'GroupSize' not in header:
		return Exception("Grouper Syntax Error: please state the size of groups you wish you be generated in your header")
	for groupee in body:
		if groupee.name not in header['Names']:
			return Exception(("Grouper Logic Error: Person named %s has a groupee entry but is not included in your list of names")\
				%(groupee.name))
		for field_name in groupee.fields:
			if field_name == 'WantToWorkWith' or field_name=='DontWantToWorkWith':
				for item in groupee.fields[field_name]:
					if item not in header['Names']:
						return Exception(('Grouper Logic Error: %s specified %s in their %s field, but %s is not included in header')\
							%(groupee.name,item,field_name,item))
				continue
			if field_name not in header:
				return Exception(("Grouper Logic Error: Field named %s is included in a groupee entry but omitted from the header")\
		 			%(field_name))
			for item in groupee.fields[field_name]:
				if item not in header[field_name]:
					return Exception(("Grouper Logic Error: Field named %s includes value %s for groupee %s, but %s is not included in the header")\
		 			%(field_name,item,groupee.name,item))
	return True
