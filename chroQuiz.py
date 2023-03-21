import requests
from customtkinter import (
    CTkFrame,
    CTkLabel,
    BOTH,
    X,
    IntVar,
    CTk,
    CTkFont,
    CTkButton,
    CTkCheckBox,
    TOP,
    RIGHT,
    LEFT,
    BOTTOM,
)
from json import loads
import random

# Initialization

answered = 1
qNo = 1

categories = [
    "Arts & Literature",
    "Film & TV",
    "Food & Drink",
    "General Knowledge",
    "Geography",
    "History",
    "Music",
    "Science",
    "Society & culture",
    "Sports & liesure",
]
index = list(range(10))
catDict = dict(zip(index, categories))

root = CTk()
root.geometry("800x420")
root.title("chroQuiz")
root.resizable(0, 0)
choosingVars = [IntVar() for i in range(10)]


art1 = IntVar()
science = IntVar()
sport = IntVar()
politucs = IntVar()


# Frames
homeFrame = CTkFrame(root)
homeFrame.pack(fill=BOTH)
quizFrame = CTkFrame(root, height=700)
endFrame = CTkFrame(root)
loadFrame = CTkFrame(root, height=800)
statusFrame = CTkFrame(root, height=100)
resultFrame = CTkFrame(root, height=800)

# Backend
def homeProceed():
    catStr = str()
    for j, i in enumerate(choosingVars):
        if i.get():
            catStr = catStr.__add__(catDict[j] + ",")
    try:
        if catStr[-1] == ",":
            catStr = catStr[:-1]
    except:
        pass
    if catStr == "":
        easyQuest = "https://the-trivia-api.com/api/questions?difficulty=easy&limit=10"
        mediumQuest = (
            "https://the-trivia-api.com/api/questions?difficulty=medium&limit=6"
        )
        hardQuest = "https://the-trivia-api.com/api/questions?difficulty=hard&limit=4"
    else:
        easyQuest = (
            "https://the-trivia-api.com/api/questions?difficulty=easy&limit=10&category="
            + catStr
        )
        mediumQuest = (
            "https://the-trivia-api.com/api/questions?difficulty=medium&limit=6&category="
            + catStr
        )
        hardQuest = (
            "https://the-trivia-api.com/api/questions?difficulty=hard&limit=4&category="
            + catStr
        )
    return loader(easyQuest, mediumQuest, hardQuest)


def loader(easy, med, hard):
    homeFrame.pack_forget()
    loadFrame.pack(fill=BOTH)
    loadLabel = CTkLabel(
        loadFrame, text="Loading...", font=CTkFont("Noto Sans", 30, "bold")
    )
    loadLabel.place(relx=0.5, rely=0.5)
    root.update()
    try:
        easyQ = requests.get(easy)
        medQ = requests.get(med)
        hardQ = requests.get(hard)
        return loadParser(easyQ, medQ, hardQ)

    except:
        loadLabel.place_forget()
        CTkLabel(
            loadFrame,
            text="Something went wrong :{\nPlease check your internet connection",
            font=CTkFont("Noto Sans", 20),
        ).place(relx=0.25, rely=0.5)
        CTkButton(
            loadFrame,
            text="Proceed",
            font=CTkFont("Noto Sans", 13),
            command=loadProceed,
        ).place(relx=0.25, rely=0.7)
        root.update()


def loadParser(easy, med, hard):
    easyQ = loads(easy.text)
    medQ = loads(med.text)
    hardQ = loads(hard.text)
    return quizLoader(easyQ, medQ, hardQ)


def loadProceed():
    loadFrame.pack_forget()
    homeFrame.pack(fill=BOTH)
    root.update()


def homeLoader():
    CTkLabel(
        homeFrame, text="Welcome to chroQuiz\n", font=CTkFont("Noto Sans", 20, "bold")
    ).pack()
    CTkLabel(
        homeFrame,
        text="There will be total of 20 quizes to be answered, 10 easy questions, 6 medium questions and 4 hard questions. If you even lost a single quiz the program ends and results get declared. Please keep your internet connection active to load the quiz\n",
        font=CTkFont("Noto Sans", 15, "normal"),
        wraplength=700,
    ).pack()
    CTkLabel(
        homeFrame,
        text="Categories of the quiz",
        font=CTkFont("Noto Sans", 15, underline=1),
    ).pack()
    for ind, cat in catDict.items():
        CTkCheckBox(homeFrame, text=cat, variable=choosingVars[ind]).pack(anchor="w")
    CTkButton(homeFrame, text="Proceed", command=homeProceed).pack()


