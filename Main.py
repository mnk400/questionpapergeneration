import sqlite3
import random
import fpdf
from tkinter import *

sql = sqlite3.connect("Questionpaper.db")
cur = sql.cursor()
pdf = fpdf.FPDF(format='letter')

def recordentry(qs, marks, diff):
    sql_id_cmd = ("SELECT MAX(ID) FROM "+diff+marks)
    cur.execute(sql_id_cmd)
    data = cur.fetchone()
    if data[0] is None:
        i = 1
    else:
        i = data[0] + 1
    sql_in_cmd = ("INSERT INTO "+diff+marks+" VALUES("+str(i)+",\""+qs+"\");")
    print(sql_in_cmd)
    cur.execute(sql_in_cmd)
    sql.commit()

def questionselector(diff):
    #print("Select Difficulty?(Easy/Medium/Hard)")
    #diff = input()
    #diff = diff.upper()
    print(diff)
    sql_id_cmd1 = ("SELECT MAX(ID) FROM "+diff+"4")
    sql_id_cmd2 = ("SELECT MAX(ID) FROM "+diff+"6")
    sql_id_cmd3 = ("SELECT MAX(ID) FROM "+diff+"10")
    cur.execute(sql_id_cmd1)
    data1=cur.fetchone()
    cur.execute(sql_id_cmd2)
    data2=cur.fetchone()
    cur.execute(sql_id_cmd3)
    data3=cur.fetchone()
    if data1[0] is None or data2[0] is None or data3[0] is None:
        print("one or more tables are Empty")
        exit()
    elif data1[0]<5 or data2[0]<5 or data3[0]<5:
        print("Not sufficient elements in Tables")
        exit()
    else:
        i1 = data1[0]
        i2 = data2[0]
        i3 = data3[0]
        rand1 = random_num_gen(i1)
        rand2 = random_num_gen(i2)
        rand3 = random_num_gen(i3)
        print(rand1,rand2,rand3)
    j=0
    obj1 = []
    obj2 = []
    obj3 = []
    for i in range(5):
        sql_in_cmd1 = ("SELECT QS FROM "+diff+"4 WHERE "+"ID = "+str(rand1[j]))
        sql_in_cmd2 = ("SELECT QS FROM "+diff+"6 WHERE "+"ID = "+str(rand2[j]))
        sql_in_cmd3 = ("SELECT QS FROM "+diff+"10 WHERE "+"ID = "+str(rand3[j]))
        j = j+1
        cur.execute(sql_in_cmd1)
        obj1.append(list(cur.fetchone()))
        cur.execute(sql_in_cmd2)
        obj2.append(list(cur.fetchone()))
        cur.execute(sql_in_cmd3)
        obj3.append(list(cur.fetchone()))

        #print(data2[0])
        #print(data3[0])
    print(obj1)
    print(obj2)
    print(obj3)
    pdf_gen(obj1,obj2,obj3)

def pdf_gen(list1,list2,list3):
    pdf.add_page()
    pdf.set_font("Times", size=20)
    pdf.cell(200,15,"Physics Exam 2018", ln=1, align="C")
    pdf.set_font("Times",'i', size=17)
    pdf.cell(200,15,"Generated using an automated paper generation system", ln=1, align="C")
    pdf.set_font("Times",'i', size=14)
    pdf.cell(200,10,"A project created by Manik and Nagesh", ln=1, align="C")
    pdf.set_font("Times", size=13)
    pdf.cell(167,15,"Max Marks : 100", align="left")
    pdf.cell(100,15,"Time : 3 Hours",ln=1, align="right")
    pdf.set_font("Arial",'b', size=16)
    pdf.cell(134,15,"Section A", align="left")
    pdf.set_font("Times",'i', size=13)
    pdf.cell(100,15,"Max marks for this section are 4",ln=1, align="left")
    pdf.set_font("Times", size=12)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list1[i][0],ln=1,align="left")
    pdf.set_font("Arial",'b', size=16)
    pdf.cell(134,15,"Section B", align="left")
    pdf.set_font("Times",'i', size=13)
    pdf.cell(100,15,"Max marks for this section are 6",ln=1, align="left")
    pdf.set_font("Times", size=12)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list2[i][0],ln=1,align="left")
    pdf.set_font("Arial",'b', size=16)
    pdf.cell(133,15,"Section C", align="left")
    pdf.set_font("Times",'i', size=13)
    pdf.cell(100,15,"Max marks for this section are 10",ln=1, align="left")
    pdf.set_font("Times", size=12)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list3[i][0],ln=1,align="left")
    pdf.output("file.pdf")

