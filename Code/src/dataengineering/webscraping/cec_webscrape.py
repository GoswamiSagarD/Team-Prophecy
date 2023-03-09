import json
import os
import re

import requests

import sqlite3

from bs4 import BeautifulSoup

# CONSTS
connection = sqlite3.connect(os.getcwd() + os.sep + "Data" + os.sep + "01_intermediate" + os.sep + "CourseData" + os.sep + "intermediate.db")
base_catalog = "https://catalog.gmu.edu"
base_masters_url = "https://catalog.gmu.edu/programs/#filter=.filter_23"
base_phd_url = "https://catalog.gmu.edu/programs/#filter=.filter_23&.filter_28"
base_courses_url = "https://catalog.gmu.edu/courses/" #Simply add a catalog code for this, and we're solid.


class CourseInfo:
    #We have REQUIRED PREREQUISITES and RECOMMENDED PREREQUISITES
    def __init__(self, code, program, credits, required_prereq_classes=""): #, recommended_classes=""):
        self.code = code
        self.program = program
        self.credits = int(credits)
        self.required_prereq_classes = required_prereq_classes
        #self.recommended_classes = recommended_classes
    def to_sql_insert(self):
        return tuple((self.code, self.credits))



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
    tables = ["program_info", "course_info", "prerequisite_lookup", "lookup_class_to_course", "requirement_table"]
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
                       "program_name TEXT UNIQUE NOT NULL, "
                       "program_url TEXT NOT NULL, "
                       "program_type TEXT NOT NULL, "
                       "program_school TEXT NOT NULL"
                       ");")
    connection.commit()
    # This will be our courses available
    connection.execute("CREATE TABLE course_info("
                       "course_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "course_name TEXT UNIQUE NOT NULL, "
                       "credits INTEGER NOT NULL"
                       ");")  # if it's not required, it's an elective
    connection.commit()
    # Then, we must list any and all prerequisites of a course within the database below
    # -> is_parent is basically asking "Is this the earliest version of pre-requisites we can find?"
    # -> is_last is asking "Is this the last known version of our lookup?"
    # -> We need the pre-req to identify which program it's under, hence program_id_fk
    # -> Prior requirements are not included if they go into the undergraduate level
    # All of this information will be calculated prior before continuing for easy grouping.
    connection.execute("CREATE TABLE prerequisite_lookup("
                       "prereq_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "program_id_fk TEXT NOT NULL, "
                       "course_name_fk TEXT NOT NULL, "
                       "prereq_name_fk TEXT NOT NULL,"
                       "FOREIGN KEY(program_id_fk) REFERENCES program_info(program_id_fk), "
                       "FOREIGN KEY(course_name_fk) REFERENCES course_info(course_name), "
                       "FOREIGN KEY(prereq_name_fk) REFERENCES course_info(course_name)"
                       ");")
    connection.commit()
    # This is going to have a one to many relationship to the class.
    connection.execute("CREATE TABLE lookup_class_to_course("
                       "lookup_ctc_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "program_name_fk TEXT NOT NULL, "
                       "course_name_fk TEXT NOT NULL, "
                       "required_class TEXT NOT NULL, "
                       "FOREIGN KEY(program_name_fk) REFERENCES program_info(program_name), "
                       "FOREIGN KEY(course_name_fk) REFERENCES course_info(course_name)"
                       ");")
    connection.commit()

    connection.execute("CREATE TABLE requirement_table(requirement_id, requirement_type);")
    connection.commit()

    # MUST create triggers after insert under program_info and course_info


