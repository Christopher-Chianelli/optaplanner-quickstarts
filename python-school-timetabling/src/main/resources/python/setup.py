import java

PythonWrapperGenerator = java.type("org.acme.schooltimetabling.gizmo.PythonWrapperGenerator")
def getOptaPlannerAnnotations(pythonClass):
    method_list = [attribute for attribute in dir(pythonClass) if callable(getattr(pythonClass, attribute)) and attribute.startswith('__') is False]
    annotated_methods = []
    for method in method_list:
        optaplanner_annotations = [attribute for attribute in dir(getattr(pythonClass, method)) if attribute.startswith('__optaplanner')]
        if optaplanner_annotations:
            returnType = getattr(pythonClass, method).__annotations__.get("return")
            if returnType is None:
                returnType = getattr(getattr(pythonClass, method), "__return", None)
            if not isinstance(returnType, type(PythonWrapperGenerator)):
                returnType = None
            annotated_methods = annotated_methods + [((method, returnType, list(map(lambda annotation: getattr(getattr(pythonClass, method), annotation), optaplanner_annotations))))]
    return annotated_methods

def wrap(javaClass, pythonObject):
    return PythonWrapperGenerator.wrap(javaClass, pythonObject)

def generateProblemFactClass(pythonClass):
    optaplannerAnnotations = getOptaPlannerAnnotations(pythonClass)
    return PythonWrapperGenerator.defineProblemFactClass(pythonClass.__name__, optaplannerAnnotations)

def generatePlanningEntityClass(pythonClass):
    optaplannerAnnotations = getOptaPlannerAnnotations(pythonClass)
    return PythonWrapperGenerator.definePlanningEntityClass(pythonClass.__name__, optaplannerAnnotations)

def generatePlanningSolutionClass(pythonClass):
    optaplannerAnnotations = getOptaPlannerAnnotations(pythonClass)
    return PythonWrapperGenerator.definePlanningSolutionClass(pythonClass.__name__, optaplannerAnnotations)

def generateConstraintProviderClass(constraintProvider):
    return PythonWrapperGenerator.defineConstraintProviderClass(constraintProvider.__name__, constraintProvider)