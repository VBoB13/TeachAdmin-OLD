from . import StudentGroup


class Student():
    """Student class with attributes to decide how
        the comments are eventually generated.
        This is where almost ALL the logic behind the script is,
        making the main function much cleaner and the algorithm easier
        to follow."""

    # Initiating the 'comment'-attribute for convenience
    # The full comment gets generated automatically through data validation
    # of each student's scores
    comment = None

    def __init__(self, name:str, gender:str, listening:int, reading:int, ff:int,
                        phonics:int, rr:int, homework:int, behavior:int,
                        quiz:int, classInfo:StudentGroup):
        """Classic initiator function for any custom Python class"""

        # Assigning the student's name to the Student class's <name> attribute
        # This makes us able to call Student.name to return a student's name
        self.name = name.title()
        self.gender = gender

        # This simply checks whether the Student object's <name> attribute
        # can be found in the preset list of female names
        # This is so that the pronouns are automatically assigned as well :)
        if self.gender == 'Female':
            self.pronoun = 'she'
            self.third_person_pronoun = 'her'
            self.ownership_pronoun = 'her'
        else:
            self.pronoun = 'he'
            self.third_person_pronoun ='him'
            self.ownership_pronoun = 'his'

        # Here we are simply just assigning each score to the class attributes
        self.listening = listening
        self.reading = reading
        self.family_friends = ff
        self.phonics = phonics
        self.running_record = rr
        self.homework = homework
        self.behavior = behavior
        self.quiz = quiz
        self.classInfo = classInfo

        # ------------- KEY MOMENT ---------------
        # Here, a function gets called to generate comments for each student
        self.comment = self._generate_comments()

    def __str__(self):
        """This function is a standard way of customizing the way your
        custom object, in this case - the [Student] objects, gets printed"""

        # Arranging these statements will just adjust the way each Student object
        # looks when it's printed
        return "\n----------------------------------------------------------"+\
                    f"\nName: \t\t\t{self.name} \
                    \nListening: \t\t{self.listening} \
                    \nReading: \t\t{self.reading} \
                    \nFamily & Friends: \t{self.family_friends}\
                    \nPhonics: \t\t{self.phonics}\
                    \nRunning Record: \t{self.running_record}\
                    \nHomework: \t\t{self.homework}\
                    \nBehavior: \t\t{self.behavior}\
                    \nQuiz: \t\t\t{self.quiz}\
                    \n\n--- Comments --- \n{self.comment}" + \
                    "\n----------------------------------------------------------\n"

    def _get_comment_outro(self):
        """Generates an intro to the comments"""
        # NOTE:
        # The underscore at the beginning of the name simply indicates that this
        # function is meant to be used by this class internally, usually
        # automatically / 'behind the scenes', which we do here

        comment_outro = "\nOverall:\n\t"

        totalScore = self.listening + self.reading + self.family_friends + self.phonics

        proud = [
                        "Keep trying, " + self.name + "!",
                        "I am very proud of " + self.name + ".",
                        "I am extremely proud of " + self.name + ".",
                        "\nI look forward to seeing " + self.third_person_pronoun + " continue to grow."
                    ]

        if totalScore > 190:
            comment_outro += proud[2] + proud[3]
        elif 190 >= totalScore >= 170:
            comment_outro += proud[1] + proud[3]
        else:
            comment_outro += proud[0] + proud[3]

        return comment_outro


    def _get_listening_comment(self):
        """Generates listening comments for a student."""

        listeningComment = "Listening:\n\t"

        if self.listening == 60:
            listeningComment += f"{self.name} got a perfect score - {str(self.listening)} "+\
                "- on the listening section! Incredible!"

        elif 60 > self.listening >= 55:
            listeningComment += f"{self.name} scored a whopping {str(self.listening)} points in the listening "+\
                "section! That's fantastic!"+\
                f"\nTo improve in this area even further, I recommend {self.third_person_pronoun} "+\
                "to study the vocabulary in addition to the phrases from the "+\
                "Fluency Time section.\n"

        elif 55 > self.listening >= 50:
            listeningComment += f"{self.name} scored {str(self.listening)} points in the listening "+\
                "section! That's very good!"+\
                f"\nTo improve in this area even further, I recommend {self.third_person_pronoun} "+\
                "to study the vocabulary in addition to the phrases from the "+\
                "Fluency Time section.\n"

        elif 50 > self.listening >= 45:
            listeningComment += f"{self.name} scored {str(self.listening)}, thus "+\
                f"{self.pronoun} missed {str(60 - self.listening)} points in the "+\
                "listening section."+\
                f"\nTo improve {self.name}'s reading skills, I recommend {self.pronoun} "+\
                "to study the vocabulary as well as the phrases from the Fluency "+\
                "Time section."

        else:
            listeningComment += f"{self.name} lost {str(60 - self.listening)}  points in the listening section."+\
                f"\nTo improve in this area, I recommend {self.third_person_pronoun} to study the vocabulary "+\
                "in addition to the phrases from the Fluency Time section. With "+\
                f"some extra practice and guidance, I have no doubt {self.name}'s' "+\
                "reading will soon improve."

        if self.listening > self.classInfo.listeningAvg:
            listeningComment += f"{self.name}'s score was higher than the average listening score! Great!"

        return listeningComment


    def _get_family_friends_comment(self):
        """Generates 'Family & Friends' comments for a student"""

        family_friends_comment = "\nFamily & Friends:\n\t"

        if self.family_friends == 60:
            family_friends_comment += f"{self.name} scored a full pot - "+\
                f"{str(self.family_friends)} points in the Family and Friends seciton!\n"

        elif 60 > self.family_friends >= 55:
            family_friends_comment += f"{self.name} scored {str(self.family_friends)} "+\
                "points in the Family and Friends section, which is amazing!"+\
                f"\nTo improve even further in this area, {self.pronoun} should review the "+\
                "vocabulary and grammar covered in the Super Study Sheet.\n"

        elif 55 > self.family_friends >= 50:
            family_friends_comment += f"{self.name} scored {str(self.family_friends)} "+\
                "points in the Family and Friends section, which is very good."+\
                f"\nTo improve even further in this area, {self.pronoun} should review the "+\
                "vocabulary and grammar covered in the Super Study Sheet.\n"


        else:
            family_friends_comment += f"{self.name} lost {str(60 - self.family_friends)} "+\
                "points in the Family and Friends section."+\
                f"\nTo improve in this area, {self.pronoun} should revise "+\
                "the vocabulary and grammar covered in the Super Study sheet.\n"

        if self.family_friends > self.classInfo.ffAvg:
            family_friends_comment += f"{self.name} scored higher than the average "+\
                "for the Family & Friends section. Great job!"

        return family_friends_comment


    def _get_running_record_comment(self):
        """Generates running record comments for a student"""

        running_record_comment = "\nRunning record:\n\t"

        if self.running_record == 100:
            running_record_comment += f"{self.name} scored 100% in Running Record."+\
                f" This is truly impressive! {self.pronoun} shows "+\
                "great potential." + \
                f"\n{self.pronoun.title()} could do very well in the English "+\
                " Competition with enough practice.\n"

        elif 90 <= self.running_record < 100:
            running_record_comment += f"{self.name} scored {str(self.running_record)} "+\
                f"for reading.\nEven if {self.pronoun} still have room for "+\
                f"growth, {self.name} is doing very well.\n"

        elif 90 > self.running_record >= 80:
            running_record_comment += f"{self.name} scored {str(self.running_record)} "+\
                " for reading. Although there is room for improvement, there is "+\
                f"no need to worry about {self.name}.\n"

        else:
            running_record_comment += f"{self.name} finds reading aloud more "+\
                f"challenging. I would recommend that {self.pronoun} tries "+\
                "using read along stories on Youtube or read along apps to help "+\
                "improve the Running Record scores. The English Competition "+\
                "also helps in this regard.\n"

        if self.running_record > self.classInfo.rrAvg:
            running_record_comment += f"{self.name} scored higher than average "+\
                "on the Running Record section. Great!"

        return running_record_comment

    def _get_homework_comment(self):
        """Generates the homework comments for a student"""

        homework_comment = "\nHomework:\n\t"

        if self.homework >= 90:
            homework_comment += f"{self.name} scored a full {str(self.homework)} on the Homework "+\
                f"section and that is fabulous.\n"
        elif 90 > self.homework >= 80:
            homework_comment += f"{self.name} scored {str(self.homework)} on "+\
                "the Homework section. That's really good!\n"
        else:
            homework_comment += f"{self.name} scored {str(self.homework)} on "+\
                "the Homework section. << ADDITIONAL COMMENTS? >>\n"

        if self.homework > self.classInfo.homeworkAvg:
            homework_comment += f"{self.name} scored higher than the average "+\
                "student on the Homework section.\n"

        return homework_comment

    def _get_behavior_comment(self):
        """Generates the behavior comments for a student"""

        behavior_comment = "\nBehavior:\n\t"

        if self.behavior == 100:
            behavior_comment += f"{self.name}'s behavior in class in exceptional. "+\
                f"{self.pronoun.title()} is a really good student and {self.pronoun} "+\
                "tries really hard.\n"
        elif 100 > self.behavior >= 95:
            behavior_comment += f"{self.name}'s behavior in class is really good.\n"
        elif 95 > self.behavior >= 90:
            behavior_comment += f"{self.name}'s behavior in class is good. "+\
                f"Though {self.pronoun} has room for growth, {self.pronoun} "+\
                f"is trying hard and I have no doubt that {self.pronoun} will "+\
                "continue to improve.\n"
        elif 90 > self.behavior >= 85:
            behavior_comment += f"{self.name}'s behavior in class is OK. "+\
                f"{self.pronoun.title()} has lots of room for growth, but "+\
                f"I am sure {self.ownership_pronoun} behavior will improve.\n"
        else:
            behavior_comment += f"{self.name}'s behavior in class is challenging."+\
                f"{self.pronoun.title()} struggles with paying attention and "+\
                "concentrating in class.\n"

        return behavior_comment

    def _get_quiz_comment(self):
        """Generates the quiz comments for a student"""

        quiz_comment = "\nQuiz:\n\t"

        if self.quiz > 80:
            quiz_comment += f"{self.name} is often prepared for the weekly "+\
                f"quizzes and earned a score of {str(self.quiz)}. Very good!\n"
        else:
            if self.quiz < self.classInfo.quizAvg:
                quiz_comment += f"{self.name} is not very prepared for the weekly "+\
                    "quizzes."
            else:
                quiz_comment += f"{self.name} is mostly prepared for the weekly "+\
                    f"quizzes, but I know {self.pronoun} can do better."

        return quiz_comment

    def _generate_comments(self):
        """This is the function that contains the main logic behind generating
            comments for each individual student"""

        listeningComment = self._get_listening_comment()
        family_friendsComment = self._get_family_friends_comment()
        running_recordComment = self._get_running_record_comment()
        homeworkComment = self._get_homework_comment()
        behaviorComment = self._get_behavior_comment()
        quizComment = self._get_quiz_comment()

        comment_outro = self._get_comment_outro()

        comments = listeningComment + "\n" + \
                    family_friendsComment + "\n" + \
                    running_recordComment + "\n" + \
                    homeworkComment + "\n" + \
                    behaviorComment + "\n" + \
                    quizComment + "\n" + \
                    comment_outro

        return comments


if __name__ == '__main__':
    print("Running student.py directly!")
else:
    print("IMPORTED: student.py")
