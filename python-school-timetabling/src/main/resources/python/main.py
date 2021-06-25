import java
from setup import wrap, generatePlanningSolutionClass, generatePlanningEntityClass, generateConstraintProviderClass
from constraints import defineConstraints
from domain import TimeTable, Lesson, generateProblem

PythonConstraintProvider = generateConstraintProviderClass(defineConstraints)

SolverConfig = java.type("org.optaplanner.core.config.solver.SolverConfig")
PythonSolver = java.type("org.acme.schooltimetabling.gizmo.PythonSolver")
Duration = java.type("java.time.Duration")

TimeTableClass = generatePlanningSolutionClass(TimeTable)
LessonClass = generatePlanningEntityClass(Lesson)
solverConfig = SolverConfig().withEntityClasses(LessonClass) \
    .withSolutionClass(TimeTableClass) \
    .withConstraintProviderClass(PythonConstraintProvider) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solution = PythonSolver.solve(solverConfig, generateProblem())

print(solution)