def scrape_course_info(program,core_list,masters_obj_dict):
    m_dict = masters_obj_dict #This will include all courses listed.
    selected_course_info = []
    all_course_info = [] #Once we get all of the course information, we want to be notified of it!
    #program_course_link = []
    c_w_prereqs = []
    for course in core_list:
        course_w_no = str(course["href"]).replace("/search/?P=", "").lower().split("%20")
        selected_course_info.append(course_w_no[0].strip() + course_w_no[1].strip())
        courses_found = base_courses_url+course_w_no[0]
        course_w_no[0] = course_w_no[0].upper()
        if course_w_no[0] not in m_dict.keys():
            courses_html = requests.get(courses_found) #Be sure to grab by class courseblocklevel
            course_assess = BeautifulSoup(courses_html.content, 'html.parser')
            m_dict[course_w_no[0]] = {}
            for c_iter in course_assess.find_all("div", {"class":"courseblocklevel"}):
                #spl_iter_text = int(c_iter.get_text().replace("\n","")[:3])
                #if spl_iter_text < 500:
                #    continue
                course_block_iter = c_iter.find_all_next("div", {"class":"courseblock"})
                for cb_iter in course_block_iter:
                    gen_indexing = cb_iter.get_text()
                    class_code = cb_iter.find_next("strong",{"class": "cb_code"}).get_text()[:-1].replace("\xa0","")
                    class_credits = int(re.search(r"([0-9]{1}) credit",gen_indexing).group(0)[:1])
                    if tuple((class_code, class_credits)) in all_course_info:
                        continue
                    #class_desc = cb_iter.find_next("div",{"class": "courseblockdesc"}).get_text()
                    """
                    prereq_recommended = gen_indexing.index("Recommended Prerequisite")
                    class_prereqs_recom = ""
                    if prereq_recommended > -1:
                        class_prereqs_recom = re.search(r"([A-Z]+\s[0-9]{3})",cb_iter.get_text()[prereq_recommended:].split(".")[0])
                    """
                    class_prereqs_needed = []
                    try:
                        prereq_needed = gen_indexing.index("Required Prerequisite")
                        if prereq_needed > -1:
                            class_prereqs_needed = set(re.findall(r"([A-Z]+.[0-9]{3})",cb_iter.get_text()[prereq_needed:].split(".")[0]))
                            class_prereqs_needed = [i.replace("\xa0", "") for i in class_prereqs_needed]
                    except:
                        class_prereqs_needed = []
                    cInfo = CourseInfo(class_code, program, class_credits,class_prereqs_needed) #,class_prereqs_recom)
                    m_dict[course_w_no[0]][cInfo.code] = cInfo
                    all_course_info.append(cInfo.to_sql_insert())
                    #program_course_link.append(tuple((cInfo.program,cInfo.code)))
                    for pr_c in cInfo.required_prereq_classes:
                        c_w_prereqs.append(tuple((cInfo.program,cInfo.code,pr_c)))

            connection.executemany("INSERT INTO course_info(course_name, credits) VALUES(?,?)",all_course_info)
            connection.commit()

            # Prerequisite information
            connection.executemany(
                "INSERT INTO prerequisite_lookup(program_id_fk, course_name_fk, prereq_name_fk) VALUES(?,?,?)",
                c_w_prereqs)
            connection.commit()

            all_course_info = []
            c_w_prereqs = []
    return selected_course_info, m_dict #program_course_link

def programToClasses(program,classes,required,m_dict):
    error_list = []
    program_course_link = []
    for c in classes:
        try:
            p_name = re.search(r"(.*[a-z])", c).group(0).upper()
            cobj = m_dict[p_name][c.upper()]
            program_course_link.append(tuple((program,cobj.code,required)))
        except:
            error_list.append(c)

    connection.executemany("INSERT INTO lookup_class_to_course(program_name_fk, course_name_fk, required_class) VALUES(?,?,?)",
                           program_course_link)
    connection.commit()

    return error_list


