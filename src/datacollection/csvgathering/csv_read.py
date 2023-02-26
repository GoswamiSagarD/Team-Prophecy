import pandas as pd
import os
import re
#import jproperties
#from graph_onedrive import OneDriveManager


#configs = jproperties.Properties()

#with open('onedrive.properties', 'rb') as onedrive_prop:
#    configs.load(onedrive_prop)

def initializeCSVFiles():
    print("Initializing our CSV Files listed via API.")
    #This will be for later. We need to get the api keys from the professor first.
    """
    print("-> NOTE: If we cannot get to our file, we will use the reference file within our raw file.")
    #First, let's authenticate our onedrive-sharepoint info.
    session = None
    try:
        print("Beginning recent onedrive reading...")
        session = OneDriveManager()
        files = session.get_files()
        print("Retrieved all files")
    except:
        print("Could not grab; moving on with raw file")
    """
    #May want to replace pandas with something more manageable.
    raw = pd.read_csv(os.getcwd() + os.sep + "Data" + os.sep + "enrollment_data" + os.sep + "01_raw" + os.sep + "CombinedData.csv")
    filered_columns = [
        'Index', 'DataExtractionDate', 'Unnamed: 1', 'Unnamed: 3', 'Record ID',
        'Stu Visa Type', 'Stu Primary Program', 'Stu New/Returning Ind',
        'Stu Residency Group', 'Course Sect College', 'Stu Registered Ind',
        'Registration Status', 'Registration Status Date', 'Course Desc',
        'Course Section', 'Course Sect Schedule Type',
        'Course Sect Instruction Delivery Method Group', 'Course Sect Wiley Courses Ind',
        'Course Sect Credits', 'Stu Course Registered Hours'
    ]
    df = raw[filered_columns]
    df.rename(columns={
        'Index': 'index',
        'DataExtractionDate': 'data_extraction_date',
        'Unnamed: 1': 'registration_term',
        'Unnamed: 3': 'admission_term',
        'Record ID': 'student_id',
        'Stu Visa Type': 'visa_type',
        'Stu Primary Program': 'program',
        'Stu New/Returning Ind': 'new_returning',
        'Stu Residency Group': 'residency',
        'Course Sect College': 'college',
        'Stu Registered Ind': 'active_registration',
        'Registration Status': 'registration_status',
        'Registration Status Date': 'registration_status_date',
        'Course Desc': 'course',
        'Course Section': 'section',
        'Course Sect Schedule Type': 'schedule',
        'Course Sect Instruction Delivery Method Group': 'instruction_delivery',
        'Course Sect Wiley Courses Ind': 'wiley_courses',
        'Course Sect Credits': 'credits',
        'Stu Course Registered Hours': 'registered_hours'
    }, inplace=True)

    df['visa_type'].fillna('Unknown', inplace=True)
    df['data_extraction_date'] = pd.to_datetime(df['data_extraction_date'])
    df['visa_type'] = df['visa_type'].astype(str)
    df['program'] = df['program'].astype(str)
    df['new_returning'] = df['new_returning'].astype(str)
    df['residency'] = df['residency'].astype(str)
    df['college'] = df['college'].astype(str)
    df['active_registration'] = df['active_registration'].astype(str)
    df['registration_status'] = df['registration_status'].astype(str)
    df['registration_status_date'] = pd.to_datetime(df['registration_status_date'])
    df['schedule'] = df['schedule'].astype(str)
    df['instruction_delivery'] = df['instruction_delivery'].astype(str)
    df['wiley_courses'] = df['wiley_courses'].astype(str)
    df = df[df['credits'].str.extract(r"(^[0-9]$)")]
    df = df[~df['credits'].isna()]
    df['credits'] = df['credits'].astype(int)
    df['registered_hours'] = df['registered_hours'].astype(int)

    df = df[df.isnull().any(1)]

    df.groupby(["program"])


    print("Completed csv associated.")




