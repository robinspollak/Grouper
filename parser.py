from pypeg2 import *

class GroupeeHeader(str):
	grammar = "Groupee",word,":",';'

class FieldData(List):
	grammar = word, maybe_some(',',word)

class Field(List):
	grammar = name(),":",attr('data',FieldData),';'

class Fields(List):
	grammar = '~',Field,maybe_some('~',Field)

class GroupeeFields(List):
	grammar = '~~',Field,maybe_some('~~',Field)

class Groupee(List):
	grammar = attr('name',GroupeeHeader),attr('fields',GroupeeFields)

class Groupees(List):
	grammar = "~",Groupee,maybe_some('~',Groupee)

class Body(List):
	grammar = "Body:",';',attr('groupees',Groupees),";"

class Header(List):
	grammar = "Header:",';',attr('fields',Fields),";"

class Program(List):
	grammar = Header,Body










