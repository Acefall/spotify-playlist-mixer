from itertools import count

class Serializer():
    def __init__(self):
        self.ids = count(0)
        self.objects = dict()

    def _getUniqueId(self):
        return next(self.ids)
    
    def serialize(self, object):

        if hasattr(object, "id"):
            print("Object has been serialized already")
            return {"id": object.id}

        object.id = self._getUniqueId()
        objectAsDict = dict()
        objectAsDict["id"] = object.id
        objectAsDict["type"] = object.__class__.__name__
        objectAsDict["data"] = object.serialize(self)

        self.objects[object.id] = objectAsDict

        return objectAsDict
    
    def getObjects(self):
        return self.objects
    
