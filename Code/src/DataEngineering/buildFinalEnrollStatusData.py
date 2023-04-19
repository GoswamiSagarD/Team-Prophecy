# importing the required libraries
import os
import pandas as pd
import matplotlib.pyplot as plt

from Code.src.modules.db_ops import *

# So the thing with extracting the final enrollment status is that it is not as simple as it seems.
# The data isn't granular enough and isn't recorded at frequent intervals. For example, the last two snapshots for Spring Semesters are Jan-15 and Feb-01.
# 1.    There are a lot of enrollments after Jan-15, thus those records aren't avaialable in the Jan-15 snapshot.
# 2.    The waitlists are cleared on around Jan-28,29. Thus, the waitlisted records are not available in the Feb-01 snapshot.
# 3.    There were discussions to combine the two snapshots, but it got so misleading that it was decided to not do that.
# 4.    Moreover, students registered for a lot of courses initially, but later no records were available that indivated, if they dropped the course or not.
# 5.    To add to the confusion, the number of registerations for international students were nowhere close to 3*N_IntlStu, indicating a lot of missing records.
# 6.    We asked if we can have more granular data, to see what is happening between these snapshots, but extracting the data is a manual process, and it was not feasible to do that.
# Thus, we decided to take the last record of each student for each course. We still had fewer than expected records, but it was the best we could do.
# If we do not have exact enrollment data, the second best thing to do is to extract student preference for courses. 
# It is still not as good as having the exact enrollment data, but it is better than using just Final Snapshots, or getting more snapshots.

# TIPS for the next team:
# -     We have the code for both the approaches, so if in future the next team wants to use Final Snapshots, they can simply rerun the code on updated data.
# -     If you are assigned to this project, figure out a way to ask for more granular data. Microstrategy is a confidential tool, but if there is a way to work with Enrollment Managemeent, push for it.
# -     We have completely focused our attention on the technique, than the data. We are assuming that the data situation might improve in the future, if not your team, maybe the team after you might have it.
# -     Look out for more tips throughout the code, we have left plenty of them.


def buildFinalEnrollStatusData():
    print("#"*40, "\t", "\n", "Final Enrollment Status Data")

    # Importing the data
    print("Importing the required datasets.. [1/3]")
    db_CECData = ConnectDB( os.path.join("Data", "02_processed", "CECData.db") )
    df_enrollment = pd.read_pickle( os.path.join("Data", "02_processed", "enrollment.pkl") )

    # ## Final Enrollment Status of all Students throughout his/her time at the University
    print("Building the final enrollment status of all students.. [2/3]")
    df_FinalEnrollRec = db_CECData.runQuery("""
        SELECT rec_id, reg_term_code, reg_term_desc, stu_id, crs_req, crs, MAX(reg_status_date) as final_reg_date, reg_status
        FROM enrollment
        GROUP BY reg_term_code, reg_term_desc, stu_id, crs_req, crs
        ORDER BY final_reg_date;
    """)

    # Adding a column to indicate this is a final record
    df_enrollment['FinalStatus'] = False
    df_enrollment.loc[df_enrollment["rec_id"].isin(df_FinalEnrollRec["rec_id"]), "FinalStatus"] = True
    
    # Extracting the final status of the students in a separate dataframe
    df_enrollmentFinalStatus = df_enrollment[df_enrollment["rec_id"].isin(df_FinalEnrollRec["rec_id"])]

    # Exporting the final status of the students
    print("Exporting the final enrollment status of all students.. [3/3]")
    df_enrollmentFinalStatus.to_csv( os.path.join("Data", "02_processed", "enrollmentFinalStatus.csv"), index=False )
    df_enrollmentFinalStatus.to_pickle( os.path.join("Data", "02_processed", "enrollmentFinalStatus.pkl") )

    df_enrollmentFinalStatus.to_sql("enrollmentFinalStatus", db_CECData.connection, if_exists="replace", index=False)


    # Fetching the latest snapshot of registration data for each semester
    df_enrollmentLatestSnapshot = db_CECData.runQuery(""" --sql
        SELECT *
        FROM enrollment
        WHERE
            rec_ext_date IN (
                SELECT MAX(rec_ext_date) AS LatestSnapshotDate
                FROM enrollment
                GROUP BY reg_term_desc
                ORDER BY reg_term_code)
    """)

    # Exporting the latest snapshot data
    df_enrollmentLatestSnapshot.to_csv( os.path.join('Data', '02_processed', 'enrollmentLatestSnapshot.csv') )
    df_enrollmentLatestSnapshot.to_pickle( os.path.join('Data', '02_processed', 'enrollmentLatestSnapshot.pkl') )

    df_enrollmentLatestSnapshot.to_sql("enrollmentLatestSnapshot", db_CECData.connection, if_exists="replace", index=False)

    print("Final Enrollment Status Data is ready for Analysis!!")
    print("#"*40)