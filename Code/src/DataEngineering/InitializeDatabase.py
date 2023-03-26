#!/usr/bin/env python
# coding: utf-8

# In[106]:


import os

import sqlite3


# In[107]:


process_path = os.path.join(os.sep+"home"+os.sep+"jupyter"+os.sep+"Team-Prophecy","Data","02_processed","intermediate.db")
connection_process = sqlite3.connect(process_path)


# In[108]:


print(process_path)


# In[109]:


raw_path = os.path.join(os.sep+"home"+os.sep+"jupyter"+os.sep+"Team-Prophecy","Data","01_raw","CourseData","raw.db")
connection_raw = sqlite3.connect(raw_path)


# In[110]:


print(raw_path)


# EXECUTE TO DESTRUCT EVERYTHING

# In[36]:


chittyChittyBangBang()


# EXECUTE ONLY WHEN READY TO INITIALIZE THE VALUES

# In[111]:


buildInitCreateDBS()


# In[112]:


buildRawDatabaseData()


# In[105]:


#These explicitly avoid foreign keys so that values can be temporarily stored prior to being merged in.
def buildRawDatabaseData():
    print("Beginning creation of the raw database for later convergence...")
    print(" -> This will help create our initial lookup values for the tables we find.")
    connection_raw.execute("CREATE TABLE campus("
                       "campus_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "campus_name TEXT NOT NULL "
                       ");")
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE colleges("
                       "col_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "col_name TEXT NOT NULL "
                       ");")
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE departments("
                       "dept_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "dept_desc TEXT NOT NULL "
                       ");")
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE student_details("
                       "stu_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "stu_admit_term_code TEXT NOT NULL, "
                       "stu_deg_level TEXT NOT NULL, "
                       "stu_college INTEGER NOT NULL, "
                       "stu_dept INTEGER NOT NULL, "
                       "stu_prog INTEGER NOT NULL, "
                       "stu_res TEXT NOT NULL, "
                       "stu_visa TEXT NOT NULL, "
                       "stu_bam TEXT NOT NULL "
                       ");")
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE programs("
                       "prog_code TEXT PRIMARY KEY, "
                       "prog_url TEXT NOT NULL, "
                       "prog_type TEXT NOT NULL "
                       ");")
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE courses("
                       "crs_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "crs_name TEXT NOT NULL, "
                       "crs_credits INTEGER NOT NULL"
                       ");")  # if it's not required, it's an elective
    connection_raw.commit()
    
    connection_raw.execute("CREATE TABLE program_course_offerings("
                       "prog_code TEXT NOT NULL, "
                       "crs_id TEXT NOT NULL "
                       ");")
    connection_raw.commit()

    connection_raw.execute("CREATE TABLE course_section("
                       "crs_id INTEGER NOT NULL, "
                       "sect_id INTEGER NOT NULL, "
                       "sect_clg INTEGER NOT NULL, "
                       "sect_dept INTEGER NOT NULL, "
                       "sect_camp INTEGER NOT NULL, "
                       "sect_mod TEXT NOT NULL, "
                       "sect_status TEXT NOT NULL, "
                       "sect_lvl TEXT NOT NULL, "
                       "sect_instr TEXT NOT NULL, "
                       "sect_wiley TEXT NOT NULL"
                       ");")
    connection_raw.commit()


# In[20]:


def chittyChittyBangBang():
    print("Destructing all databases prior to continuing...")
    proc_tables = ["campus", "colleges", "departments",
              "degree_level", "programs", "courses",
              "course_prerequisite", "semester_course_offerings",
              "program_course_offerings", "term", "student_details",
              "course_section", "registration_status", "registration_log",
              "resultant_values"]
    raw_tables = ["campus","colleges","departments","course_section",
                 "student_details"]
    for table in proc_tables:
        try:
            connection_process.execute("DROP TABLE " + table)
            connection_process.commit()
        except:
            print("Could not drop processed table " + table)
    for table in raw_tables:
        try:
            connection_raw.execute("DROP TABLE " + table)
            connection_raw.commit()
        except:
            print("Could nto drop raw table " + table)


# In[87]:


