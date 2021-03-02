import Question
import xlsxwriter
import logging
import re
import os.path
class Poll ():
    def __init__(self, answerLength, answers, pollName, pollNumber):
        self.questionsInPoll = []  # 1 poll için soru texti, kimlerin hangi şıkkı kaç kez seçtiği, seçilen tüm şıklar
        self.questionText = []
        self.pollNumber = pollNumber
        self.pollName = pollName
        self.answers = answers  # soruların cevap anahtarı- doğru cevapları
        self.answerLength = answerLength



    def writePollInformation(self, students, readPath, studentsLength, Polls,pollQuizTitles,pollQuizPath,dateofpoll):
        iter = 0
        directory = "./POLL REPORT RESULTS/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        length_Polls = len(Polls)
        while iter < length_Polls:
            row = 0
            col = 0
            newPath = readPath.split(".csv")
            if iter == 0:
                picname=newPath[0]
            pollName = re.sub("[^0-9a-zA-Z]+", "_", Polls[iter].pollName)
            dateofpoll1=re.sub("[^0-9a-zA-Z]+", "_", dateofpoll[iter])
            readPath = directory+"Poll_" + str(Polls[iter].pollNumber) + "_"+ pollName +"_"+dateofpoll1
            workbook = xlsxwriter.Workbook(readPath + '.xlsx')
            worksheet = workbook.add_worksheet()
            worksheet2 = workbook.add_worksheet('Sheet2')
            # Iterate over the data and write it out row by row.

            worksheet.write(row, col, pollQuizTitles[0])
            col += 1
            worksheet.write(row, col, pollQuizTitles[1])
            col += 1
            for questionNumber in range(1, Polls[iter].answerLength + 1):
                worksheet.write(row, col, "Q" + str(questionNumber))
                col += 1

            worksheet.write(row, col, pollQuizTitles[2])
            col += 1
            worksheet.write(row, col, pollQuizTitles[3])
            col += 1
            worksheet.write(row, col, pollQuizTitles[4])
            col += 1
            worksheet.write(row, col, pollQuizTitles[5])
            col += 1
            worksheet.write(row, col, pollQuizTitles[6])
            col += 1
            worksheet.write(row, col, pollQuizTitles[7])
            col += 1

            i = 0;
            while i < len(students):
                row += 1
                col = 0
                worksheet.write(row, col, str(students[i].studentid))
                col += 1
                worksheet.write(row, col, students[i].firstName + " " + students[i].lastName)
                col += 1
                j = 0
                while j < len(students[i].question[iter]):
                    worksheet.write(row, col, students[i].question[iter][j])
                    col += 1
                    j += 1


                worksheet.write(row, col, Polls[iter].answerLength)
                col += 1
                worksheet.write(row, col, students[i].totalpointforThispoll[iter])
                col += 1
                lengthOfQuestion = students[i].question[iter]
                answerLength = Polls[iter].answerLength
                #Wrong answers
                if sum(lengthOfQuestion)== (-1 * answerLength): #If student did not enter the quiz
                    worksheet.write(row, col, str(0))
                    col += 1
                else:#If student enter the quiz
                    numOfWrongQuestion = 0
                    iter2 = 0
                    while iter2 < len(lengthOfQuestion):
                        if students[i].question[iter][iter2] == 0:
                            numOfWrongQuestion += 1
                        iter2 += 1
                    worksheet.write(row, col, str(numOfWrongQuestion))
                    col += 1

                #Empty Answers
                if sum(lengthOfQuestion)== (-1 * answerLength): #If student did not enter the quiz
                    worksheet.write(row, col, str(answerLength))
                    col += 1
                else:#If student did not enter the quiz
                    iter2 = 0
                    numOfEmptyQuestion = 0
                    while iter2 < len(lengthOfQuestion):
                        if students[i].question[iter][iter2] == -1:
                            numOfEmptyQuestion += 1
                        iter2 += 1
                    worksheet.write(row, col, str(numOfEmptyQuestion))
                    col += 1

                worksheet.write(row, col, str(students[i].totalpointforThispoll[iter]/answerLength))
                col += 1
                worksheet.write(row, col, str((students[i].totalpointforThispoll[iter] / answerLength) * 100))
                col += 1

                i += 1

            a = 0
            lengthOfPreviousAnswer = 0
            previousPlace = studentsLength + 4 + 15 * a + lengthOfPreviousAnswer
            worksheet.write('A' + str(previousPlace), "----------------QUESTIONS---------------- ")
            previousPlace += 2
            inputQuestion = Question.Question("")
            a, previousPlace, worksheet, iter, Polls = inputQuestion.histogram( a, Polls, previousPlace, worksheet, iter, picname)
            inputQuestion.summary(0, Polls, 1, worksheet2, iter, picname)
            workbook.close()
            iter += 1
            logging.info("Output file for " + readPath + "is created")
