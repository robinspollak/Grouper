import fileinput
from intake_functions import *
from parser import *
from backend import *

input_string = ""
for line in fileinput.input():
	input_string+=line

program = parse(prepass(input_string),Program)
header = intake_header(program[0])
body = intake_body(program[1])
valid = validate(header,body)
if (type(valid)==bool):
    print(process(header,body))

else:
    print(valid)


