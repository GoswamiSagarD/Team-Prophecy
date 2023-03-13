# importing the required libraries
import os
import pandas as pd
import matplotlib.pyplot as plt

# os.chdir( os.path.join("..", "..", "..") )

from Code.src.modules.db_ops import *

def buildFinalEnrollStatusData():
    print("#"*40, "\t", "\n", "Final Enrollment Status Data")

    # Importing the data
    print("Importing the required datasets.. [1/3]")
    db_enrollment = ConnectDB( os.path.join("Data", "02_processed", "enrollment4EDA.db") )
    df_enrollment = pd.read_pickle( os.path.join("Data", "02_processed", "enrollment.pkl") )

    # ## Final Enrollment Status of all Students throughout his/her time at the University
    print("Building the final enrollment status of all students.. [2/3]")
    df_enrollmentFinalStatus = db_enrollment.runQuery("""
        SELECT rec_id, reg_term_code, reg_term_desc, stu_id, crs, MAX(reg_status_date) as final_reg_date, reg_status
        FROM enrollment4EDA
        GROUP BY reg_term_code, reg_term_desc, stu_id, crs
        ORDER BY final_reg_date;
    """)

    df_enrollmentFinalStatus = df_enrollment[df_enrollment["rec_id"].isin(df_enrollmentFinalStatus["rec_id"])]

    # Exporting the final status of the students
    print("Exporting the final enrollment status of all students.. [3/3]")
    df_enrollmentFinalStatus.to_csv( os.path.join("Data", "02_processed", "enrollmentFinalStatus.csv"), index=False )
    df_enrollmentFinalStatus.to_pickle( os.path.join("Data", "02_processed", "enrollmentFinalStatus.pkl") )

    db_enrollmentFinalStatus = ConnectDB( os.path.join("Data", "02_processed", "enrollmentFinalStatus.db") )
    df_enrollmentFinalStatus.to_sql("enrollmentFinalStatus", db_enrollmentFinalStatus.connection, if_exists="replace", index=False)

    print("Final Enrollment Status Data is ready for EDA!")