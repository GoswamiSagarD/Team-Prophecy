# Initiation
# importing required libraries
import os
import pandas as pd

# importing the custom modules
from Code.src.modules.db_ops import *


def buildProfessorData():
    # # Professor Data
    print("#"*40, "\t", "\n", "Professor Data")
    print("Importing the Professor Data... [1/3]")
    # Importing the CSV File
    df_professor = pd.read_excel(
        os.path.join("Data", "01_raw", "ProfessorData", "CEC Course Info including Fac Name.xlsx")
    )

    # renaming the columns
    rename_dict = {
        "Stu Term"                              : "reg_term_desc",
        "Unnamed: 1"                            : "reg_term_code",
        "Course Sect College"                   : "crs_sect_clg",
        "Course Sect Level"                     : "crs_sect_level",
        "Course Sect Primary Instr Home Org"    : "instr_home_org",
        "Course Sect Primary Instr Name"        : "instr_name",
        "Course Sect Dept"                      : "crs_sect_dept",
        "Unnamed: 7"                            : "crs_sect_dept_desc",
        "Course Sect Campus"                    : "crs_sect_camp",
        "Course Desc"                           : "crs",
        "Course Sect Section Number"            : "crs_sect",
        "Course Sect Instruction Delivery Method Group" : "crs_sect_modality",
        "Course Status"                         : "crs_sect_status",
        "Course Sect Term Actual Enrolled"      : "crs_sect_enroll_count",
        "Course Sect Term Seats Avail"          : "crs_sect_enroll_avail",
        "Course Sect Term Waitlist Count"       : "crs_sect_enroll_waitlist",
    }
    df_professor.rename(columns=rename_dict, inplace=True)

    # Extracting features from the dataset

    # splitting the "reg_term_desc" column into term and year
    df_professor["reg_term_name"] = df_professor["reg_term_desc"].str.split(" ", expand=True)[0]
    df_professor["reg_term_year"] = df_professor["reg_term_desc"].str.split(" ", expand=True)[1]

    # combining the above two columns to create a new column
    df_professor["crs_sect"] = df_professor["crs"] + " " + df_professor["crs_sect"]

    # Cleaning the dataset
    print("Cleaning the Professor dataset... [2/3]")
    df_professor['instr_home_org'].replace("'--", "No Value", inplace=True)
    df_professor['instr_name'].replace(',  ', "No Value", inplace=True)

    # Sorting the dataframe and creating a new index

    df_professor.sort_values(
        by=['reg_term_code', 'crs_sect_dept', 'crs_sect'], inplace=True)

    df_professor.reset_index(drop=True, inplace=True)

    df_professor['rec_id'] = df_professor.index

    # Converting the columns to the appropriate data types
    df_professor['reg_term_code']           = df_professor['reg_term_code'].astype('category')
    df_professor['reg_term_year']           = df_professor['reg_term_year'].astype('int')
    df_professor['reg_term_name']           = df_professor['reg_term_name'].astype('category')
    df_professor['reg_term_desc']           = df_professor['reg_term_desc'].astype('category')
    df_professor['crs_sect_clg']            = df_professor['crs_sect_clg'].astype('category')
    df_professor['crs_sect_camp']           = df_professor['crs_sect_camp'].astype('category')
    df_professor['crs_sect_dept']           = df_professor['crs_sect_dept'].astype('category')
    df_professor['crs_sect_dept_desc']      = df_professor['crs_sect_dept_desc'].astype('category')
    df_professor['crs_sect_level']          = df_professor['crs_sect_level'].astype('category')
    df_professor['crs_sect_modality']       = df_professor['crs_sect_modality'].astype('category')
    df_professor['crs_sect_status']         = df_professor['crs_sect_status'].astype('category')
    df_professor['instr_name']              = df_professor['instr_name'].astype('category')
    df_professor['instr_home_org']          = df_professor['instr_home_org'].astype('category')
    df_professor['crs_sect_enroll_count']   = df_professor['crs_sect_enroll_count'].astype('int')
    df_professor['crs_sect_enroll_avail']   = df_professor['crs_sect_enroll_avail'].astype('int')
    df_professor['crs_sect_enroll_waitlist']= df_professor['crs_sect_enroll_waitlist'].astype('int')

    # Reordering the columns
    df_professor = df_professor[[
        # Records Info
        'rec_id',
        # Registration Term/Semester Info
        'reg_term_code', 'reg_term_year', 'reg_term_name', 'reg_term_desc',
        # Course Info
        'crs', 'crs_sect', 'crs_sect_clg', 'crs_sect_camp', 'crs_sect_dept', 'crs_sect_dept_desc',
        'crs_sect_level', 'crs_sect_modality', 'crs_sect_status', 'Course Sect Term Count',
        # Professor Info
        'instr_name', 'instr_home_org',
        # Enrollment Info
        'crs_sect_enroll_count', 'crs_sect_enroll_avail', 'crs_sect_enroll_waitlist'
    ]]


    print("Exporting the Professor dataset... [3/3]")
    # Saving the dataframe as a pickle file
    df_professor.to_pickle(
        os.path.join("Data", "02_processed", "professor.pkl")
    )

    # Saving the dataframe to a csv file
    df_professor.to_csv(
        os.path.join("Data", "02_processed", "professor.csv"), index=False
    )

    # Saving the dataframe to a new sqlite database
    db_professor = ConnectDB(
        os.path.join("Data", "02_processed", "CECData.db")
    )
    df_professor.to_sql('professor', db_professor.connection, if_exists='replace', index=False)
    db_professor.commitDB()

    print("Professor Data processed successfully!")