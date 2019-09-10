class Course:
    course_ids = []
    def __init__(self, cid, name):
        self.cid = cid
        Course.course_ids.append(cid)
        self.name = name
        self.teachers = []
        self.students = []
    
    def add_student(self, uid):
        if uid not in self.students:
            self.students.append(uid)
    
    def add_teacher(self, uid):
        if uid not in self.teachers:
            self.teachers.append(uid)
    
    def __str__(self):
        return "Course Name: "+self.name+" | Teachers: " + str(self.teachers)+" | Students: "+str(self.students)