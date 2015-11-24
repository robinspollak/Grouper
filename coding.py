from groupee import *
def setupCoding(groupeelist):
    count = 0
    encode = {}
    decode = {}
    for groupee in groupeelist:
        encode[groupee.name] = count
        decode[count]=groupee
        count+=1
    return encode,decode

def encode(arg,encoder):
    if (type(arg)==GroupeeStruct):
        if arg.name in encoder:
            return encoder[arg.name]
        else:
            return Exception("you've tried to encode a groupee which was not included in the setup")
    elif (type(arg)==list):
        return list(map(lambda x: encode(x,encoder),arg))
    else:
        return Exception("Can only encode a groupee or list of groupees")

def decode(arg,decoder):
    if (type(arg)==int):
        if arg in decoder:
            return decoder[arg]
        else:
            return Exception("you've tried to decode a groupee which was not included in the setup")
    elif (type(arg)==list):
        return list(map(lambda x: decode(x,decoder),arg))
    else:
        return Exception("Can only decode an int or a list of ints")
