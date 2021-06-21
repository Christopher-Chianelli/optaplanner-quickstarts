import polyglot
import java

TimeTable = java.type("org.acme.schooltimetabling.domain.TimeTable")
Lesson = java.type("org.acme.schooltimetabling.domain.Lesson")
Timeslot = java.type("org.acme.schooltimetabling.domain.Timeslot")
Room = java.type("org.acme.schooltimetabling.domain.Room")

LocalTime = java.type("java.time.LocalTime")
Duration = java.type("java.time.Duration")
DayOfWeek =  java.type("java.time.DayOfWeek")

Joiners = java.type("org.optaplanner.core.api.score.stream.Joiners")
HardSoftScore = java.type("org.optaplanner.core.api.score.buildin.hardsoft.HardSoftScore")

def within30Mins(lesson1, lesson2):
    between = Duration.between(lesson1.getTimeslot().getEndTime(),
                               lesson2.getTimeslot().getStartTime())
    return not between.isNegative() and between.compareTo(Duration.ofMinutes(30)) <= 0

def defineConstraints(constraintFactory):
    return [
        # Hard constraints
        roomConflict(constraintFactory),
        teacherConflict(constraintFactory),
        studentGroupConflict(constraintFactory),
        # Soft constraints
        teacherRoomStability(constraintFactory),
        teacherTimeEfficiency(constraintFactory),
        studentGroupSubjectVariety(constraintFactory)
    ]

def roomConflict(constraintFactory):
    # A room can accommodate at most one lesson at the same time.
    return constraintFactory \
            .fromUniquePair(Lesson,
            # ... in the same timeslot ...
                Joiners.equal(lambda lesson: lesson.getTimeslot()),
            # ... in the same room ...
                Joiners.equal(lambda lesson: lesson.getRoom())) \
            .penalize("Room conflict", HardSoftScore.ONE_HARD)


def teacherConflict(constraintFactory):
    # A teacher can teach at most one lesson at the same time.
    return constraintFactory \
                .fromUniquePair(Lesson,
                        Joiners.equal(lambda lesson: lesson.getTimeslot()),
                        Joiners.equal(lambda lesson: lesson.getTeacher())) \
                .penalize("Teacher conflict", HardSoftScore.ONE_HARD)

def studentGroupConflict(constraintFactory):
    # A student can attend at most one lesson at the same time.
    return constraintFactory \
            .fromUniquePair(Lesson,
                Joiners.equal(lambda lesson: lesson.getTimeslot()),
                Joiners.equal(lambda lesson: lesson.getStudentGroup())) \
            .penalize("Student group conflict", HardSoftScore.ONE_HARD)

def teacherRoomStability(constraintFactory):
    # A teacher prefers to teach in a single room.
    return constraintFactory \
                .fromUniquePair(Lesson,
                        Joiners.equal(lambda lesson: lesson.getTeacher())) \
                .filter(lambda lesson1, lesson2: lesson1.getRoom() != lesson2.getRoom()) \
                .penalize("Teacher room stability", HardSoftScore.ONE_SOFT)

def teacherTimeEfficiency(constraintFactory):
    # A teacher prefers to teach sequential lessons and dislikes gaps between lessons.
    return constraintFactory["from"](Lesson) \
                .join(Lesson, Joiners.equal(lambda lesson: lesson.getTeacher()),
                        Joiners.equal(lambda lesson: lesson.getTimeslot().getDayOfWeek())) \
                .filter(within30Mins) \
                .reward("Teacher time efficiency", HardSoftScore.ONE_SOFT)

def studentGroupSubjectVariety(constraintFactory):
    # A student group dislikes sequential lessons on the same subject.
    return constraintFactory["from"](Lesson) \
        .join(Lesson,
                        Joiners.equal(lambda lesson: lesson.getSubject()),
                        Joiners.equal(lambda lesson: lesson.getStudentGroup()),
                        Joiners.equal(lambda lesson: lesson.getTimeslot().getDayOfWeek())) \
        .filter(within30Mins) \
        .penalize("Student group subject variety", HardSoftScore.ONE_SOFT)

polyglot.export_value("TimeTableConstraintProvider", defineConstraints)