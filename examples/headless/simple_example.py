from src.geometric_primitives.point import Point
from src.geometric_primitives.segment import Segment
from src.geometric_primitives.arc import Arc
from src.constraints.constraint import Constraint
from src.constraints.constraints import CONSTRAINT_TYPE, Constraints
from src.geometry import Geometry
from src.solver.solver import Solver

# Step 1: Create geometry container
geometry = Geometry()

# Step 2: Create geometric primitives
# Example: Create a rectangle
geometry.segments = [
    Segment(Point(100, 100), Point(300, 100)),  # bottom edge
    Segment(Point(300, 100), Point(300, 200)),  # right edge
    Segment(Point(300, 200), Point(100, 200)),  # top edge
    Segment(Point(100, 200), Point(100, 100))  # left edge
]

# Step 3: Create constraints collection
constraints = Constraints()

# Step 4: Add constraints between primitives
# Example: Ensure rectangle corners are connected
constraints += [
    # Connect corners
    Constraint([geometry.segments[0].p2, geometry.segments[1].p1], CONSTRAINT_TYPE.COINCIDENCE),
    Constraint([geometry.segments[1].p2, geometry.segments[2].p1], CONSTRAINT_TYPE.COINCIDENCE),
    Constraint([geometry.segments[2].p2, geometry.segments[3].p1], CONSTRAINT_TYPE.COINCIDENCE),
    Constraint([geometry.segments[3].p2, geometry.segments[0].p1], CONSTRAINT_TYPE.COINCIDENCE),

    # Fix one point to prevent floating
    Constraint([geometry.segments[0].p1], CONSTRAINT_TYPE.FIXED)
]


# Step 5: Create solver with callback
def geometry_changed():
    pass  # Optional callback when geometry is updated


solver = Solver(geometry, geometry_changed, constraints)

# Step 6: Solve the constraints
solver.solve(None)

# Step 7: Access updated geometry
for segment in geometry.segments:
    print(f"Segment: ({segment.p1.x}, {segment.p1.y}) to ({segment.p2.x}, {segment.p2.y})")

# Example: Modify a point and resolve
geometry.segments[2].p1.x = 350
solver.solve(geometry.segments[2].p1)
print('...')
for segment in geometry.segments:
    print(f"Segment: ({segment.p1.x}, {segment.p1.y}) to ({segment.p2.x}, {segment.p2.y})")
