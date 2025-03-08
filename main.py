import tkinter as tk
from src.constraints.constraints import Constraints
from src.geometry import Geometry
from src.gui.gui import GUI
from src.solver.solver import Solver

def geometry_changed_by_GUI(active_point):
    global solver
    solver.solve(active_point)

def constraints_changed_by_GUI():
    global solver
    solver.solve(None)

def geometry_changed_by_solver():
    global gui
    global solver
    gui.degrees_of_freedom = solver.degrees_of_freedom
    gui.redraw_geometry()

geometry = Geometry()
constraints = Constraints()

solver = Solver(geometry, geometry_changed_by_solver, constraints)

root_widget = tk.Tk()
root_widget.title('2D Geometric Constraint Solver')

gui = GUI(root_widget, geometry, geometry_changed_by_GUI, constraints, constraints_changed_by_GUI)
gui.pack(fill="both", expand=True)

root_widget.mainloop()