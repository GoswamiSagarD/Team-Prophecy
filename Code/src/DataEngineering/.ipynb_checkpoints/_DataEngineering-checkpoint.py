# Initiation
# importing required libraries
# import os
# import glob
# import pandas as pd

# importing the custom modules
from Code.src.DataEngineering.buildCourseData               import buildCourseData
from Code.src.DataEngineering.buildEnrollmentData           import buildEnrollmentData
from Code.src.DataEngineering.buildProfessorData            import buildProfessorData
from Code.src.DataEngineering.buildFinalEnrollStatusData    import buildFinalEnrollStatusData


def buildAllData():
    buildEnrollmentData()
    buildProfessorData()
    buildCourseData()
    buildFinalEnrollStatusData()