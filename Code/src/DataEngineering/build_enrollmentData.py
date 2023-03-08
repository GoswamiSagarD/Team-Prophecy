# importing required libraries
import os
import glob
import pandas as pd

# importing the custom modules
from Code.src.modules.db_ops import *













# Enrollment Data
# Merging the Enrollment data from all the CSV files in the EnrollmentData folder
files = glob.glob(
    os.path.join("Data", "01_raw", "EnrollmentData", "*.csv")
)

# Reading each file, adding filename as a column and appending to a pandas dataframe
df_enrollment = pd.read_csv(files[0])
df_enrollment['file_name'] = files[0]
for file in files[1:]:
    data = pd.read_csv(file)
    data['file_name'] = file
    df_enrollment = pd.concat([df_enrollment, data], ignore_index=True)

# Shape of the final dataframe
df_enrollment.shape














# renaming all the columns in the dataframe
rename_dict = {
    'Unnamed: 0'                        : 'file_index',
    'Stu Term'                          : 'reg_term_code',
    'Unnamed: 1'                        : 'reg_term_desc',
    'Stu Admit Term'                    : 'stu_admit_term_code',
    'Unnamed: 3'                        : 'stu_admit_term_desc',
    'Record ID'                         : 'stu_id',
    'Stu Visa Type'                     : 'stu_visa',
    'Stu Attribute BAM'                 : 'stu_bam',
    'Stu Admit Type'                    : 'stu_prog_level',
    'Stu Primary Degree Level'          : 'stu_deg_level',
    'Stu Primary Major 1 College'       : 'stu_college',
    'Stu Primary Program'               : 'stu_prog_desc',
    'Stu Primary Program Code'          : 'stu_prog_code',
    'Stu Primary Department'            : 'stu_dept',
    'Unnamed: 14'                       : 'stu_dept_desc',
    'Stu New/Returning Ind'             : 'stu_new_ret',
    'Stu Residency Group'               : 'stu_res',
    'Course Sect College'               : 'crs_sect_clg',
    'Stu Registered Ind'                : 'stu_act_reg_ind',
    'Registration Status'               : 'reg_status',
    'Registration Status Date'          : 'reg_status_date',
    'Course Desc'                       : 'crs',
    'Course Section'                    : 'crs_sect',
    'Course Sect Schedule Type'         : 'crs_type',
    'Course Sect Wiley Courses Ind'     : 'crs_sect_wiley_ind',
    'Course Sect Credits'               : 'crs_credits',
    'Stu Course Registered Hours'       : 'crs_hours',
    'Course Sect Instruction Delivery Method Group' : 'crs_sect_modality',
}
df_enrollment.rename(columns=rename_dict, inplace=True)








# Extracting features from the dataframe

# splitting the "reg_term_desc" column into term and year
df_enrollment['reg_term_name'] = df_enrollment['reg_term_desc'].str.split(' ').str[0]
df_enrollment['reg_term_year'] = df_enrollment['reg_term_desc'].str.split(' ').str[1]
# splitting the "stu_admit_term_desc" column into term and year
df_enrollment['stu_admit_term_name'] = df_enrollment['stu_admit_term_desc'].str.split(' ').str[0]
df_enrollment['stu_admit_term_year'] = df_enrollment['stu_admit_term_desc'].str.split(' ').str[1]

# storing the Record Extraction Date from the "file_name" column
df_enrollment['rec_ext_date'] = df_enrollment['file_name'].str.split("_").str[-2]
df_enrollment['rec_ext_date'] = df_enrollment['rec_ext_date'].str.replace(".", "/", regex=False)








# Cleaning the data

df_enrollment['stu_id'].dropna(inplace=True)
df_enrollment['stu_visa'].fillna("Not Relevent", inplace=True)

df_enrollment['stu_bam'].replace("'--", "Not BAM", inplace=True)
df_enrollment['stu_dept'].replace("'-----", "No Value", inplace=True)
df_enrollment['crs_sect_wiley_ind'].replace("'--", "No Value", inplace=True)

df_enrollment['crs_credits'] = df_enrollment['crs_credits'].astype(str)

df_enrollment['crs_credits'].replace("6-Jan", "1-6", inplace=True)
df_enrollment['crs_credits'].replace("3-Jan", "1-3", inplace=True)
df_enrollment['crs_credits'].replace("18-Jan", "1-18", inplace=True)
df_enrollment['crs_credits'].replace("4-Jan", "1-4", inplace=True)
df_enrollment['crs_credits'].replace("0,3", "0-3", inplace=True)














