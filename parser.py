from pypeg2 import *
import fileinput
from groupee import *

input_string = ""
for line in fileinput.input():
	input_string+=line
print(input_string)

class GroupeeHeader(str):
	grammar = "Groupee ",word,":"

class FieldData(List):
	grammar = word, maybe_some(',',word)

class Field(List):
	grammar = name(),":",attr('data',FieldData)

class Fields(List):
	grammar = "+",Field,maybe_some('+',Field)

class Groupee(List):
	grammar = attr('name',GroupeeHeader),attr('fields',Fields)

class Groupees(List):
	grammar = "-",Groupee,maybe_some('-',Groupee)

class Body(List):
	grammar = "Body","{",attr('groupees',Groupees),"}"

class Header(List):
	grammar = "Header","{",attr('fields',Fields),"}"

class Program(List):
	grammar = Header,Body

program = parse(input_string,Program)

header_fields = {}
groupees = []

for field in program[0].fields:
	try:
		data = int(field.data[0])
	except:
		data = list(field.data)
	header_fields[str(field.name)] = data

for groupee in program[1].groupees:
	fields_dict = {}
	for field in groupee.fields:
		try:
			data = int(field.data[0])
		except:
			data = list(field.data)
		fields_dict[str(field.name)] = data
	groupees.append(GroupeeStruct(groupee.name,fields_dict))

print(groupees)


