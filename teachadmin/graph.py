from .models import *
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import io
import urllib
import base64

assignment = Assignment()
exam = Exam()
lessontest = LessonTest()
homework = Homework()

SINGLE_SCORE_MODELS = (assignment, exam, lessontest, homework)

lesson = Lesson()
subject = Subject()
homeroom = HomeRoom()

MULTIPLE_SCORE_MODELS = (lesson, subject, homeroom)

class Graph():
    """ This class is meant to simplify the code for generating graphs
        for all the different views in the TeachAdmin application.
        params: model (model object) """

    model_instance = None
    model = None
    uri = False
    df = pd.DataFrame()

    def __init__(self, model_instance):
        try:
            for score_model in SINGLE_SCORE_MODELS:
                if type(model_instance) == type(score_model):
                    self.model = score_model
            for multiscore_model in MULTIPLE_SCORE_MODELS:
                if type(model_instance) == type(multiscore_model):
                    self.model = multiscore_model

            self.model_instance = model_instance
            self.df = self._get_dataframe()
            self.uri = self._get_uri()

        except TypeError as te:
            print("Cannot establish Graph object.")
            print(te)

    def __str__(self):
        return "{}: {}".format(self.model, self.model_instance)

    def _create_score_df(self):
        students = self.model_instance.students()
        all_scores = self.model_instance.scores()
        if len(students) != 0 and all_scores != None:
            scores_dict = {
                'Student': [],
                'Gender': [],
                '{}'.format(self.model_instance): []
            }    
            for student in students:
                score_list = []
                for score in all_scores.filter(student=student):
                    score_list.append(score.score)
                if len(score_list) >= 1:
                    max_score = max(score_list)
                else:
                    max_score = None
                scores_dict['Student'].append(student)
                scores_dict['Gender'].append(student.gender)
                scores_dict['{}'.format(self.model_instance)].append(max_score)
            
            try:
                df = pd.DataFrame(data=scores_dict)
            except Exception as err:
                print("Error while creating DataFrame for {}".format(self.model_instance))
                print(err)
            else:
                if not df.empty:
                    df['Gender'] = df['Gender'].apply(self._gender_map)
                    return df
        else:
            return pd.DataFrame()

    def _create_multiple_score_df(self):
        students = self.model_instance.students()
        score_model_list = self.model_instance.get_score_models()
        if (len(score_model_list) > 0) and students:
            scores_dict = {
                'Student': [],
                'Gender': []
            }
            for score_model in score_model_list:
                all_scores = score_model.scores()
                if '{}'.format(score_model) not in scores_dict.keys():
                    scores_dict['{}({})'.format(score_model, score_model.pk)] = []
                
                for student in students:
                    if student not in scores_dict['Student']:
                        scores_dict['Student'].append(student)
                        scores_dict['Gender'].append(student.gender)
                    if type(score_model) in (type(lessontest), type(homework)):
                        if all_scores.filter(student=student).exists():
                            scores_list = []
                            for score in all_scores.filter(student=student):
                                scores_list.append(round((score.score/score_model.max_score)*100,1))
                            scores_dict['{}({})'.format(score_model, score_model.pk)].append(max(scores_list))
                        else:
                            scores_dict['{}({})'.format(score_model, score_model.pk)].append(None)
            
            for key, value in scores_dict.items():
                print(key, value)
            
            try:
                df = pd.DataFrame(data=scores_dict)
            except Exception as err:
                print("Couldn't create DataFrame for {}!".format(self.model_instance))
                print(err)
                df = pd.DataFrame()
            else:
                df['Gender'] = df['Gender'].apply(self._gender_map)
                avg_scores = []
                for column in df.select_dtypes(include=['float64']).columns:
                    avg_scores.append(round(df[column].mean(), 1))
                df.insert(2, "{} avg.".format(self.model_instance), avg_scores)
                print(df)
        
        return df

    def _gender_map(self, gender):
        if gender == 'F':
            return 'Female'
        elif gender == 'M':
            return 'Male'
        else:
            return 'Other'

    def _get_dataframe(self):
        df = pd.DataFrame()
        if self.model in SINGLE_SCORE_MODELS:
            df = self._create_score_df()
        else:
            df = self._create_multiple_score_df()
        return df
    
    def _create_uri(self):
        # Initiating graph
        fig = plt.figure()
        sns.set_style(style='darkgrid')
        plt.style.use("dark_background")
        axes = fig.gca()

        # Note: Since the seaborn 'swarmplot' wouldn't let me omit either 'x' or 'y' to get the 'hue' shown properly
        # I had to provide 'dummy-data' for the 'x' to make the 'hue' work
        # Link to issue: https://github.com/mwaskom/seaborn/issues/941
        if self.model in SINGLE_SCORE_MODELS:
            sns.swarmplot(
                data=self.df,
                x=[""]*len(self.df),
                y='{}'.format(self.model_instance),
                hue='Gender',
                palette='deep',
                size=7,
                edgecolor='white',
                linewidth=1
            )
            axes.legend(title='Gender', loc='center left',
                        bbox_to_anchor=(1.02, 0.90))
        else:
            sns.swarmplot(
                data=self.df.select_dtypes(include=['float64']),
                palette='deep',
                size=7,
                edgecolor='white',
                linewidth=1
            )
        axes.set_ylim(
            (self.df.min(axis=0, numeric_only=True).min())-2,
            (self.df.max(axis=0, numeric_only=True).max())+2
        )
        plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")
        axes.set_title("{} scores".format(self.model_instance))
        plt.tight_layout()

        # Getting the complete filepath to which we save the graph
        buf = io.BytesIO()
        try:
            plt.savefig(buf, format='png')
        except Exception as err:
            print("Error while saving graph for {}".format(self.model_instance))
            print(err)
            return False
        else:
            buf.seek(0)
            pltstring = base64.b64encode(buf.read())
            uri = urllib.parse.quote(pltstring)
            return uri

    def _get_uri(self):
        if not self.df.empty:
            uri = self._create_uri()
            return uri
        return None

    
