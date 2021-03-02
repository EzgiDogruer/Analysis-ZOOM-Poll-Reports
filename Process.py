import Student
import csv
import Answer
import Question
import Global
import Poll
import xlwt
import xlrd
from os import path
import os.path
import json
import re
import logging


logging.basicConfig(filename="loggerFile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)

  #-------------read configuration file------------------------

def readFile():
    unused=0
myjsonfile = open('configuration.json', 'r')
jsondata = myjsonfile.read()
obj = json.loads(jsondata)

studentListFileName = str(obj['StudentList']) #pollName
logging.info("Student List taken from configuration file")
pollName = str(obj['ReadPollName']) #pollName
logging.info("Poll names are taken from configuration file")
attendanceFile = str(obj['AttendanceOutput']) #attendance file name
logging.info("Attendance file name is taken from configuration file")
globalFileName = str(obj['globalOutput']) #global file name
logging.info("Global file name is taken from configuration file")
logging.info("The files with attendance polls are detected from configuration file")
pollQuizPath = str(obj['pollQuizPathBegin']) #for poll quiz results path name
logging.info("The files with poll results are detected from configuration file")
answerList = obj['answerKeys'] #take an input answer key names
logging.info("Answer key files are taken from configuration file")
outputanormalies = str(obj['outputAnormalies'])
outputzoom = str(obj['outputzoom'])
outputAbsent =str(obj['outputAbsent'])
studentsLength = int(str(obj["studentlength"]))
readStudentTitles = obj['readStudentTitles']
QuestionTypes = obj['QuestionTypes']
AllAnswerTextIncludes =obj['AllAnswerTextIncludes']
AllPollTextIncludes=obj['AllPollTextIncludes']
AnswerKeyCont = str(obj['AnswerKeyCont'])


answerkeys = []
anormaly = []
absent = []
absents = []
anormalies = []
for i in range(len(answerList)):  #add answer key
  answerkeys.append(answerList[i].get('key'))
logging.info("Answer keys are added")

attendanceTitles = obj['attendanceFileTitles'] #attendance excel file titles
pollQuizTitles = obj['quizPollTitles'] #quiz poll excel file titles
globalFileTitles = obj['globalFileTitles'] #qlobal excel file titles
readAnswerKeyTitles = obj['readAnswerKeyTitles'] #read answer excel file titles

readFile()
#------------------------------------------------------------


attendanceAbsent = []
numberOfAbsent = studentsLength
students = []
studentsFullname = []
Polls = []
answerkeyPolls=[]
assignQuestion = 0
differentPoll = 0
countoflesson = 0
dateofpoll=[]
inputStudent = Student.Student("", "", "")
totalpoint = []
#read all students
inputStudent.readStudents(students,studentsLength, studentsFullname,studentListFileName,totalpoint)
logging.info("Students are read")

def isIncludeAll(pollFullname, studentIndex, studentsFullname ,type):
    k = 0
    while k < len(studentsFullname):
        isNameIncludeAll = 0
        w = 0
        while w < len(pollFullname):
            controlName = studentsFullname[k]
            if type == 1:
                controlName = re.sub(r" ", "", controlName)
            if pollFullname[w] in controlName:
                isNameIncludeAll += 1
                if isNameIncludeAll == len(pollFullname):
                    studentIndex = k
                    break
            w += 1

        if isNameIncludeAll == len(pollFullname):
            break
        k += 1
    if studentIndex == -1:
        isNameIncludeAll = 0
    return  studentIndex, isNameIncludeAll



def findStudentIndex(pollFullname, studentsFullname):

    studentIndex = -1
    isNameIncludeAll = 0
    pollFullnames = pollFullname
    pollFullnames = inputStudent.changeName(pollFullnames)

    #if isNameIncludeAll == 0 and studentIndex == -1:


    if isNameIncludeAll == 0 and studentIndex == -1 :
        pollFullname = pollFullnames
        pollFullname = re.sub('[^a-zA-Z]+', "", pollFullname)
        pollFullname = pollFullname.split(" ")
        studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 0)
        if  isNameIncludeAll == 0 and studentIndex == -1 :
            studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 1)


    if isNameIncludeAll == 0 and studentIndex == -1 :
        pollFullname = pollFullnames
        pollFullname = pollFullname.split(" ")
        s = 0
        while s < len(pollFullname):
            if pollFullname[s].isalpha() == False:
                findex = re.search("[^a-zA-Z]+", pollFullname[s])
                findex = findex.start()
                pollFullname[s] = pollFullname[s][:findex]
            s += 1
        studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 0)
        if  isNameIncludeAll == 0 and studentIndex == -1 :
            studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 1)

    if isNameIncludeAll == 0 and studentIndex == -1:
        pollFullname = pollFullnames
        pollFullname = pollFullname.split(" ")
        s = 0
        while s < len(pollFullname):
            if pollFullname[s].isalpha() == False:
                pollFullname.remove(pollFullname[s])
            s += 1
        studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 0)
        if isNameIncludeAll == 0 and studentIndex == -1:
            studentIndex, isNameIncludeAll = isIncludeAll(pollFullname, studentIndex, studentsFullname, 1)
    logging.info("Student found at index "+ str(studentIndex))
    return isNameIncludeAll, studentIndex


