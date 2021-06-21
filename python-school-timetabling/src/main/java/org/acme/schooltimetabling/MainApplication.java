package org.acme.schooltimetabling;

import org.acme.schooltimetabling.bootstrap.DemoDataGenerator;
import org.acme.schooltimetabling.domain.Lesson;
import org.acme.schooltimetabling.domain.TimeTable;
import org.acme.schooltimetabling.solver.TimeTableConstraintProvider;
import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Source;
import org.graalvm.polyglot.Value;
import org.optaplanner.core.api.score.stream.Constraint;
import org.optaplanner.core.api.score.stream.ConstraintFactory;
import org.optaplanner.core.api.score.stream.ConstraintProvider;
import org.optaplanner.core.api.solver.Solver;
import org.optaplanner.core.api.solver.SolverFactory;
import org.optaplanner.core.config.score.director.ScoreDirectorFactoryConfig;
import org.optaplanner.core.config.solver.EnvironmentMode;
import org.optaplanner.core.config.solver.SolverConfig;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.time.Duration;

public class MainApplication {

    private static String PYTHON = "python";
    private static String VENV_EXECUTABLE = MainApplication.class.getClassLoader().getResource("venv/bin/python").getPath();
    private static String SOURCE_FILE_NAME = "constraints.py";

    public static class PythonConstraintProvider implements ConstraintProvider {

        @Override public Constraint[] defineConstraints(ConstraintFactory constraintFactory) {
            return getPythonObjects().getMember("TimeTableConstraintProvider").execute(constraintFactory).as(Constraint[].class);
        }
    }

    public static void main(String[] args) throws Exception {
        Value pythonObjects = getPythonObjects();

        SolverConfig solverConfig = new SolverConfig();
        solverConfig.withEntityClasses(Lesson.class)
                .withSolutionClass(TimeTable.class)
                .withConstraintProviderClass(PythonConstraintProvider.class)
                // .withEnvironmentMode(EnvironmentMode.FULL_ASSERT)
                .withTerminationSpentLimit(Duration.ofSeconds(30));

        //solverConfig.getScoreDirectorFactoryConfig().withAssertionScoreDirectorFactory(
        //        new ScoreDirectorFactoryConfig().withConstraintProviderClass(TimeTableConstraintProvider.class)
        //);

        Solver<TimeTable> solver = SolverFactory.<TimeTable>create(solverConfig).buildSolver();
        TimeTable solution = solver.solve(DemoDataGenerator.generateDemoData());
        System.out.println(solution);
    }

    public static Value getPythonObjects() {
        Context context = Context.newBuilder(PYTHON).
                // It is a good idea to start with allowAllAccess(true) and only when everything is
                // working to start trying to reduce it. See the GraalVM docs for fine-grained
                // permissions.
                        allowAllAccess(true).
                // Python virtualenvs work by setting up their initial package paths based on the
                // runtime path of the python executable. Since we are not executing from the python
                // executable, we need to set this option to what it would be
                        option("python.Executable", VENV_EXECUTABLE).
                // The actual package setup only happens inside Python's "site" module. This module is
                // automatically imported when starting the Python executable, but there is an option
                // to turn this off even for the executable. To avoid accidental file system access, we
                // do not import this module by default. Setting this option to true after setting the
                // python.Executable option ensures we import the site module at startup, but only
                // within the virtualenv.
                        option("python.ForceImportSite", "true").
                        build();
        InputStreamReader code = new InputStreamReader(MainApplication.class.getClassLoader().getResourceAsStream(SOURCE_FILE_NAME));
        Source source;
        try {
            source = Source.newBuilder(PYTHON, code, SOURCE_FILE_NAME).build();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        context.eval(source);
        return context.getPolyglotBindings();
    }
}
