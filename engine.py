import fileinput
from intake_functions import *
from parser import *
from backend import *

input_string = ""
for line in fileinput.input():
	input_string+=line #first read in the file

program = parse(prepass(input_string),Program) #do the prepass
header = intake_header(program[0])
body = intake_body(program[1])
valid = validate(header,body) #do a pre-run check that the program is valid
if (type(valid)==bool):
    print(process(header,body))

else:
    print(valid)


