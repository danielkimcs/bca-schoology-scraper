from bs4 import BeautifulSoup
from course import Course

class Student:
    student_ids = []
    def __init__(self, uid, name, courses_html, user_html, course_list, senior = False):
        self.uid = uid
        Student.student_ids.append(uid)
        self.name = name

        # Courses
        soup = BeautifulSoup(courses_html, 'html.parser')

        item_names = soup.select('.course-item-right')
        courses = []
        for item in item_names:
            course_link = item.select('a')[0].attrs['href']
            course_id = int(course_link[8:])
            course_name = item.select('a')[0].get_text()
            if course_id not in Course.course_ids:
                new_course = Course(course_id, course_name)
                new_course.add_student(self)
                course_list.append(new_course)
            else:
                for c in course_list:
                    if c.cid == course_id:
                        c.add_student(self)
            courses.append(course_id)
        
        self.courses = courses

        # Name, Grade
        soup2 = BeautifulSoup(user_html, 'html.parser')

        self.grade = None
        if (len(soup2.select("span.admin-val.email")) > 0):
            email = soup2.select("span.admin-val.email")[0].get_text()
            # Frosh = 1, Soph = 2, Junior = 3, Senior = 4
            if not senior or (senior and "20@bergen.org" in email):
                self.grade = 24-int(email[-13:-11])
    
    def __str__(self):
        return "Name: " + " " + self.name + " " + "| Courses: " + " " + str(self.courses) + " " + "| Grade: " + " " + str(self.grade)