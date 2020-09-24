from .models import *
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import io
import urllib
import base64

MODELS = (Student, LessonTest)

class Graph():
    """ This class is meant to simplify the code for generating graphs
        for all the different views in the TeachAdmin application.
        params: model (model object) """

    model_instance = None
    model = None
    uri = None
    df = None

    def __init__(self, model):
        try:
            if isinstance(model, MODELS):
                if isinstance(model, Student):
                    self.model = Student
                    self.model_instance = model
                    self.df = self._get_dataframe()
                    self.uri = self._get_uri()
                elif isinstance(model, LessonTest):
                    self.model = LessonTest
                    self.model_instance = model
                    self.df = self._get_dataframe()
                    self.uri = self._get_uri()
                else:
                    pass
        except TypeError as te:
            print("Cannot establish Graph object.")
            print(te)

    def __str__(self):
        return "{}: {}".format(self.model, self.model_instance)

    def _get_df_lessontest(self):
        students = self.model_instance.students()
        all_scores = self.model_instance.scores()
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
                if "Gender" in df.columns:
                    df['Gender'] = df['Gender'].apply(self._gender_map)
                return df

    def _gender_map(self, gender):
        if gender == 'F':
            return 'Female'
        elif gender == 'M':
            return 'Male'
        else:
            return 'Other'

    def _get_dataframe(self):
        if self.model == LessonTest:
            df = self._get_df_lessontest()
            
        return df
    
    def _get_uri_lessontest(self):
        # Initiating graph
        fig = plt.figure()
        sns.set_style(style='darkgrid')
        plt.style.use("dark_background")

        # Note: Since the seaborn 'swarmplot' wouldn't let me omit either 'x' or 'y' to get the 'hue' shown properly
        # I had to provide 'dummy-data' for the 'x' to make the 'hue' work
        # Link to issue: https://github.com/mwaskom/seaborn/issues/941
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
        axes = fig.gca()
        axes.set_ylim(
            (self.df.min(axis=0, numeric_only=True).min())-2,
            (self.df.max(axis=0, numeric_only=True).max())+2
        )
        plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")
        axes.set_title("{} scores".format(self.model_instance))
        axes.legend(title='Gender', loc='center left',
                    bbox_to_anchor=(1.02, 0.90))
        plt.tight_layout()

        # Getting the complete filepath to which we save the graph
        buf = io.BytesIO()
        try:
            plt.savefig(buf, format='png')
        except Exception as err:
            print("Error while saving graph for {}".format(self.model_instance))
            print(err)
        else:
            buf.seek(0)
            pltstring = base64.b64encode(buf.read())
            uri = urllib.parse.quote(pltstring)
            return uri

        return False

    def _get_uri(self):
        if self.model == LessonTest:
            uri = self._get_uri_lessontest()

        return uri

    
