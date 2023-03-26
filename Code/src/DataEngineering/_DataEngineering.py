# Initiation
# importing required libraries
# import os
# import glob
# import pandas as pd

# importing the custom modules
from Code.src.dataengineering.buildCourseData               import buildCourseData
from Code.src.dataengineering.buildEnrollmentData           import buildEnrollmentData
from Code.src.dataengineering.buildProfessorData            import buildProfessorData
from Code.src.dataengineering.buildFinalEnrollStatusData    import buildFinalEnrollStatusData
from Code.src.dataengineering.buildInitialDatabaseTables    import buildInitCreateDBS

def buildAllData():
    buildInitCreateDBS()
    buildCourseData()
    buildEnrollmentData()
    buildProfessorData()
    buildFinalEnrollStatusData()