import sqlite3
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

def beginSolverProcess():
    print("Starting solver process...")
    solver = pywraplp.Solver.CreateSolver(("GLOP"))
    