def scape_masters_info():
    phd_html_listed = requests.get(base_phd_url)
    masters_html_listed = requests.get(base_masters_url)
    print("Now, we process our masters...")
    if masters_html_listed.status_code != 200:
        print("Could not retrieve list of masters classes")
        return
    if phd_html_listed.status_code != 200:
        print("Could not retrieve list of phd classes")
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
        name = name.replace("-graduate-certificate", "-gc") #.replace("-ms", "")
        school = cert_list[len(cert_list) - 2]
        master_link_dict[i] = ProgramInfo(i, name, m_iter, type, school)
        i += 1
    prog_info_list = [i.to_sql_insert(True) for i in master_link_dict.values()]

    phd_content = str(phd_html_listed.content)
    phd_content_list = re.findall(r"(\/colleges-schools\/.+?(?=\"))", phd_content)[1:]
    print("Phd Content List will now be filtered.")
    phd_content_list = [p_iter for p_iter in phd_content_list if ("-phd" in p_iter)]
    phd_link_dict = {}
    # Now that we have all values listed, we should rework them so that they can be handled
    for p_iter in phd_content_list:
        cert_list = p_iter.split("/")
        cert_list = cert_list[1:len(cert_list) - 1]
        name = cert_list[len(cert_list) - 1]
        type = "phd"
        school = cert_list[len(cert_list) - 2]
        phd_link_dict[i] = ProgramInfo(i, name, m_iter, type, school)
        i += 1
    prog_info_list.extend([i.to_sql_insert(True) for i in phd_link_dict.values()])


    #id,name,url,program_type,program_school
    connection.executemany("INSERT INTO program_info VALUES(?,?,?,?,?)", prog_info_list)

    error_list = []
    masters_obj_dict = {} #This handles the extended masters list
    m_vals = master_link_dict.values()
    for m_iter in m_vals:
        masters_url = base_catalog+m_iter.url+"#requirementstext"
        masters_courses_html = requests.get(masters_url)
        if masters_courses_html.status_code != 200:
            print("Could not retrieve list of masters classes")
            continue
        #masters_courses_types_html = str(masters_courses_html.content).replace("\\xc2\\xa0", " ").lower()
        be_assess = BeautifulSoup(masters_courses_html.content,'html.parser')
        #Either it's a required course, or it's not.
        for core_class in be_assess.find_all("h3"):
            if core_class.get_text().lower() == "required courses" or core_class.get_text().lower() == "core courses":
                core_list = core_class.parent.find_all("a",{"class":"bubblelink code"})
                #For any courses that we find, we must add all of them to our database.
                # This is IIF we haven't encountered them prior.. (Likely will need to include courses later)
                selected_classes, extend_map_list = scrape_course_info(m_iter.id,core_list,masters_obj_dict) #master_info,
                masters_obj_dict.update(extend_map_list)
                error_list.extend(programToClasses(m_iter.name,selected_classes,True,masters_obj_dict))
                #core_class.parent.find_all("a", {"class": "bubblelink code"})[0]["onclick"]
            elif core_class.get_text().lower() == "electives":
                elective_list = core_class.parent.find_all("a", {"class": "bubblelink code"})
                selected_classes, extend_map_list = scrape_course_info(m_iter.id, elective_list, masters_obj_dict)  # master_info,
                masters_obj_dict.update(extend_map_list)
                error_list.extend(programToClasses(m_iter.name, selected_classes, False,masters_obj_dict))
        # masters_courses_html_list = re.findall(r"\<a href=\"(\/search\/\?P\=.+?(?=\"))", masters_courses_html)[1:]
        """
        #DEPRECATED CODE; NO LONGER INCLUDING...
        masters_courses_html_list = re.findall(r"\" title=\"(.+?(?=\"))",masters_courses_types_html) #\" class=\"bubblelink code\"
        temp_list = {h_iter for h_iter in masters_courses_html_list if len(h_iter.split(" ")) == 2 and h_iter.split(" ")[1].isdigit()}
        #We want to keep all of the values listed by the course grouping id because even if they aren't immediately used, we can request data on them later
        course_grouping_dict[m_iter.id] = list(temp_list)
        """
    print(error_list)
    #grouping_set = grouping_set.union(set([c[0] for c in course_grouping_dict.values()]))

    #From then on, it's likely best if we handle all Professor variables.


def init():
    print("Initializing our webscraping environment")
    destruct()
    init_create_dbs()
    scape_masters_info()
    #scrape_phd_info()
