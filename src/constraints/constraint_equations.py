# helpers

from collections import Counter
from ..geometric_primitives.arc import Arc
from ..geometric_primitives.line import Line, distance_p2l
from ..geometric_primitives.point import Point, distance_p2p
from ..geometric_primitives.segment import Segment
from ..geometric_primitives.vector import Vector, cross, dot

def pairs(entities):
    return zip(entities[:-1], entities[1:])

def all_entities(entities, cls):
    return all(entity.__class__ is cls for entity in entities)

# constraints

def parallel(s1: Segment, s2: Segment):
    return [cross(s1.vector(), s2.vector())]

def perpendicular(s1: Segment, s2: Segment):
    return [dot(s1.vector(), s2.vector())]

def equal_length_or_radius(entity1, entity2):
    entities = (entity1, entity2)
    segments, arcs = all_entities(entities, Segment), all_entities(entities, Arc)
    assert segments or arcs
    return [entity1.length() - entity2.length()] if segments else [entity1.radius() - entity2.radius()]

def length(entity1, length_or_entity2, length_value=None):
    if isinstance(entity1, Segment) and isinstance(length_or_entity2, (int, float)):
        # Case 1: Segment with length value
        return [(Vector(entity1.p2.x - entity1.p1.x, entity1.p2.y - entity1.p1.y).length() - length_or_entity2)]
    elif isinstance(entity1, Point) and isinstance(length_or_entity2, Point) and isinstance(length_value, (int, float)):
        # Case 2: Two points with distance value
        return [(Vector(length_or_entity2.x - entity1.x, length_or_entity2.y - entity1.y).length() - length_value)]
    else:
        assert False, "Invalid arguments for length constraint"

def tangency(entity1, entity2):
    temp = Counter((entity1.__class__, entity2.__class__))
    if temp == Counter((Arc, Segment)):
        arc = entity1 if isinstance(entity1, Arc) else entity2
        segment = entity1 if isinstance(entity1, Segment) else entity2
        return [distance_p2l(arc.center(), Line(segment.p1, segment.p2)) - arc.radius()]
    elif temp == Counter((Arc, Arc)):
        return [distance_p2p(entity1.center(), entity2.center()) - (entity1.radius() + entity2.radius())]
    else:
        assert False

def concentricity(arc1: Arc, arc2: Arc):
    return [distance_p2p(arc1.center(), arc2.center())]