def buildInitCreateDBS():
    #chittyChittyBangBang()
    print("Loading all databases for our venture")
    # Initializes the campus, colleges, and department tables.
    # -> Campus have multiple colleges
    # -> Colleges have multiple departments
    # -> Departments have multiple courses
    connection_process.execute("CREATE TABLE campus("
                       "campus_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "campus_name TEXT NOT NULL "
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE colleges("
                       "col_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "col_name TEXT NOT NULL, "
                       "campus_id_fk TEXT NOT NULL, "
                       "FOREIGN KEY(campus_id_fk) REFERENCES campus(campus_id)"
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE departments("
                       "dept_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "dept_desc TEXT NOT NULL, "
                       "col_id_fk INTEGER NOT NULL, "
                       "FOREIGN KEY(col_id_fk) REFERENCES colleges(col_id)"
                       ");")
    connection_process.commit()

    #Next, we have to get degree_level
    connection_process.execute("CREATE TABLE degree_level("
                       "deg_level INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "deg_name TEXT NOT NULL"
                       ");")
    connection_process.commit()
    #Then, we get into Programs

    connection_process.execute("CREATE TABLE programs("
                       "prog_code TEXT PRIMARY KEY, "
                       "prog_url TEXT NOT NULL, "
                       "prog_type TEXT NOT NULL, "
                       "prog_clg INTEGER NOT NULL, "
                       "prog_lvl TEXT NOT NULL"
                       ");")
    connection_process.commit()
    # This will be our courses available
    connection_process.execute("CREATE TABLE courses("
                       "crs_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "crs_name TEXT NOT NULL, "
                       "dept_type TEXT NOT NULL, "
                       "crs_credits INTEGER NOT NULL"
                       ");")  # if it's not required, it's an elective
    connection_process.commit()

    # All of this information will be calculated prior before continuing for easy grouping.
    connection_process.execute("CREATE TABLE course_prerequisite("
                       "prereq_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "crs INTEGER NOT NULL, "
                       "crs_prereq INTEGER NOT NULL,"
                       "FOREIGN KEY(crs) REFERENCES courses(crs_id)"
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE semester_course_offerings("
                       "cum_id INTEGER UNIQUE NOT NULL DEFAULT 0, "
                       "cum_term_code TEXT UNIQUE NOT NULL, "
                       "cum_sect_id TEXT UNIQUE NOT NULL, "
                       "cum_seat_enroll INTEGER NOT NULL, "
                       "cum_seat_wait INTEGER NOT NULL DEFAULT 0, "
                       "cum_seat_avail INTEGER NOT NULL DEFAULT 0, "
                       "CONSTRAINT course_section_pk PRIMARY KEY (cum_term_code, cum_sect_id)"
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE program_course_offerings("
                       "prog_code TEXT NOT NULL, "
                       "crs_id TEXT NOT NULL, "
                       "CONSTRAINT prog_req_pk PRIMARY KEY (prog_code, crs_id) "
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE term("
                       "term_code TEXT PRIMARY KEY, "
                       "term_year TEXT NOT NULL, "
                       "term_name TEXT NOT NULL, "
                       "term_desc TEXT NOT NULL "
                       ");")

    connection_process.execute("CREATE TABLE student_details("
                       "stu_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "stu_admit_term_code TEXT NOT NULL, "
                       "stu_deg_level TEXT NOT NULL, "
                       "stu_college INTEGER NOT NULL, "
                       "stu_dept INTEGER NOT NULL, "
                       "stu_prog INTEGER NOT NULL, "
                       "stu_res TEXT NOT NULL, "
                       "stu_visa TEXT NOT NULL, "
                       "stu_bam TEXT NOT NULL, "
                       "FOREIGN KEY(stu_admit_term_code) REFERENCES term(term_code), "
                       "FOREIGN KEY(stu_deg_level) REFERENCES degree_level(deg_level), "
                       "FOREIGN KEY(stu_college) REFERENCES colleges(col_id), "
                       "FOREIGN KEY(stu_dept) REFERENCES departments(dept_id),"
                       "FOREIGN KEY(stu_prog) REFERENCES programs(prog_code) "
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE course_section("
                       "crs_id INTEGER NOT NULL, "
                       "sect_id INTEGER NOT NULL, "
                       "sect_clg INTEGER NOT NULL, "
                       "sect_dept INTEGER NOT NULL, "
                       "sect_camp INTEGER NOT NULL, "
                       "sect_mod TEXT NOT NULL, "
                       "sect_status TEXT NOT NULL, "
                       "sect_lvl TEXT NOT NULL, "
                       "sect_instr TEXT NOT NULL, "
                       "sect_wiley TEXT NOT NULL,"
                       "CONSTRAINT course_section_pk PRIMARY KEY (crs_id, sect_id), "
                       "FOREIGN KEY(sect_clg) REFERENCES colleges(col_id), "
                       "FOREIGN KEY(sect_dept) REFERENCES departments(dept_id), "
                       "FOREIGN KEY(sect_camp) REFERENCES campus(camp_id), "
                       "FOREIGN KEY(sect_instr) REFERENCES instructors(instr_name) "
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE registration_status("
                       "reg_id INTEGER UNIQUE NOT NULL DEFAULT 0, "
                       "reg_term_code TEXT NOT NULL, "
                       "reg_stu_id INTEGER NOT NULL, "
                       "sect_id INTEGER NOT NULL, "
                       "reg_status_date TEXT NOT NULL, "
                       "reg_final_status TEXT NOT NULL, "
                       "reg_sect_reg_ind INTEGER NOT NULL, "
                       "reg_new_ret_stu INTEGER NOT NULL, "
                       "CONSTRAINT registration_status_pk PRIMARY KEY(reg_term_code, reg_stu_id, sect_id) "
                       ");")
    connection_process.commit()

    connection_process.execute("CREATE TABLE registration_log("
                       "rec_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "reg_id INTEGER NOT NULL, "
                       "rec_ext_Date INTEGER NOT NULL, "
                       "file_name TEXT NOT NULL, "
                       "file_index INTEGER NOT NULL "
                       ");")
    connection_process.commit()

    #THIS IS EXPLICITLY FOR OUR RESULTANT_VALUES
    connection_process.execute("CREATE TABLE resultant_values("
                       "result_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "crs_name TEXT NOT NULL, "
                       "crs_sect_id INTEGER NOT NULL, "
                       "available_seats INTEGER NOT NULL DEFAULT 0 "
                       ");")
    connection_process.commit()

    # MUST create triggers after insert under program_info and course_info

