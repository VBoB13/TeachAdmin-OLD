# TeachAdmin
A website that is a tool for teachers to observe, analyze and manage their student's progress through various score data such as exams, assignments, tests and homeworks. It will be kept simple at first and gradually build up more advanced and (hopefully) even more useful functionalities.
Currently, these tools/libraries are used for this project:

## Tools / Libraries
1. Python 3.7.7
2. Django 3.0.6
3. pandas 1.0.3
4. matplotlib 3.1.3
5. seaborn 0.10.1

## Idea
It all started as I was simply helping my wife sorting out her students' test, homework and exam data and generating comments (that they have to provide to each student's parents by the end of the year). Teachers already have **VERY** extensive responsibilities and its often even more difficult for them to also have the time for analyzing the progress of each individual student.
The core idea behind this project is to make teachers able to explore the data they put in about their students, thus enabling the teachers to observe, analyze and manage their students' learning progress through the course of time. While the main functionality is to simply provide visual graphs generated with the students score data, thus allowing teachers to quickly get an overview of the progress of the students, the system will also be able to eventually point out which students struggle in particular when compared to other students in the same subject etc. Machine learning will most likely end up being used to figure out patterns in the data that could provide teachers with hints about these things.

## Structure / Models
- Teacher (user)
- School
    - Each teacher can add schools to their 'portfolio' (not a real term within the app itself, but I don't know any better way of explaining it). Within each school, they can then add homerooms or subjects.
- Homeroom
    - The term simply comes from the term "homeroom teacher" as in "teacher who teaches certain subject(s) to a certain set of students", thus making that "homeroom" a *fixed group of students that the teacher is educating*.
- Subject
    - Subjects, just like the name suggests, is referred to as the subject that the teacher is teaching. The idea is that teachers should mainly use their subject-page is their go-to page to analyze scores as it is often easier and more accurate to analyze data all from the same context (subject). Any subject can be assigned to multiple Homerooms to make sure each teacher can teach the same material to students with or without a Homeroom.
- Exam
    - As the name suggests, it represents the exams in each subject. Each subject can (obviously) have many exams.
- ExamScore
    - The score tied to any one Exam that the teacher has added to their 'portfolio' AND the student that took the exam. E.g. the record of a student having a score in an exam.
- Assignment
    - Can be viewed as any major 'paper' or 'project' for a subject.
- AssignmentScore
    - Like ExamScore, but for Assignments.
- Lesson
    - Each subject will be able to have lessons added to them. Within each lesson, the teacher can then add tests and homeworks.
- LessonTest
    - Tests for lessons. They're almost identical to Exams in terms of structure, thus serving an almost identical purpose.
- LessonTestScore
    - Score for LessonTests
- Homework
    - Just like Assignments, but for Lessons.
- HomeworkScore
    - Score for Homeworks.
- BehaviorCategory
    - This model has yet to be implemented and utilized in the app, but eventually this model (together with BehaviorEvents) will help teachers track behaviors of students and if and/or how they impact the students' progress.
- BehaviorEvent
    - Used to keep track of behaviors (BehaviorCategory) for a specific student (Student).
