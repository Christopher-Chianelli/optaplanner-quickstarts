import java
from annotations import PlanningId, PlanningScore, PlanningVariable, ValueRangeProvider, PlanningEntityCollectionProperty, ProblemFactCollectionProperty
from setup import generatePlanningEntityClass, generateProblemFactClass
from datetime import time

class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @PlanningId
    def getId(self):
        return self.id

    def __str__(self):
        return "Room(id=" + str(self.id) + ", name=" + str(self.name) + ")"

class Timeslot:
    def __init__(self, id, dayOfWeek, startTime, endTime):
        self.id = id
        self.dayOfWeek = dayOfWeek
        self.startTime = startTime
        self.endTime = endTime

    @PlanningId
    def getId(self):
        return self.id

    def __str__(self):
        return "Timeslot(id=" + str(self.id) + \
               ", dayOfWeek=" + str(self.dayOfWeek) + ", startTime=" + str(self.startTime) + \
               ", endTime=" + str(self.endTime) + ")"

TimeslotClass = generateProblemFactClass(Timeslot)
RoomClass = generateProblemFactClass(Room)

class Lesson:
    def __init__(self, id, subject, teacher, studentGroup, timeslot=None, room=None):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.studentGroup = studentGroup
        self.timeslot = timeslot
        self.room = room

    @PlanningId
    def getId(self):
        return self.id

    @PlanningVariable(TimeslotClass, valueRangeProviderRefs=["timeslotRange"])
    def getTimeslot(self):
        return self.timeslot

    def setTimeslot(self, newTimeslot):
        self.timeslot = newTimeslot

    @PlanningVariable(RoomClass, valueRangeProviderRefs=["roomRange"])
    def getRoom(self):
        return self.room

    def setRoom(self, newRoom):
        self.room = newRoom

    def __str__(self):
        return "Lesson(id=" + str(self.id) + \
                ", timeslot=" + str(self.timeslot) + ", room=" + str(self.room) + \
                ", teacher=" + str(self.teacher) + ", subject=" + str(self.subject) + \
                ", studentGroup=" + str(self.studentGroup) + ")"

LessonClass = generatePlanningEntityClass(Lesson)
HardSoftScore = java.type("org.optaplanner.core.api.score.buildin.hardsoft.HardSoftScore")

class TimeTable:
    def __init__(self, timeslotList=[], roomList=[], lessonList=[], score=None):
        self.timeslotList = timeslotList
        self.roomList = roomList
        self.lessonList = lessonList
        self.score = score

    @ProblemFactCollectionProperty(TimeslotClass)
    @ValueRangeProvider(id = "timeslotRange")
    def getTimeslotList(self):
        return self.timeslotList

    @ProblemFactCollectionProperty(RoomClass)
    @ValueRangeProvider(id = "roomRange")
    def getRoomList(self):
        return self.roomList

    @PlanningEntityCollectionProperty(LessonClass)
    def getLessonList(self):
        return self.lessonList

    @PlanningScore(HardSoftScore)
    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def __str__(self):
        return "TimeTable(timeSlotList=" + str(self.timeslotList) + \
               ", roomList=" + str(self.roomList) + ", lessonList=" + str(self.lessonList) + \
               ", score=" + str(self.score) + ")"

def generateProblem():
    timeslotList = [
        Timeslot(1, "MONDAY", time(hour=8, minute=30), time(hour=9, minute=30)),
        Timeslot(2, "MONDAY", time(hour=9, minute=30), time(hour=10, minute=30)),
        Timeslot(3, "MONDAY", time(hour=10, minute=30), time(hour=11, minute=30)),
        Timeslot(4, "TUESDAY", time(hour=8, minute=30), time(hour=9, minute=30)),
        Timeslot(5, "TUESDAY", time(hour=9, minute=30), time(hour=10, minute=30)),
        Timeslot(6, "TUESDAY", time(hour=10, minute=30), time(hour=11, minute=30)),
    ]
    roomList = [
        Room(1, "Room A"),
        Room(2, "Room B"),
        Room(3, "Room C")
    ]
    lessonList = [
        Lesson(1, "Math", "A. Turing", "9th grade"),
        Lesson(2, "Math", "A. Turing", "9th grade"),
        Lesson(3, "Physics", "M. Curie", "9th grade"),
        Lesson(4, "Chemistry", "M. Curie", "9th grade")
    ]
    return TimeTable(timeslotList, roomList, lessonList)