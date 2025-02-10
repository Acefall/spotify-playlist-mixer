from itertools import count

class Serializer():
    def __init__(self):
        self.ids = count(0)
        self.objects = dict()

    def _getUniqueId(self):
        return next(self.ids)
    
    def serialize(self, object):
        
        if id(object) in self.objects:
            print("Object has been serialized already")
            return {"id": id(object)}
        
        self.objects[id(object)] = "I have seen this id."

        objectAsDict = dict()
        objectAsDict["id"] = id(object)
        objectAsDict["type"] = object.__class__.__name__
        objectAsDict["data"] = object.serialize(self)

        self.objects[id(object)] = objectAsDict

        return objectAsDict
    
    def getObjects(self):
        return self.objects
    
