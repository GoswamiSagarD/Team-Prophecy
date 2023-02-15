import json
import os
import re

import requests
import sqlite3

# from bs4 import BeautifulSoup

# CONSTS
connection = sqlite3.connect(os.getcwd() + os.sep + "course_info.db")
base_catalog = "https://catalog.gmu.edu"
base_masters_url = "https://catalog.gmu.edu/programs/#filter=.filter_23"
base_phd_url = "https://catalog.gmu.edu/programs/#filter=.filter_23&.filter_28"
base_courses_url = "https://catalog.gmu.edu/courses/" #Simply add a catalog code for this, and we're solid.


class courseInfo:
    #We have REQUIRED PREREQUISITES and RECOMMENDED PREREQUISITES
    def __init__(self, id, name, url, program_name, pre_req_classes=None, recommended_prereqs=None):
        self.id = id
        self.name = name
        self.url = url
        self.program_name = program_name
        self.pre_req_classes = pre_req_classes
        self.recommended_prereqs = recommended_prereqs


class ProgramInfo:
    def __init__(self, id, name, url, program_type, program_school):
        self.id = id
        self.name = name
        self.url = url
        self.program_type = program_type
        self.program_school = program_school

    def to_sql_insert(self, include_id=False):
        if include_id:
            return tuple((int(self.id), self.name, self.url, self.program_type, self.program_school))
        return tuple((self.name, self.url, self.program_type, self.program_school))


def destruct():
    print("Destructing all databases prior to continuing...")
    tables = ["program_info", "course_info", "prerequisite_lookup", "lookup_class_to_course"]
    for table in tables:
        try:
            connection.execute("DROP TABLE " + table)
            connection.commit()
        except:
            print("Could not drop " + table)


def init_create_dbs():
    print("Loading all databases for our venture")
    # This will be our program (program type = phd, masters or graduate cert; program_school = where we are getting the value from)
    connection.execute("CREATE TABLE program_info("
                       "program_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "program_name TEXT NOT NULL, "
                       "program_url TEXT NOT NULL, "
                       "program_type TEXT NOT NULL, "
                       "program_school TEXT NOT NULL"
                       ");")
    connection.commit()
    # This will be our courses available
    connection.execute("CREATE TABLE course_info("
                       "course_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "course_name TEXT NOT NULL"
                       ");")  # if it's not required, it's an elective
    connection.commit()
    # Then, we must list any and all prerequisites of a course within the database below
    # -> is_parent is basically asking "Is this the earliest version of pre-requisites we can find?"
    # -> is_last is asking "Is this the last known version of our lookup?"
    # -> We need the pre-req to identify which program it's under, hence program_id_fk
    # All of this information will be calculated prior before continuing for easy grouping.
    connection.execute("CREATE TABLE prerequisite_lookup("
                       "prereq_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "program_id_fk INTEGER NOT NULL, "
                       "course_id_fk INTEGER NOT NULL, "
                       "course_id_fk_2 INTEGER NOT NULL,"
                       "is_parent INTEGER NOT NULL, "
                       "is_last INTEGER NOT NULL, "
                       "FOREIGN KEY(program_id_fk) REFERENCES program_info(program_id), "
                       "FOREIGN KEY(course_id_fk) REFERENCES course_info(course_id), "
                       "FOREIGN KEY(course_id_fk_2) REFERENCES course_info(course_id)"
                       ");")
    connection.commit()
    # This is going to have a one to many relationship to the class.
    connection.execute("CREATE TABLE lookup_class_to_course("
                       "lookup_ctc_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "program_id_fk INTEGER NOT NULL, "
                       "course_id_fk INTEGER NOT NULL, "
                       "required INTEGER NOT NULL, "
                       "core_class INTEGER NOT NULL, "
                       "FOREIGN KEY(program_id_fk) REFERENCES program_info(program_id), "
                       "FOREIGN KEY(course_id_fk) REFERENCES course_info(course_id)"
                       ");")
    connection.commit()
    # MUST create triggers after insert under program_info and course_info


def scape_masters_info():
    masters_html_listed = requests.get(base_masters_url)
    print("Now, we process our masters...")
    if masters_html_listed.status_code != 200:
        print("Could not retrieve list of masters classes")
        return
    # Match using this: (\/colleges-schools\/.+?(?=\")) for masters
    masters_content = str(masters_html_listed.content)
    masters_content_list = re.findall(r"(\/colleges-schools\/.+?(?=\"))", masters_content)[1:]
    print("Masters Content List will now be filtered.")
    masters_content_list = [m_iter for m_iter in masters_content_list if
                            ("-graduate-certificate" in m_iter or "-ms" in m_iter)]
    print(masters_content_list)
    master_link_dict = {}
    i = 1;  # This will be our temporary auto-increment value
    # Now that we have all values listed, we should rework them so that they can be handled
    for m_iter in masters_content_list:
        cert_list = m_iter.split("/")
        cert_list = cert_list[1:len(cert_list)-1]
        name = cert_list[len(cert_list) - 1]
        type = "graduate-certificate" if "graduate-certificate" in name else "ms"
        name = name.replace("-graduate-certificate", "").replace("-ms", "")
        school = cert_list[len(cert_list) - 2]
        master_link_dict[i] = ProgramInfo(i, name, m_iter, type, school)
        i += 1
    prog_info_list = [i.to_sql_insert(True) for i in master_link_dict.values()]

    #id,name,url,program_type,program_school
    connection.executemany("INSERT INTO program_info VALUES(?,?,?,?,?)", prog_info_list)

    course_grouping_dict = {}  # This course group is going to have the masters as it's key, and then the physical names of all courses prior to continuing.
    grouping_set = set()
    m_vals = master_link_dict.values()
    base_json_dir = os.getcwd()+os.sep+"json"+os.sep
    if "master_classes.json" in os.listdir(base_json_dir):
        course_grouping_dict = dict(json.load(base_json_dir + "course_grouping.json"))
        grouping_set = set([h_iter.split(" ")[0].lower() for h_iter in course_grouping_dict.values()])
    else:
        for m_iter in m_vals:
            masters_courses_html = requests.get(base_catalog+m_iter.url+"#requirementstext")
            if masters_courses_html.status_code != 200:
                print("Could not retrieve list of masters classes")
                continue
            masters_courses_types_html = str(masters_courses_html.content).replace("\\xc2\\xa0", " ").lower()
            # masters_courses_html_list = re.findall(r"\<a href=\"(\/search\/\?P\=.+?(?=\"))", masters_courses_html)[1:]
            masters_courses_html_list = re.findall(r"\" title=\"(.+?(?=\"))",masters_courses_types_html) #\" class=\"bubblelink code\"
            temp_list = {h_iter for h_iter in masters_courses_html_list if len(h_iter.split(" ")) == 2 and h_iter.split(" ")[1].isdigit()}
            course_grouping_dict[m_iter.id] = list(temp_list)
        with open(base_json_dir+"course_grouping.json", 'w+', encoding="utf8") as jf:
            json.dump(course_grouping_dict, jf)
            #grouping_set = grouping_set.union(set([c[0] for c in course_grouping_dict.values()]))

    print("Now that we have all of our course information for each masters, " +
          "we just have to make the connection between the masters list and courses list")

    i = 1

    # From there, we have to regex the information that we see.


def scrape_phd_info():
    phd_html_listed = requests.get(base_phd_url)


def init():
    print("Initializing our webscraping environment")
    destruct()
    init_create_dbs()
    scape_masters_info()
    #scrape_phd_info()


def select_masters_cec_website(filter):
    print("Selecting values from our program...")
