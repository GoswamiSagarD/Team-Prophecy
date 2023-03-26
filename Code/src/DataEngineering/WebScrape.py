#!/usr/bin/env python
# coding: utf-8

# In[208]:


import json
import os
import re

import requests

import sqlite3

from bs4 import BeautifulSoup


# In[209]:


process_path = os.path.join(os.sep+"home"+os.sep+"jupyter"+os.sep+"Team-Prophecy","Data","02_processed","intermediate.db")
print(process_path)


# In[210]:


raw_path = os.path.join(os.sep+"home"+os.sep+"jupyter"+os.sep+"Team-Prophecy","Data","01_raw","CourseData","raw.db")
print(raw_path)


# In[211]:


raw_connection = sqlite3.connect(raw_path)


# In[212]:


process_connection = sqlite3.connect(process_path)


# In[213]:


base_catalog = "https://catalog.gmu.edu"
base_masters_url = "https://catalog.gmu.edu/programs/#filter=.filter_23"
#base_phd_url = "https://catalog.gmu.edu/programs/#filter=.filter_23&.filter_28"
base_courses_url = "https://catalog.gmu.edu/courses/" 

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
    def to_sql_insert_program_code_key(self):
        return tuple((self.program, self.code))


class ProgramInfo:
    def __init__(self, name, url, program_type):
        self.name = name
        self.url = url
        self.program_type = program_type #i.e. masters/phd

    def to_sql_insert(self):
        return tuple((self.name, self.url, self.program_type))



masters_html_listed = requests.get(base_masters_url)
print("Now, we process our masters...")
masters_content = None
if masters_html_listed.status_code != 200:
    print("Could not retrieve list of masters classes")
    exit()
# Match using this: (\/colleges-schools\/.+?(?=\")) for masters
masters_content = str(masters_html_listed.content)
masters_content_list = re.findall(r"(\/colleges-schools\/.+?(?=\"))", masters_content)[1:]
print("Masters Content List will now be filtered.")

masters_content_list = [m_iter for m_iter in masters_content_list if
                            ("-graduate-certificate" in m_iter or "-ms" in m_iter or "-phd" in m_iter)]



#print(masters_content_list)


# We must now declare all values under our colleges, departments, and degree levels so that we can later use them as referential variables

process_connection.executemany("INSERT INTO degree_level(deg_name) VALUES(?)", [("gc",),("ms",),("phd",)])
process_connection.commit()

master_link_dict = {}
i = 1;  # This will be our temporary auto-increment value
# Now that we have all values listed, we should rework them so that they can be handled
for m_iter in masters_content_list:
    cert_list = m_iter.split("/")
    cert_list = cert_list[1:len(cert_list)-1]
    name = cert_list[len(cert_list) - 1]
    if "graduate-certificate" in name:
        type = "graduate-certificate"
        name = name.replace("-graduate-certificate", "-gc")  # .replace("-ms", "")
    elif "phd" in name:
        type = "phd"
    else:
        type = "ms" #Should be 
    if name in master_link_dict.keys():
        continue
    #school = cert_list[len(cert_list) - 2]
    master_link_dict[name] = ProgramInfo(name, m_iter, type)
prog_info_list = [i.to_sql_insert() for i in master_link_dict.values()]


raw_connection.executemany("INSERT INTO programs VALUES(?,?,?)", prog_info_list)
raw_connection.commit()


def scrape_course_info(program,core_list,masters_obj_dict):
    m_dict = masters_obj_dict #This will include all courses listed.
    selected_course_info = []
    all_course_info = [] #Once we get all of the course information, we want to be notified of it!
    program_course_link = set()
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
                    program_course_link.add(tuple((cInfo.program,cInfo.code)))
                    m_dict[course_w_no[0]][cInfo.code] = cInfo
                    all_course_info.append(cInfo.to_sql_insert())
                    for pr_c in cInfo.required_prereq_classes:
                        c_w_prereqs.append(tuple((cInfo.code,pr_c)))

            raw_connection.executemany("INSERT INTO courses(crs_name, crs_credits) VALUES(?,?)",all_course_info)
            raw_connection.commit()
            
            program_course_arr = list(program_course_link)
            #print("\n".join(str(i) for i in program_course_arr))
            raw_connection.executemany("INSERT INTO program_course_offerings(prog_code, crs_id) VALUES(?,?)",program_course_arr)
            raw_connection.commit()

            # Prerequisite information
            process_connection.executemany(
                "INSERT INTO course_prerequisite(crs, crs_prereq) VALUES(?,?)",
                c_w_prereqs)
            process_connection.commit()

            all_course_info = []
            c_w_prereqs = []
    return selected_course_info, m_dict #program_course_link


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
            selected_classes, extend_map_list = scrape_course_info(m_iter.name,core_list,masters_obj_dict) #master_info,
            masters_obj_dict.update(extend_map_list)
            #core_class.parent.find_all("a", {"class": "bubblelink code"})[0]["onclick"]
        elif core_class.get_text().lower() == "electives":
            elective_list = core_class.parent.find_all("a", {"class": "bubblelink code"})
            selected_classes, extend_map_list = scrape_course_info(m_iter.name, elective_list, masters_obj_dict)  # master_info,
            masters_obj_dict.update(extend_map_list)

