import pandas as pd
import Poll
import re
class Answer ():
    def __init__(self, questionText, answer):
        self.questionText = questionText
        self.answer = answer

    def getNumbers(self, str):
        array = re.findall(r'[0-9]+', str)
        return array
    def read_and_assign_answerkey(self, answerkeyPolls,name,QuestionTypes,AllAnswerTextIncludes,AllPollTextIncludes,AnswerKeyCont):
        whichRow = 0
        numOfAllPolls = 0
        inWhichPoll = -1
        PollsA = []
        pollname = ""
        pollNumber = 0
        polllength = 0
        inWhichQuestion = -1
        pollquestions = ""
        pollanswers = []
        pollanswersForEachQuestion = []
        inputAnswer=Answer("","")
        try:
            file = open(name+AnswerKeyCont, "r", encoding="utf-8")
            for i in file:  # Tıpkı listeler gibi dosyanın her bir satırı üzerinde geziniyoruz.
                if i != "\n":
                    if whichRow == 0:
                        str = i
                        str = inputAnswer.getNumbers(str)
                        numOfAllPolls = str[0]

                    elif AllPollTextIncludes[0] and AllPollTextIncludes[1] in i:
                        inWhichPoll += 1
                        if inWhichQuestion != -1 and inWhichPoll != 0:
                            answer = Answer(pollquestions, pollanswersForEachQuestion)
                            pollanswers.append(answer)
                            pollquestions = ""
                            pollanswersForEachQuestion = []

                        if inWhichPoll != 0:
                            poll = Poll.Poll(polllength, pollanswers, pollname, pollNumber)
                            PollsA.append(poll)
                            pollanswers = []
                            polllength = 0
                            pollname = ""
                            inWhichQuestion = -1
                        str = i
                        str = str.split(":")
                        pollNumber = str[0].split()
                        pollNumber = pollNumber[-1]
                        str = str[1].split("\t")
                        pollname = str[0]
                        str = str[1].split()
                        polllength = str[0]


                    elif (QuestionTypes[0] in i) or (QuestionTypes[1] in i):
                        inWhichQuestion += 1
                        if inWhichQuestion != 0:
                            answer = Answer(pollquestions, pollanswersForEachQuestion)
                            pollanswers.append(answer)
                            pollquestions = ""
                            pollanswersForEachQuestion = []

                        str = i
                        str = str.split(". ", 1)
                        if QuestionTypes[0] in str[1]:
                            str = str[1].split(QuestionTypes[0])
                        elif QuestionTypes[1] in str[1]:
                            str = str[1].split(QuestionTypes[1])
                        pollquestions = str[0]

                    elif AllAnswerTextIncludes[0] and AllAnswerTextIncludes[1] in i:
                        str = i
                        str = str.split(" ", 2)
                        str = str[2].split("\n")
                        pollanswersForEachQuestion.append(str[0])

                    else:
                        str = i
                        str = inputAnswer.getNumbers(str)
                    whichRow += 1
            file.close()
        except FileNotFoundError:
            print("File is not found....")

        if (inWhichQuestion != -1) and inWhichPoll != 0:
            answer = Answer(pollquestions, pollanswersForEachQuestion)
            pollanswers.append(answer)
            pollquestions = ""
            pollanswersForEachQuestion = []
        if inWhichPoll != 0:
            poll = Poll.Poll(polllength, pollanswers, pollname, pollNumber)
            PollsA.append(poll)


        answerkeyPolls=PollsA
        return answerkeyPolls

    # READ QUESTIONS AND ANSWERS OF THE QUESTION POLL
    def isInsideInAnswerkeyPolls(self, answerkeyPolls, first_question_text):
        first_question_text = first_question_text.replace("\n","")
        first_question_text = first_question_text.replace("\t", "")
        first_question_text = first_question_text.replace(" ", "")
        first_question_text = re.sub("[^0-9a-zA-Z]+", "",first_question_text)
        iter=-1
        k=0
        while k<len(answerkeyPolls):
            d=0
            while d < len(answerkeyPolls[k].answers):
                question = answerkeyPolls[k].answers[d].questionText.replace("\n", "")
                question = question.replace("\t", "")
                question = question.replace(" ", "")
                question = re.sub("[^0-9a-zA-Z]+", "", question)

                if question == first_question_text:
                    #print(answerkeyPolls[k].answers[d].questionText)
                    iter = k
                    break
                d += 1
            k += 1
            if iter == k-1:
                break
        return iter

    def assignPoll(self, Polls, answerkeyPolls, column, IndexOfanswerkeyPolls,dateofpoll,students):
        w = 0

        answers = []
        pollName = answerkeyPolls[IndexOfanswerkeyPolls].pollName
        answerLength = int(answerkeyPolls[IndexOfanswerkeyPolls].answerLength)
        pollNumber = int(answerkeyPolls[IndexOfanswerkeyPolls].pollNumber)
        while w < answerLength:
            questionsInPoll = column[4 + w * 2].replace("\n","")
            questionsInPoll = questionsInPoll.replace(" ", "")
            questionsInPoll = questionsInPoll.replace("\t", "")
            questionsInPoll = re.sub("[^0-9a-zA-Z]+", "", questionsInPoll)
            g = 0
            while g < len(answerkeyPolls[IndexOfanswerkeyPolls].answers):
                answerkeyquestionText = answerkeyPolls[IndexOfanswerkeyPolls].answers[g].questionText.replace("\n", "")
                answerkeyquestionText = answerkeyquestionText.replace(" ", "")
                answerkeyquestionText = answerkeyquestionText.replace("\t", "")
                answerkeyquestionText = re.sub("[^0-9a-zA-Z]+", "", answerkeyquestionText)

                if questionsInPoll == answerkeyquestionText:
                    answer = Answer(answerkeyPolls[IndexOfanswerkeyPolls].answers[g].questionText, answerkeyPolls[IndexOfanswerkeyPolls].answers[g].answer)
                    answers.append(answer)
                g += 1

            w += 1
        poll = Poll.Poll(answerLength, answers, pollName, pollNumber)
        dateofpoll.append(" ")
        k=0
        while k <len(students):
            students[k].answerof.append([])
            k=k+1
        Polls.append(poll)
        return Polls