if(path.exists(attendanceFile)):
     loc = (attendanceFile)
     wb = xlrd.open_workbook(loc)
     sheet = wb.sheet_by_index(0)
     k=0
     f=1
     countoflesson = sheet.cell_value(1, 4)
     while k < len(students):
         students[k].attendance=int(sheet.cell_value(f, 3))
         logging.info("Attendance for student at index " + str(k) +" is taken ")
         k=k+1
         f=f+1

#----------------------

iter2=0
while iter2<studentsLength:
    attendanceAbsent.append(-1)
    iter2 += 1


readPath = pollName
#------------------for answer method----------------------------
inputAnswer =Answer.Answer("", "")
name=" "
line_count=0
with open(str(readPath) + ".csv", encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for column in csv_reader:
        if line_count <= 3:
            if line_count==3:
                name=column[0]
            print(f'Column names are {", ".join(column)}')
        line_count += 1


#READING ANSWER KEYS AND ASSIGN IT TO answerkeyPolls
answerkeyPolls = inputAnswer.read_and_assign_answerkey(answerkeyPolls,name,QuestionTypes,AllAnswerTextIncludes,AllPollTextIncludes,AnswerKeyCont)

inputPoll =Poll.Poll("", "", "","")
inputPoll2=Global.Global("", "")

line_count = 0


attendancedate=""

with open(str(readPath) + ".csv", encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for column in csv_reader:
        if line_count <= 5:
            print(f'Column names are {", ".join(column)}')
            line_count += 1
        else:
            pollFullname = column[1]
            pollEmail = column[2]

            isNameIncludeAll, studentIndex = findStudentIndex(pollFullname,studentsFullname)

            if isNameIncludeAll == 0:
                anormaly.append('{student name:' + pollFullname + '},' + '{student email:' + pollEmail + '}')
                continue

            students[studentIndex].attendance += 1
            checkAttending = inputAnswer.isInsideInAnswerkeyPolls(answerkeyPolls, column[4])

            if checkAttending == -1:
                attendanceAbsent[studentIndex]=1
                numberOfAbsent -= 1

            elif checkAttending != -1:
                question_students = []
                totalPointThisPoll = 0
                #assign questions in the question list
                first_question_text = column[4]
                length_polls = len(Polls)
                iter = 0
                questionIndexInPoll = 0
                indexOfPoll = -1
                while iter < length_polls:
                    length_questions = len(Polls[iter].answers)
                    iter2 = 0

                    first_question_text = first_question_text.replace("\n ", "")
                    first_question_text = first_question_text.replace(" ", "")
                    while iter2 < length_questions:
                        ans_questiontext = Polls[iter].answers[iter2].questionText.replace("\n", "")
                        ans_questiontext = Polls[iter].answers[iter2].questionText.replace(" ", "")
                        if ans_questiontext == first_question_text:
                            indexOfPoll = iter
                            questionIndexInPoll = iter2
                            break
                        iter2 += 1
                    if indexOfPoll != -1:
                        break
                    iter += 1
                assignQuestion = 0

                if indexOfPoll == -1:  # ------------------FOR NEW POLL
                     anormalies.append(anormaly)
                     anormaly = []
                     absent = []
                     if numberOfAbsent != studentsLength:
                         iter2 = 0
                         while iter2 < studentsLength:
                             if attendanceAbsent[iter2] == -1:
                                 absent.append('{student no:' + str(students[iter2].studentid) + ',student name:'
                                               + students[iter2].firstName + ' ' + students[iter2].lastName + '},')
                             iter2 += 1
                         absents.append(absent)
                         numberOfAbsent = studentsLength

                         iter2 = 0
                         attendanceAbsent = []
                         while iter2 < studentsLength:
                             attendanceAbsent.append(-1)
                             iter2 += 1

                     if differentPoll != 0:
                         absent = []
                         k, iter2 = 0, 0
                         while k < studentsLength:
                             iter2 = 0
                             while iter2 < len(students[k].question[length_polls - 1]):
                                 isabsent = students[k].question[length_polls - 1][iter2]

                                 if isabsent != -1:
                                     break

                                 iter2 += 1

                             if iter2 == len(students[k].question[length_polls - 1]):
                                 absent.append('{student no:' + str(students[k].studentid) + ',student name:'
                                               + students[k].firstName + ' ' + students[k].lastName + '},')
                             k = k + 1
                         absents.append(absent)

                     differentPoll += 1
                     assignQuestion += 1

                     if assignQuestion == 1:
                        assignQuestion == 0
                        numOfQuestion = 0
                        IndexOfanswerkeyPolls=-1
                        IndexOfanswerkeyPolls = inputAnswer.isInsideInAnswerkeyPolls(answerkeyPolls, first_question_text)

                        #kontrol koy
                        Polls = inputAnswer.assignPoll(Polls, answerkeyPolls, column, IndexOfanswerkeyPolls,dateofpoll,students)
                        dateofpoll[iter]=column[3]
                        assign_1 = 0
                        length_polls = len(Polls)
                        while assign_1 < Polls[length_polls - 1].answerLength:
                            question_students.append(-1)
                            assign_1 += 1

                        k = 0
                        while k < studentsLength:
                            students[k].question.append(question_students)
                            students[k].totalpointforThispoll.append(0)
                            k += 1

                        totalPointThisPoll = 0
                        iter = len(Polls) - 1
                        # poll içi questiontext doldurma
                        while numOfQuestion < Polls[iter].answerLength :
                            questiontxt = column[numOfQuestion * 2 + 4]
                            Polls[iter].questionText.append(questiontxt)
                            question = Question.Question(questiontxt)
                            Polls[iter].questionsInPoll.append(question)
                            numOfQuestion += 1

                question_students = []
                assign_1 = 0
                while assign_1 < Polls[length_polls - 1].answerLength:
                    question_students.append(-1)
                    assign_1 += 1
                count_question = len(Polls[iter].answers)
                numOfQuestion = 0
                while numOfQuestion < count_question and column[(numOfQuestion * 2) + 4] !="":
                    questiontxt = column[(numOfQuestion * 2) + 4]
                    questionIndex = Polls[iter].questionText.index(questiontxt)
                    answerOfQuestion = column[(numOfQuestion * 2) + 5].split(";") # eğer cevapta ; ile ilgili sorun varsa buraya bak

                    if len(Polls[iter].questionsInPoll[questionIndex].answers) == 0:
                        iter2=0
                        while iter2 < len(Polls[iter].answers[questionIndex].answer):
                            Polls[iter].questionsInPoll[questionIndex].answers.append(Polls[iter].answers[questionIndex].answer[iter2])
                            Polls[iter].questionsInPoll[questionIndex].countOfStudent.append(0)
                            iter2 += 1
                    iter2 = 0
                    while iter2 < len(answerOfQuestion):
                        try:
                            answerIndex = Polls[iter].questionsInPoll[questionIndex].answers.index(answerOfQuestion[iter2])
                        except ValueError:
                            answerIndex = -1
                        if answerIndex == -1:
                            Polls[iter].questionsInPoll[questionIndex].answers.append(answerOfQuestion[iter2])
                            Polls[iter].questionsInPoll[questionIndex].countOfStudent.append(1)
                        elif answerIndex != -2 and answerIndex != -1:
                            Polls[iter].questionsInPoll[questionIndex].countOfStudent[answerIndex] += 1
                        iter2 += 1
                    NoTrueAnswer = 0
                    iter2, i = 0, 0
                    while iter2 < len(Polls[iter].answers[questionIndex].answer):
                        while i < len(answerOfQuestion):
                           if answerOfQuestion[i] == Polls[iter].answers[questionIndex].answer[iter2] and NoTrueAnswer != -1: ##burası
                                NoTrueAnswer = -1
                                students[studentIndex].totalPoint += 1
                                question_students[questionIndex] = 1
                                totalPointThisPoll += 1
                                logging.info("Points for student at index " + str(studentIndex) + " is increased")
                                continue
                           i += 1

                        iter2 += 1


                    if NoTrueAnswer==0:
                        question_students[questionIndex] = 0
                    numOfQuestion += 1
                iter2 = 0
                inWhichQuestion = 0
                while iter2 < len(question_students):
                    if question_students[iter2] != -1:
                        students[studentIndex].answerof[iter].append(column[(inWhichQuestion * 2) + 5])
                        inWhichQuestion += 1
                    elif question_students[iter2] == -1:
                        students[studentIndex].answerof[iter].append("")

                    iter2 += 1

                students[studentIndex].question[iter] = question_students
                students[studentIndex].totalpointforThispoll[iter] = totalPointThisPoll
            if checkAttending==-1:
                date=column[3]
                date=date.split(":")
                date=date[0]
                if(attendancedate!=date):
                    countoflesson+=1
                    attendancedate=date
            line_count += 1

    anormalies.append(anormaly)
    anormaly = []
    absent = []

    if numberOfAbsent != studentsLength:
        iter2 = 0
        while iter2 < studentsLength:
            if attendanceAbsent[iter2] == -1:
                absent.append('{student no:' + str(students[iter2].studentid) + ',student name:'
                              + students[iter2].firstName + ' ' + students[iter2].lastName + '},')
            iter2 += 1
        absents.append(absent)
        numberOfAbsent = studentsLength

        iter2 = 0
        attendanceAbsent = []
        while iter2 < studentsLength:
            attendanceAbsent.append(-1)
            iter2 += 1
    if differentPoll != 0:
        absent = []
        k, iter2 = 0, 0
        while k < studentsLength:
            iter2 = 0
            while iter2 < len(students[k].question[length_polls - 1]):
                isabsent = students[k].question[length_polls - 1][iter2]

                if isabsent != -1:
                    break
                iter2 += 1
            if iter2 == len(students[k].question[length_polls - 1]):
                absent.append('{student no:' + str(students[k].studentid) + ',student name:'
                              + students[k].firstName + ' ' + students[k].lastName + '},')
            k = k + 1
        absents.append(absent)


unused=0
length_polls = len(Polls)
if length_polls != 0:
    inputPoll.writePollInformation(students, readPath, studentsLength, Polls, pollQuizTitles, pollQuizPath, dateofpoll)
    inputPoll2.writeinGlobal(students, readPath, Polls, globalFileName, globalFileTitles, totalpoint, dateofpoll)
    inputPoll2.studentınformation(Polls, students,readStudentTitles)


countoflesson += len(Polls)
if countoflesson != 0 :
    wb = xlwt.Workbook(attendanceFile)

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    logging.info("Sheet is created")

    sheet1.write(0, 0, attendanceTitles[0])
    sheet1.write(0, 1, attendanceTitles[1])
    sheet1.write(0, 2, attendanceTitles[2])
    sheet1.write(0, 3, attendanceTitles[3])
    sheet1.write(0, 4, attendanceTitles[4])
    sheet1.write(0, 5, attendanceTitles[5])
    d = 0
    i = 1
    while d < len(students):
        sheet1.write(i, 0, str(students[d].studentid))
        sheet1.write(i, 1, students[d].firstName)
        sheet1.write(i, 2, students[d].lastName)
        sheet1.write(i, 3, students[d].attendance)
        sheet1.write(i, 4, countoflesson)
        sheet1.write(i, 5, str((students[d].attendance / countoflesson) * 100))
        logging.info("Student with id " + str(students[d].studentid) + " is written")
        d = d + 1
        i = i + 1

    wb.save(attendanceFile)

if countoflesson == 0:
    print("\n---Students are not matched please control the input files..---")

def createjsonFile():
    directory = "./ABSENTS&ANOMALIES JSON/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    i=0
    while i<len(absents):
        with open(directory+"Output "+str(i+1)+".Poll "+pollName+".json", 'w') as out:
            out.write('%s\n' % '{')
            a = outputzoom + pollName + '.csv",'
            out.write('%s\n' % (outputzoom + pollName + '.csv",'))
            out.write('%s\n' % outputAbsent)
            out.write('%s\n' % '[')
            for listabsent in absents[i]:
                out.write('%s\n' % listabsent)
            out.write('%s\n' % '],')
            out.write('%s\n' % outputanormalies)
            out.write('%s\n' % '[')

            for listitem in anormalies[i]:
                out.write('%s\n' % listitem)
            out.write('%s\n' % '],')
            out.write('%s\n' % '}')

        i=i+1

    logging.info("Json file is created for the students who are not found in the Student List")

createjsonFile()
