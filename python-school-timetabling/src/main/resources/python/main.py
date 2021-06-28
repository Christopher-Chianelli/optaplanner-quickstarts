import java
from setup import getClass
from constraints import defineConstraints
from domain import TimeTable, Lesson, generateProblem

SolverConfig = java.type("org.optaplanner.core.config.solver.SolverConfig")
PythonSolver = java.type("org.acme.schooltimetabling.gizmo.PythonSolver")
Duration = java.type("java.time.Duration")

solverConfig = SolverConfig().withEntityClasses(getClass(Lesson)) \
    .withSolutionClass(getClass(TimeTable)) \
    .withConstraintProviderClass(getClass(defineConstraints)) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solution = PythonSolver.solve(solverConfig, generateProblem())

print(solution)