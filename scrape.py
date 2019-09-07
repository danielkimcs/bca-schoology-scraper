import re
import time
import pickle
from bs4 import BeautifulSoup

from robobrowser import RoboBrowser

br = RoboBrowser()
br.open("https://bca.schoology.com/login/ldap?destination=home&school=11897239")
form = br.get_form(id="s-user-login-form")
form['mail'] = ''  # Username
form['pass'] = ''  # Password
br.submit_form(form)

# course_id_dict = {}
# student_dict = {}


def get_name_and_courses(user_id):
    """
    Returns 2-tuple: (name, courses) where:
        name = a string containing user's name
        courses = a list of course names of user
    """
    soup = BeautifulSoup(br.session.get(
        "https://bca.schoology.com/user/"+str(user_id)+"/courses/list").text, 'html.parser')

    item_names = soup.select('.course-item-right')
    courses = []
    for item in item_names:
        course_link = item.select('a')[0].attrs['href']
        course_id = int(course_link[8:])
        course_name = item.get_text()
        if course_id not in course_id_dict.keys():
            course_id_dict[course_id] = course_name
        courses.append(course_id)

    soup2 = BeautifulSoup(br.session.get(
        "https://bca.schoology.com/user/"+str(user_id)+"/info").text, 'html.parser')

    name = soup2.select("#center-top .page-title")[0].get_text()
    if (len(soup2.select("span.admin-val.email")) > 0):
        email = soup2.select("span.admin-val.email")[0].get_text()
        if "20@bergen.org" not in email:
            return None
    return name, courses


def isStudent(user_id):
    """
    Verifies if given user_id is a current senior
    """
    soup = BeautifulSoup(br.session.get(
        "https://bca.schoology.com/user/"+str(user_id)+"/info").text, 'html.parser')
    if (len(soup.select("span.admin-val.email")) > 0):
        email = soup.select("span.admin-val.email")[0].get_text()
        if "20@bergen.org" not in email:
            return False
    return True


def print_tuple(user_tuple):
    print("Name: "+user_tuple[0])
    print("Current classes:")
    for course in user_tuple[1]:
        print(course)


def get_senior_ids():
    """
    Gets all senior user_ids from the BCA-2020 group page on Schoology, excludes administrators/teachers.
    Also includes students who have dropped out.
    """
    ids = []
    current_url = "https://bca.schoology.com/enrollments/edit/members/group/772763961/ajax?ss=&p="
    page = 1
    soup = BeautifulSoup(br.session.get(
        current_url+str(page)).text, 'html.parser')
    while (len(soup.select("tbody")) > 0):
        for user in soup.select("tbody")[0].select("tr"):
            time.sleep(0.25)
            cur_id = int(user.get("id"))
            if (isStudent(cur_id)):
                ids.append(cur_id)
        page += 1
        soup = BeautifulSoup(br.session.get(
            current_url+str(page)).text, 'html.parser')
    return ids


def str_cmp(a):
    return course_id_dict[a]


def generate_classes_list():
    """
    Generates list of senior students for every possible class,
    stores it in classes.txt.
    """
    course_dict = {}
    for uid in uids:
        student = student_dict[uid]
        name = student[0]
        courses = student[1]
        for c in courses:
            if c not in course_dict.keys():
                course_dict[c] = {name}
            else:
                course_dict[c].add(name)

    cur_file = open("classes.txt", "w")
    for c in sorted(course_dict, key=str_cmp):
        cur_file.write(course_id_dict[c]+"\n\n")
        cur_file.write("Teachers:\n")
        if c not in course_teacher_dict.keys():
            cur_file.write("UNKNOWN\n")
        else:
            for t in course_teacher_dict[c]:
                cur_file.write(teacher_dict[t][0]+"\n")
        cur_file.write("\nStudents:\n")
        for k in course_dict[c]:
            cur_file.write(k+"\n")
        cur_file.write("\n")

# outfile = open("stds_and_classes","wb")

# pickle.dump(student_dict, outfile)
# outfile.close()


# outfile2 = open("class_ids","wb")

# pickle.dump(course_id_dict, outfile2)
# outfile2.close()

# course_id_dict = {}

def get_teachers():
    """
    Gets all teacher user_ids, and courses they teach.
    """
    current_url = "https://bca.schoology.com/school/11897239/faculty?page="

    for page in range(0, 13):
        soup = BeautifulSoup(br.session.get(current_url+str(page)).text, 'html.parser')
        
        for teacher in soup.select(".faculty-name"):
            time.sleep(0.25)
            tid = int(teacher.find("a").attrs['href'][6:])
            name = teacher.get_text()
            soup2 = BeautifulSoup(br.session.get(
                "https://bca.schoology.com/user/"+str(tid)+"/courses/list").text, 'html.parser')
            item_names = soup2.select('.course-item-right')
            print(name)
            if len(item_names) > 0:
                courses = []
                for item in item_names:
                    course_link = item.select('a')[0].attrs['href']
                    course_id = int(course_link[8:])
                    course_name = item.select('a')[0].get_text()
                    if course_id not in course_id_dict.keys():
                        course_id_dict[course_id] = course_name
                    courses.append(course_id)
                # teacher_dict[tid] = (name, courses)
            
prefile = open("user_ids.txt", "r")
uids = []
for line in prefile:
    uid = int(line)
    uids.append(uid)
prefile.close()

infile = open("stds_and_classes", "rb")
student_dict = pickle.load(infile)
infile.close()

infile2 = open("class_ids", "rb")
course_id_dict = pickle.load(infile2)
infile2.close()

# outfile = open("class-ids","wb")
# pickle.dump(course_id_dict, outfile)
# outfile.close()

infile3 = open("teacher_dict", "rb")
teacher_dict = pickle.load(infile3)
infile3.close()

# for uid in uids:
#     time.sleep(0.3)
#     student_dict[uid]=get_name_and_courses(uid)

# outfile = open("class_ids","wb")

# pickle.dump(course_id_dict, outfile)
# outfile.close()


# for k in course_id_dict:
#     print(k,course_id_dict[k])
# print(course_id_dict)

# for k in student_dict:
#     for l in student_dict[k][1]:
#         if l not in course_id_dict.keys(): print(student_dict[k][0])

course_teacher_dict = {}
for k in teacher_dict:
    courses = teacher_dict[k][1]
    for c in courses:
        if c not in course_teacher_dict.keys():
            course_teacher_dict[c] = [k]
        else:
            course_teacher_dict[c].append(k)

generate_classes_list()

# for k in course_teacher_dict:
#     print(course_id_dict[k])
#     for t in course_teacher_dict[k]:
#         print(teacher_dict[t][0])
#     print()
