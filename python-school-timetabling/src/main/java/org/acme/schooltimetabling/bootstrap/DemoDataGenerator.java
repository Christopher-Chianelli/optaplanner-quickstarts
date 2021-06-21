/*
 * Copyright 2020 Red Hat, Inc. and/or its affiliates.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.acme.schooltimetabling.bootstrap;

import org.acme.schooltimetabling.domain.Lesson;
import org.acme.schooltimetabling.domain.Room;
import org.acme.schooltimetabling.domain.TimeTable;
import org.acme.schooltimetabling.domain.Timeslot;

import java.time.DayOfWeek;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

public class DemoDataGenerator {

    public static TimeTable generateDemoData() {
        List<Timeslot> timeslotList = new ArrayList<>(10);
        timeslotList.add(new Timeslot(1L, DayOfWeek.MONDAY, LocalTime.of(8, 30), LocalTime.of(9, 30)));
        timeslotList.add(new Timeslot(2L, DayOfWeek.MONDAY, LocalTime.of(9, 30), LocalTime.of(10, 30)));
        timeslotList.add(new Timeslot(3L,DayOfWeek.MONDAY, LocalTime.of(10, 30), LocalTime.of(11, 30)));
        timeslotList.add(new Timeslot(4L, DayOfWeek.MONDAY, LocalTime.of(13, 30), LocalTime.of(14, 30)));
        timeslotList.add(new Timeslot(5L, DayOfWeek.MONDAY, LocalTime.of(14, 30), LocalTime.of(15, 30)));

        timeslotList.add(new Timeslot(6L, DayOfWeek.TUESDAY, LocalTime.of(8, 30), LocalTime.of(9, 30)));
        timeslotList.add(new Timeslot(7L, DayOfWeek.TUESDAY, LocalTime.of(9, 30), LocalTime.of(10, 30)));
        timeslotList.add(new Timeslot(8L, DayOfWeek.TUESDAY, LocalTime.of(10, 30), LocalTime.of(11, 30)));
        timeslotList.add(new Timeslot(9L, DayOfWeek.TUESDAY, LocalTime.of(13, 30), LocalTime.of(14, 30)));
        timeslotList.add(new Timeslot(10L, DayOfWeek.TUESDAY, LocalTime.of(14, 30), LocalTime.of(15, 30)));

        List<Room> roomList = new ArrayList<>(3);
        roomList.add(new Room(1L,"Room A"));
        roomList.add(new Room(2L,"Room B"));
        roomList.add(new Room(3L,"Room C"));

        List<Lesson> lessonList = new ArrayList<>();
        lessonList.add(new Lesson(1L,"Math", "A. Turing", "9th grade"));
        lessonList.add(new Lesson(2L,"Math", "A. Turing", "9th grade"));
        lessonList.add(new Lesson(3L,"Physics", "M. Curie", "9th grade"));
        lessonList.add(new Lesson(4L,"Chemistry", "M. Curie", "9th grade"));
        lessonList.add(new Lesson(5L,"Biology", "C. Darwin", "9th grade"));
        lessonList.add(new Lesson(6L,"History", "I. Jones", "9th grade"));
        lessonList.add(new Lesson(7L,"English", "I. Jones", "9th grade"));
        lessonList.add(new Lesson(8L,"English", "I. Jones", "9th grade"));
        lessonList.add(new Lesson(9L,"Spanish", "P. Cruz", "9th grade"));
        lessonList.add(new Lesson(10L,"Spanish", "P. Cruz", "9th grade"));

        lessonList.add(new Lesson(11L,"Math", "A. Turing", "10th grade"));
        lessonList.add(new Lesson(12L,"Math", "A. Turing", "10th grade"));
        lessonList.add(new Lesson(13L,"Math", "A. Turing", "10th grade"));
        lessonList.add(new Lesson(14L,"Physics", "M. Curie", "10th grade"));
        lessonList.add(new Lesson(15L,"Chemistry", "M. Curie", "10th grade"));
        lessonList.add(new Lesson(16L,"French", "M. Curie", "10th grade"));
        lessonList.add(new Lesson(17L,"Geography", "C. Darwin", "10th grade"));
        lessonList.add(new Lesson(18L,"History", "I. Jones", "10th grade"));
        lessonList.add(new Lesson(19L,"English", "P. Cruz", "10th grade"));
        lessonList.add(new Lesson(20L,"Spanish", "P. Cruz", "10th grade"));

        Lesson lesson = lessonList.get(0);
        lesson.setTimeslot(timeslotList.get(0));
        lesson.setRoom(roomList.get(0));

        return new TimeTable(timeslotList, roomList, lessonList);
    }

    public enum DemoData {
        NONE,
        SMALL,
        LARGE
    }

}
