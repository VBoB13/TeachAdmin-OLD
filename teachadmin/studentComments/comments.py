# This script is written with the newest Python version at the moment, which is
# Python 3.7.


from student import Student
from StudentGroup import StudentGroup
import numpy as np
import pandas as pd



if __name__ == '__main__':
    print("RUNNING: comments.py")
    """This is the main function of the algorithm. I rewrote the script into
    Object Oriented Code so that it would be easier for you to read and possibly
    also fully understand what is actually going on.
    If there are any questions about the code, just ask. I will try my best to fix
    whatever problem, bug or extra function you need."""

    # This line reads in data from a datasheet in form of a .csv-file
    # This version only has a hard-coded file name, so you will HAVE TO save the
    # scores into another 'scores.csv' file in order for this to work properly.
    result = pd.read_csv('scores.csv', index_col = 'Number')

    # This simply prints the content from the file out to the screen and a
    # small summary about it as well
    # Mostly for testing, but I left it there in case you (Benjamin) were interested
    # Don't worry - Jenn probably doesn't care :P
    print("\n", result, "\n", result.info())

    studentClass = StudentGroup(result)
    print(studentClass)


    # This iterates through each row in the table of the .csv-file
    for index, row in result.iterrows():
        # This line creates a Student-object out of all the
        # lines of data from the file
        student = Student(row['Name'], row['Gender'],
                            row['Listening'], row['Reading'],
                            row['English'], row['Phonics'],
                            row['Running Record'], row['Homework'],
                            row['Behavior'], row['DWS Quiz'], studentClass)

        # After the Student object is created,
        # it's simply printed to the console.
        print(student)

        # In order to make things slightly smoother for you, I decided to write
        # all of the information into .txt-files
        # Each student (with comments) are printed into THEIR OWN INDIVIDUAL
        # .txt-file with names such as:
        # << Student Number >>.txt
        txtFile = open(f"{index}.txt", "w+")
        txtFile.write(student.__str__())
        txtFile.close()

else:
    print("IMPORTED: comments.py")
