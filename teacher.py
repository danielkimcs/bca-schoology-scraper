from bs4 import BeautifulSoup
from course import Course

class Teacher:
    teacher_ids = []
    def __init__(self, uid, name, courses_html, course_list):
        self.uid = uid
        Teacher.teacher_ids.append(uid)
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
                new_course.add_teacher(self)
                course_list.append(new_course)
            else:
                for c in course_list:
                    if c.cid == course_id:
                        c.add_teacher(self)
            courses.append(course_id)
        
        self.courses = courses
    
    def __str__(self):
        return "Name: " + self.name + " | Courses: " + str(self.courses)