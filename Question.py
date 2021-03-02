import matplotlib.pyplot as plt
import logging
import os

class Question ():

    def __init__(self,question):
        self.question = question
        self.answers = []
        self.countOfStudent = []

        #create a directory to keep *.png files
        self.directory_histogram = "histogram_pngs"
        self.directory_pieChart = "pieChart_pngs"
        self.parent_dir = os.path.dirname(os.path.realpath(__file__))
        self.path_histogram = os.path.join( self.parent_dir , self.directory_histogram)
        self.path_pieChart = os.path.join(self.parent_dir, self.directory_pieChart)

        isdir = os.path.isdir(self.path_histogram)
        if not isdir:
            mode = 0o666
            os.mkdir(self.path_histogram, mode)

        isdir = os.path.isdir(self.path_pieChart)
        if not isdir:
            mode = 0o666
            os.mkdir(self.path_pieChart, mode)



    def histogram(self, a, Polls, previousPlace, worksheet, iter, picname ):
        while a < Polls[iter].answerLength:
            sizes = []
            myColors = []
            myLabels = []
            myExplode = []
            x_bar = []
            y_bar = []
            lengthOfAnswer = len(Polls[iter].questionsInPoll[a].answers)
            i = 0
            trueAnswerIndex = 0

            total_ans = 0
            while i < lengthOfAnswer:
                total_ans += Polls[iter].questionsInPoll[a].countOfStudent[i]
                i += 1

            i = 0

            while i < lengthOfAnswer:
                x_bar.append(str(i + 1))
                y_bar.append(Polls[iter].questionsInPoll[a].countOfStudent[i])

                myLabels.append(str(i + 1))
                sizes.append((Polls[iter].questionsInPoll[a].countOfStudent[i]/total_ans)*100)
                myExplode.append(0.01)

                if Polls[iter].questionsInPoll[a].answers[i] == Polls[iter].answers[a].answer:
                    trueAnswerIndex = i


                j = 0
                while j < len(Polls[iter].answers[a].answer):
                    if Polls[iter].questionsInPoll[a].answers[i] == Polls[iter].answers[a].answer[j]:
                        myColors.append("red")
                    elif Polls[iter].questionsInPoll[a].answers[i] != Polls[iter].answers[a].answer[j]:
                        myColors.append("blue")
                    j += 1


                i += 1

            barlist = plt.bar(x_bar, y_bar, color='b')
            j = 0
            while j < len(Polls[iter].answers[a].answer):
                barlist[j].set_color('g')
                j += 1

            nameOfPng = str(1 + a) + "Pic_" + str(iter + 1) + "Poll_" + picname + ".png"
            plt.savefig(self.path_histogram + "/" + nameOfPng, dpi=150)
            plt.close()

            plt.pie(sizes, labels=myLabels, colors=myColors, autopct='%.2f', explode=myExplode)
            nameOfPng = str(1 + a) + "Pic_" + str(iter + 1) + "Poll_" + picname + ".png"
            plt.savefig(self.path_pieChart + "/" + nameOfPng, dpi=150)
            plt.close()

            worksheet.write('A' + str(previousPlace), str(a + 1) + "Q) " + Polls[iter].questionsInPoll[a].question)
            previousPlace += 1
            worksheet.insert_image('B' + str(previousPlace),self.path_histogram + "/" + nameOfPng, {'x_scale': 0.5, 'y_scale': 0.5})
            worksheet.insert_image('H' + str(previousPlace),self.path_pieChart + "/" + nameOfPng, {'x_scale': 0.5, 'y_scale': 0.5})

            i = 0
            previousPlace += 12
            while i < lengthOfAnswer:
                previousPlace += 1
                worksheet.write('A' + str(previousPlace),
                                str(i + 1) + "- " + Polls[iter].questionsInPoll[a].answers[i] + " (" + str(
                                    Polls[iter].questionsInPoll[a].countOfStudent[i]) + " students select)")

                i += 1
            previousPlace += 3

            a += 1
            logging.info("Histograms are created")

        return a, previousPlace, worksheet, iter, Polls

    def summary(self, a, Polls, previousPlace, worksheet, iter, picname ):
        worksheet.write('A' + str(previousPlace), "----------------SUMMARY---------------- ")
        previousPlace += 2
        worksheet.write('A' + str(previousPlace),'Diagram')
        worksheet.write('F' + str(previousPlace), 'Correct Answer')
        worksheet.write('G' + str(previousPlace), 'Question Number')
        previousPlace += 3

        while a < Polls[iter].answerLength:
            lengthOfAnswer = len(Polls[iter].questionsInPoll[a].answers)
            i = 0
            trueAnswerIndex = 0

            total_ans = 0
            while i < lengthOfAnswer:
                total_ans += Polls[iter].questionsInPoll[a].countOfStudent[i]
                i += 1

            i = 0

            while i < lengthOfAnswer:
                if Polls[iter].questionsInPoll[a].answers[i] == Polls[iter].answers[a].answer:
                    trueAnswerIndex = i

                i += 1

            nameOfPng = str(1 + a) + "Pic_" + str(iter + 1) + "Poll_" + picname + ".png"
            worksheet.insert_image('A' + str(previousPlace),self.path_pieChart + "/" + nameOfPng, {'x_scale': 0.5, 'y_scale': 0.5})
            worksheet.write('F' + str(previousPlace), str(Polls[iter].questionsInPoll[a].countOfStudent[trueAnswerIndex]) + '/' + str(total_ans))
            worksheet.write('G' + str(previousPlace), str(a + 1) + "Q) " + Polls[iter].questionsInPoll[a].question)

            previousPlace += 13
            a += 1
            logging.info("Summary is created")

        return a, previousPlace, worksheet, iter, Polls