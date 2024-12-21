from spotify_playlist_mixer.serializer import Serializer

class LeafNode:
    def __init__(self):
        self.serializeCalls = 0

    def serialize(self, serializer):
        self.serializeCalls += 1
        return {
            "attribute": "value",
        }
    
def test_serialize_results_in_filled_dictionary():
    serializer = Serializer()
    object = LeafNode()

    assert object.serializeCalls == 0

    serialized = serializer.serialize(object)

    assert object.serializeCalls == 1

    assert len(serialized) == 3

    assert "id" in serialized
    assert "type" in serialized
    assert serialized["type"] == "LeafNode"
    assert "data" in serialized
    assert "attribute" in serialized["data"]

def test_second_serialize_results_in_reference_by_id():
    serializer = Serializer()
    object = LeafNode()

    assert object.serializeCalls == 0
    serialized = serializer.serialize(object)
    assert object.serializeCalls == 1
    serialized = serializer.serialize(object)
    assert object.serializeCalls == 1

    assert len(serialized) == 1
    assert "id" in serialized
    assert serialized["id"] == object.id

class InternalNode:
    def __init__(self, child):
        self.serializeCalls = 0
        self.child = child

    def serialize(self, serializer):
        self.serializeCalls += 1
        return {
            "child": serializer.serialize(self.child)
        }

def test_cyclic_dependency_is_resolved():
    serializer = Serializer()
    node1 = InternalNode(None)
    node2 = InternalNode(node1)
    node1.child = node2

    serializedNode1 = serializer.serialize(node1)

    assert "type" in serializedNode1
    assert "data" in serializedNode1
    assert "child" in serializedNode1["data"]

    serializedNode2 = serializedNode1["data"]["child"]
    assert "type" in serializedNode2
    assert "data" in serializedNode2
    assert "child" in serializedNode2["data"]
    
    # Test that the refernece of node2 to node1 is only by an id
    serializedNode1Ref = serializedNode2["data"]["child"]
    assert len(serializedNode1Ref) == 1
    assert "id" in serializedNode1Ref


def test_cyclic_dependency_results_in_two_serialized_objects():
    serializer = Serializer()
    node1 = InternalNode(None)
    node2 = InternalNode(node1)
    node1.child = node2

    serializer.serialize(node1)
    assert len(serializer.objects) == 2

    assert 0 in serializer.objects
    assert "type" in serializer.objects[0]
    assert "data" in serializer.objects[0]
    assert "child" in serializer.objects[0]["data"]

    assert 1 in serializer.objects
    assert "type" in serializer.objects[1]
    assert "data" in serializer.objects[1]
    assert "child" in serializer.objects[0]["data"]
    

