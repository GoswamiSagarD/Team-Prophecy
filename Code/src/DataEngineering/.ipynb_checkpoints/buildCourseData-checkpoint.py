# Initiation
# importing required libraries
import os
import glob
import pandas as pd

# importing the custom modules
from Code.src.modules.db_ops import *
from Code.src.dataengineering.buildWebscrapeData import *


def buildCourseData():
    init()
    # Course Data
    print("#"*40, "\t", "\n", "Course Data")
    # Copying the course database file to the processed folder
    print("Copying the Course database file to the processed folder... [1/1]")
    os.system("cp Data/01_raw/CourseData/intermediate.db Data/02_processed/course4EDA.db")

    print("Course Data processed successfully!")