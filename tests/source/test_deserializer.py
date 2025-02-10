from spotify_playlist_mixer.deserializer import Deserializer
from spotify_playlist_mixer.serializer import Serializer

class LeafNode:
    deserializeCalls = 0

    def serialize(self, serializer):
        return {
            "attribute": "value",
        }

    @classmethod
    def deserialize(cls, data, deserializer):
        cls.deserializeCalls += 1
        return cls()

Deserializer.class_map["LeafNode"] = LeafNode

def test_object_is_only_deserialized_once():
    serializer = Serializer()
    leafNode = LeafNode()
    serializedNode = serializer.serialize(leafNode)

    deserializer = Deserializer(serializer.objects)
    assert LeafNode.deserializeCalls == 0
    deserializer.deserialize(serializedNode)
    assert LeafNode.deserializeCalls == 1
    deserializer.deserialize(serializedNode)
    assert LeafNode.deserializeCalls == 1
    
def test_object_is_provided_from_already_deserialized_objects_as_reference():
    serializer = Serializer()
    leafNode = LeafNode()
    serializedNode = serializer.serialize(leafNode)

    deserializer = Deserializer()
    deserializedNode = deserializer.deserialize(serializedNode)
    deserializedNode.magicAttribute = "MagicValue"

    deserializedNodeAgain = deserializer.deserialize({"id": serializedNode["id"]})
    assert hasattr(deserializedNodeAgain, "magicAttribute")
    assert deserializedNodeAgain.magicAttribute == "MagicValue"