def random_num_gen(n):
    rlist = random.sample(range(n),5)
    rlist = [x+1 for x in rlist]
    return rlist

def mainwin():
    window = Tk()
    window.title("Question Paper Generator")
    window.configure(background='#ECECEC')
    window.geometry('305x180')
    lbl = Label(window, font="SF\Mono 36 bold", text = "Question Paper\nGenerator",background='#ECECEC',justify='left')
    lbl.grid(column=0, row=0,padx=20,pady=10)
    frame=Frame(window)
    frame.grid(column=0,row=3,padx=0,pady=10)
    addbutton=Button(frame,text="Add Question",)
    addbutton.config(height = 2, width = 15,bg='#ECECEC',justify='left',bd='0',relief='raised',command=addQwin)
    addbutton.grid(column=0,row=2)

    genbutton=Button(frame,text="Generate PDF",)
    genbutton.config(height = 2, width = 15,bg='#ECECEC',justify='left',bd='0',relief='raised',command=genpdf)
    genbutton.grid(column=1,row=2)
    window.mainloop()

def addQwin():
    window = Tk()
    window.title("Add Questions")
    window.configure(background='#ECECEC')
    window.geometry('233x460')
    def clicked():
        qs = txt1.get()
        marks = txt2.get()
        diff = txt3.get()
        print(qs,marks,diff)
        recordentry(qs,marks,diff)
    lbl = Label(window, font="SF\Mono 36 bold", text = "Add\nQuestions",background='#ECECEC',justify='left')
    lbl.grid(column=0, row=0,padx=20,pady=10)
    frame1=Frame(window)
    frame1.grid(column=0,row=2,padx=0,pady=10)
    txt1 = Entry(frame1,width=20,bg='#ECECEC')
    txt1.grid(column=0, row=0)
    lbl2 = Label(window, font="SF\Mono 28 bold", text = "Enter Marks",background='#ECECEC',justify='left')
    lbl2.grid(column=0, row=3,padx=20,pady=10)
    frame2=Frame(window)
    frame2.grid(column=0,row=4,padx=0,pady=10)
    txt2 = Entry(frame2,width=20,bg='#ECECEC')
    txt2.grid(column=0, row=0)
    lbl2 = Label(window, font="SF\Mono 26 bold", text = "Enter Difficulty",background='#ECECEC',justify='left')
    lbl2.grid(column=0, row=5,padx=20,pady=10)
    frame3=Frame(window)
    frame3.grid(column=0,row=6,padx=0,pady=10)
    txt3 = Entry(frame3,width=20,bg='#ECECEC')
    txt3.grid(column=0, row=0)
    frame4=Frame(window)
    frame4.grid(column=0,row=7,padx=0,pady=10)
    btn = Button(frame4, text="Submit",command=clicked)
    btn.grid(column=0, row=0)

def genpdf():
    window = Tk()
    window.title("Generate PDF")
    window.configure(background='#ECECEC')

    def clickeasy():
        questionselector("Easy")
        lbl2 = Label(window, font="SF\Mono 14 bold", text = "PDF Generated in\ncurrent working directory",background='#ECECEC')
        lbl2.grid(column=0, row=3,padx=20,pady=10)
    def clickmed():
        questionselector("Medium")
        lbl2 = Label(window, font="SF\Mono 14 bold", text = "PDF Generated in\ncurrent working directory",background='#ECECEC')
        lbl2.grid(column=0, row=3,padx=20,pady=10)
    def clickhard():
        questionselector("Hard")
        lbl2 = Label(window, font="SF\Mono 14 bold", text = "PDF Generated in\ncurrent working directory",background='#ECECEC')
        lbl2.grid(column=0, row=3,padx=20,pady=10)

    lbl = Label(window, font="SF\Mono 36 bold", text = "Generate\nPDF",background='#ECECEC',justify='left')
    lbl.grid(column=0, row=0,padx=20,pady=10)
    frame=Frame(window)
    frame.grid(column=0,row=2,padx=0,pady=10)
    btn1 = Button(frame, text="Easy",command=clickeasy)
    btn1.config(height = 2)
    btn1.grid(column=0, row=0)
    btn2 = Button(frame, text="Medium",command=clickmed)
    btn2.config(height = 2)
    btn2.grid(column=1, row=0)
    btn3 = Button(frame, text="Hard",command=clickhard)
    btn3.config(height = 2)
    btn3.grid(column=2, row=0)

mainwin()
sql.close()
