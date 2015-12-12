"""
A simple structure to store the information about each groupee
"""
class GroupeeStruct:
    def __init__(self,name,fields):
        self.name=name
        self.fields = fields

    def __repr__(self):
        #return 'Groupee Object. Name: %s'%(self.name)+str(self.fields)
        return self.name
