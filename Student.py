import pandas as pd
import Student
import re
import xlrd
import logging
class Student() :



    def __init__(self, studentid, firstName, lastName):
        self.studentid = studentid
        self.firstName = firstName
        self.lastName = lastName
        self.attendance = 0
        self.question = []
        self.totalpointforThispoll = []
        self.totalPoint = 0;
        self.answerof=[]


    def changeName(self, sFullname):
        sFullname = re.sub(r"İ", "i", sFullname)
        sFullname = re.sub(r"I", "i", sFullname)
        sFullname = re.sub(r"Ç", "c", sFullname)
        sFullname = re.sub(r"Ş", "s", sFullname)
        sFullname = re.sub(r"Ü", "u", sFullname)
        sFullname = re.sub(r"Ğ", "g", sFullname)
        sFullname = re.sub(r"i", "i", sFullname)
        sFullname = re.sub(r"ı", "i", sFullname)
        sFullname = re.sub(r"ç", "c", sFullname)
        sFullname = re.sub(r"ş", "s", sFullname)
        sFullname = re.sub(r"ü", "u", sFullname)
        sFullname = re.sub(r"ğ", "g", sFullname)
        sFullname = re.sub(r"O", "o", sFullname)
        sFullname = re.sub(r"Ö", "o", sFullname)
        sFullname = re.sub(r"ö", "o", sFullname)
        sFullname = sFullname.lower()  # for the rest use default lower
        return sFullname

    # READ ALL STUDENTS
    def readStudents(self,students, studentsLength, studentsFullname,studentListFileName,totalpoint):
        i = 0
        inputStudent = Student("", "", "")
        Workbook = xlrd.open_workbook(studentListFileName)
        Worksheet = Workbook.sheet_by_index(0)
        c = 0
        while c < Worksheet.nrows:
            value = Worksheet.cell_value(c, 4)
            if (value == "" or value == "Adı"):
                c += 1
            else:
                studentId=Worksheet.cell_value(c, 2)
                firstName = Worksheet.cell_value(c,4)
                lastName= Worksheet.cell_value(c,7)

                sFullName = firstName + " " + lastName
                sFullName = inputStudent.changeName(sFullName)
                studentsFullname.append(sFullName)
                Student1 = Student(studentId, firstName, lastName)
                students.append(Student1)
                totalpoint.append(0)
                logging.info("Student with id "+studentId+" is read")
                c = c + 1