def quizLoader(easy, med, hard):
    global answered, qNo, qLabel, totalQ, nextButton, difficulty

    loadFrame.pack_forget()

    statusFrame.pack(side=BOTTOM, anchor="s", fill=X)
    quizFrame.pack(side=TOP, fill=BOTH)

    qLabel = CTkLabel(
        quizFrame, font=CTkFont(family="Noto Sans", size=15), wraplength=400
    )
    nextButton = CTkButton(statusFrame, text="Next", command=quizNext)

    difficulty = CTkLabel(statusFrame, text="Difficulty:easy")
    difficulty.pack(side=LEFT, anchor="s", fill=X)
    totalQ = easy + med + hard
    quizAsker()


def quizAsker():
    global answered, qNo, qLabel, totalQ, op1, op2, op3, op4, difficulty
    if answered:
        if qNo == 11:
            difficulty.configure(text="Difficulty:medium")
        if qNo == 17:
            difficulty.configure(text="Difficulty:hard")
        if qNo == 21:
            return quizResult()
        answered = 0
        qLabel.configure(text=totalQ[qNo - 1]["question"])
        qLabel.pack(side=TOP)
        options = totalQ[qNo - 1]["incorrectAnswers"] + [
            totalQ[qNo - 1]["correctAnswer"]
        ]
        random.shuffle(options)
        op1 = CTkButton(
            quizFrame,
            text=options[0],
            command=lambda: quizAnswer(options[0], options),
            font=CTkFont(family="Noto Sans", size=14),
        )

        op2 = CTkButton(
            quizFrame,
            text=options[1],
            command=lambda: quizAnswer(options[1], options),
            font=CTkFont(family="Noto Sans", size=14),
        )

        op3 = CTkButton(
            quizFrame,
            text=options[2],
            command=lambda: quizAnswer(options[2], options),
            font=CTkFont(family="Noto Sans", size=14),
        )

        op4 = CTkButton(
            quizFrame,
            text=options[3],
            command=lambda: quizAnswer(options[3], options),
            font=CTkFont(family="Noto Sans", size=14),
        )

        op1.pack(side=TOP, fill=X, pady=5, padx=5)
        op2.pack(side=TOP, fill=X, pady=5, padx=5)
        op3.pack(side=TOP, fill=X, pady=5, padx=5)
        op4.pack(side=TOP, fill=X, pady=5, padx=5)

        root.update()


def quizAnswer(option, options):
    global answered, totalQ, nextButton, qNo, op1, op2, op3, op4
    opIndex = options.index(option)
    ansOpIndex = options.index(totalQ[qNo - 1]["correctAnswer"])
    for op in [op1, op2, op3, op4]:
        op.configure(command=None)
    if option == totalQ[qNo - 1]["correctAnswer"]:
        nextButton.pack(side=RIGHT)

        if opIndex == 0:
            op1.configure(fg_color="green")
        if opIndex == 1:
            op2.configure(fg_color="green")
        if opIndex == 2:
            op3.configure(fg_color="green")
        if opIndex == 3:
            op4.configure(fg_color="green")

        answered = 1
        qNo += 1
    else:
        nextButton.configure(command=quizResult)
        nextButton.pack(anchor="e")

        if opIndex == 0:
            op1.configure(fg_color="brown")
        if opIndex == 1:
            op2.configure(fg_color="brown")
        if opIndex == 2:
            op3.configure(fg_color="brown")
        if opIndex == 3:
            op4.configure(fg_color="brown")

        if ansOpIndex == 0:
            op1.configure(fg_color="green")
        if ansOpIndex == 1:
            op2.configure(fg_color="green")
        if ansOpIndex == 2:
            op3.configure(fg_color="green")
        if ansOpIndex == 3:
            op4.configure(fg_color="green")


def quizNext():
    global op1, op2, op3, op4, qLabel, answered, nextButton
    op1.pack_forget()
    op2.pack_forget()
    op3.pack_forget()
    op4.pack_forget()
    qLabel.pack_forget()
    nextButton.pack_forget()
    answered = 1
    quizAsker()


def quizResult():
    statusFrame.destroy()
    quizFrame.destroy()
    resultFrame.pack(fill=BOTH)
    CTkLabel(
        resultFrame,
        text="You scored " + str(qNo - 1),
        font=CTkFont(family="Noto Sans"),
        fg_color="transparent",
    ).place(relx=0.5, rely=0.5)


homeLoader()
root.mainloop()