# sorting the dataframe by term code and registration status date
df_enrollment.sort_values(
    by=['reg_term_code', 'rec_ext_date', 'reg_status_date'], inplace=True
)

# resetting the index after sorting
df_enrollment.reset_index(drop=True, inplace=True)

# creating a new rec_id column for identifying each record
df_enrollment['rec_id'] = df_enrollment.index










# Changing the data type of the columns
df_enrollment['rec_ext_date']           = pd.to_datetime(df_enrollment['rec_ext_date'])
df_enrollment['reg_term_code']          = df_enrollment['reg_term_code'].astype(str)
df_enrollment['reg_term_year']          = df_enrollment['reg_term_year'].astype(int)
df_enrollment['reg_term_name']          = df_enrollment['reg_term_name'].astype('category')
df_enrollment['stu_new_ret']            = df_enrollment['stu_new_ret'].astype('category')
df_enrollment['stu_deg_level']          = df_enrollment['stu_deg_level'].astype('category')
df_enrollment['stu_college']            = df_enrollment['stu_college'].astype('category')
df_enrollment['stu_prog_desc']          = df_enrollment['stu_prog_desc'].astype('category')
df_enrollment['stu_prog_level']         = df_enrollment['stu_prog_level'].astype('category')
df_enrollment['stu_dept']               = df_enrollment['stu_dept'].astype('category')
df_enrollment['stu_dept_desc']          = df_enrollment['stu_dept_desc'].astype('category')
df_enrollment['stu_admit_term_code']    = df_enrollment['stu_admit_term_code'].astype(str)
df_enrollment['stu_admit_term_year']    = df_enrollment['stu_admit_term_year'].astype(int)
df_enrollment['stu_admit_term_name']    = df_enrollment['stu_admit_term_name'].astype('category')
df_enrollment['stu_res']                = df_enrollment['stu_res'].astype('category')
df_enrollment['stu_visa']               = df_enrollment['stu_visa'].astype('category')
df_enrollment['stu_bam']                = df_enrollment['stu_bam'].astype('category')
df_enrollment['crs_sect_clg']           = df_enrollment['crs_sect_clg'].astype('category')
df_enrollment['crs_type']               = df_enrollment['crs_type'].astype('category')
df_enrollment['crs_sect_modality']      = df_enrollment['crs_sect_modality'].astype('category')
df_enrollment['crs_sect_wiley_ind']     = df_enrollment['crs_sect_wiley_ind'].astype('category')
df_enrollment['crs_credits']            = df_enrollment['crs_credits'].astype('category')
df_enrollment['crs_hours']              = df_enrollment['crs_hours'].astype('category')
df_enrollment['stu_act_reg_ind']        = df_enrollment['stu_act_reg_ind'].astype('category')
df_enrollment['reg_status']             = df_enrollment['reg_status'].astype('category')
df_enrollment['reg_status_date']        = pd.to_datetime(df_enrollment['reg_status_date'])













# reordering the columns
df_enrollment = df_enrollment[[
    # Records Info
    'rec_id', 'rec_ext_date', 'file_name', 'file_index',
    # Registration Term/Semester Info
    'reg_term_code', 'reg_term_year', 'reg_term_name', 'reg_term_desc',
    # Student Info
    'stu_id', 'stu_deg_level', 'stu_college', 'stu_res', 'stu_visa', 'stu_bam', 'stu_new_ret',
    'stu_dept', 'stu_dept_desc', 'stu_prog_code', 'stu_prog_level', 'stu_prog_desc',
    'stu_admit_term_code', 'stu_admit_term_year', 'stu_admit_term_name', 'stu_admit_term_desc',
    # Course Info
    'crs', 'crs_type', 'crs_credits', 'crs_hours',
    'crs_sect', 'crs_sect_clg', 'crs_sect_modality', 'crs_sect_wiley_ind',
    # Registration Status Info
    'reg_status', 'reg_status_date', 'stu_act_reg_ind'
]]














# Saving the dataframe as a pickle file
df_enrollment.to_pickle(
    os.path.join("Data", "02_processed", "enrollment.pkl")
)

# Saving the dataframe to a csv file
df_enrollment.to_csv(
    os.path.join("Data", "02_processed", "enrollment.csv"), index=False
)

# Saving the dataframe to a new sqlite database
db_enrollment4EDA = ConnectDB(
    os.path.join("Data", "02_processed", "enrollment4EDA.db")
)
df_enrollment.to_sql('enrollment4EDA', db_enrollment4EDA.connection, if_exists='replace', index=False)
db_enrollment4EDA.commitDB()