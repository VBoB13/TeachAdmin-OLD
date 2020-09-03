import numpy as np
import pandas as pd


DECIMALS = 2

class StudentGroup():

    def __init__(self, classInfo: pd.DataFrame):

        """Initiator for a 'StudentGroup' class (read: 'real life class') """

        self.listeningAvg = round(classInfo['Listening'].mean(), DECIMALS)
        self.listeningMin = round(classInfo['Listening'].min(), DECIMALS)
        self.listeningMax = round(classInfo['Listening'].max(), DECIMALS)

        self.readingAvg = round(classInfo['Reading'].mean(), DECIMALS)
        self.readingMin = round(classInfo['Reading'].min(), DECIMALS)
        self.readingMax = round(classInfo['Reading'].max(), DECIMALS)

        self.ffAvg = round(classInfo['English'].mean(), DECIMALS)
        self.ffMin = round(classInfo['English'].min(), DECIMALS)
        self.ffMax = round(classInfo['English'].max(), DECIMALS)

        self.phonicsAvg = round(classInfo['Phonics'].mean(), DECIMALS)
        self.phonicsMin = round(classInfo['Phonics'].min(), DECIMALS)
        self.phonicsMax = round(classInfo['Phonics'].max(), DECIMALS)

        self.rrAvg = round(classInfo['Running Record'].mean(), DECIMALS)
        self.rrMin = round(classInfo['Running Record'].min(), DECIMALS)
        self.rrMax = round(classInfo['Running Record'].max(), DECIMALS)

        self.homeworkAvg = round(classInfo['Homework'].mean(), DECIMALS)
        self.homeworkMin = round(classInfo['Homework'].min(), DECIMALS)
        self.homeworkMax = round(classInfo['Homework'].max(), DECIMALS)

        self.behaviorAvg = round(classInfo['Behavior'].mean(), DECIMALS)
        self.behaviorMin = round(classInfo['Behavior'].min(), DECIMALS)
        self.behaviorMax = round(classInfo['Behavior'].max(), DECIMALS)

        self.quizAvg = round(classInfo['DWS Quiz'].mean(), DECIMALS)
        self.quizMin = round(classInfo['DWS Quiz'].min(), DECIMALS)
        self.quizMax = round(classInfo['DWS Quiz'].max(), DECIMALS)

    def __str__(self):
        """Returns a string representation of a StudentGroup object"""
        return "\n--- Class Data ---\
                \nAvg. Listening Score 5:\t\t{}\
                \nAvg. Reading Score 5:\t\t{}\
                \nAvg. Family & Friends 5:\t{}\
                \nAvg. Phonics Score 5:\t\t{}\
                \nAvg. Running Record 5:\t\t{}\
                \nAvg. Homework Score 5:\t\t{}\
                \nAvg. Behavior Score 5:\t\t{}\
                \nAvg. Quiz Score 5:\t\t{}".format(self.listeningAvg,
                                                    self.readingAvg, self.ffAvg,
                                                    self.phonicsAvg, self.rrAvg,
                                                    self.homeworkAvg,
                                                    self.behaviorAvg,
                                                    self.quizAvg)
