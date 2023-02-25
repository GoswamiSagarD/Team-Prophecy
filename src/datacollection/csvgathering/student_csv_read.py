import os
import re

import requests
import sqlite3

# from bs4 import BeautifulSoup

# CONSTS
connection = sqlite3.connect(os.getcwd() + os.sep + "course_info.db")

def init_create_db():
    print("Creating the initial databases for DAEN Data Dictionary...")
    print("Loading all databases for our venture")
    # This will be our program (program type = phd, masters or graduate cert; program_school = where we are getting the value from)
    connection.execute("CREATE TABLE student_info("
                       "student_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "reg_term TEXT NOT NULL, "
                       "admitted_term TEXT NOT NULL, "
                       "visa_type INTEGER NOT NULL, "
                       "acc_masters INTEGER NOT NULL, "
                       "program_code TEXT NOT NULL, "
                       "dept_code TEXT NOT NULL, "
                       "ret_ind INTEGER NOT NULL, "
                       "reg_status TEXT NOT NULL, "
                       "residency_grp INTEGER NOT NULL, "
                       "course_section TEXT NOT NULL, "
                       "reg_hours INTEGER NOT NULL"
                       ");")
