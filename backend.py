from coding import *
from solver import *
def process(header,body):
    encode_dict,decode_dict = setupCoding(body)
    encoded = encode(body,encode_dict)
    decoded = decode(encoded,decode_dict)
    #print(list(map(lambda x:x.name,body)),encoded,decoded)
    handleConstraints(header,body)

