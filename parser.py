from pypeg2 import *

class GroupeeHeader(str): # The header that declares a groupee
	grammar = "Groupee",word,":",';'

class FieldData(List): #The data that follows a field, such as in the header
	grammar = word, maybe_some(',',word)

class Field(List): #The whole field, including the name and the data
	grammar = name(),":",attr('data',FieldData),';'

class Fields(List): #multiple fields as above
	grammar = '~',Field,maybe_some('~',Field)

class GroupeeFields(List): #different because there are two tab characters
	grammar = '~~',Field,maybe_some('~~',Field)

class Groupee(List): #the whole groupee
	grammar = attr('name',GroupeeHeader),attr('fields',GroupeeFields)

class Groupees(List): #multiple groupees!
	grammar = "~",Groupee,maybe_some('~',Groupee)

class Body(List): #all the groupees
	grammar = "Body:",';',attr('groupees',Groupees),";"

class Header(List): #all the header
	grammar = "Header:",';',attr('fields',Fields),";"

class Program(List): #the whole shebang
	grammar = Header,Body










