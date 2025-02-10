from spotify_playlist_mixer.serializer import Serializer
from spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.setMinus import SetMinus
from spotify_playlist_mixer.source.takeN import TakeN
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.repeatN import RepeatN
from spotify_playlist_mixer.source.loop import Loop
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest


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
    

def test_complex_playlist_is_serialized_and_deserialized_correctly():
    recentlyPlayed = SpotifyPlaylistMock(["s1", "k1", "b1"])
    salsa = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"])
    bachata = SpotifyPlaylistMock(["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"])
    kizomba = SpotifyPlaylistMock(["k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8"])
    zouk = SpotifyPlaylistMock(["z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8"])

    freshSalsa = SetMinus(salsa, recentlyPlayed)
    freshBachata = SetMinus(bachata, recentlyPlayed)
    freshKizomba = SetMinus(kizomba, recentlyPlayed)
    freshZouk = SetMinus(zouk, recentlyPlayed)

    salsaPattern = TakeN(3, freshSalsa)
    bachataPattern = TakeN(3, freshBachata)
    kizombaPattern = TakeN(3, freshKizomba)
    zoukPattern = TakeN(2, freshZouk)

    sbk = Concatenate([salsaPattern, bachataPattern, kizombaPattern])
    sbk3 = RepeatN(3, sbk)
    sbkAndZouk = Concatenate([sbk3, zoukPattern])

    playlist = Loop(sbkAndZouk)

    serializer = Serializer()
    serialized = serializer.serialize(playlist)

    deserializer = Deserializer(serializer.getObjects())
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)
   
    for originalTrack, deserializedTrack in zip(playlist, deserialized):
        assert originalTrack == deserializedTrack

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)
