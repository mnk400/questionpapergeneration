import sqlite3
import random
import itertools
import fpdf

sql = sqlite3.connect("Questionpaper.db")
cur = sql.cursor()
pdf = fpdf.FPDF(format='letter')

def recordentry():
    print("Enter Question?")
    qs = input()
    print("Enter Marks")
    marks = input()
    print("Enter Difficulty?(Easy/Medium/Hard)")
    diff = input()
    diff = diff.upper()
    sql_id_cmd = ("SELECT MAX(ID) FROM "+diff+marks)
    cur.execute(sql_id_cmd)
    data = cur.fetchone()
    if data[0] is None:
        i = 1
    else:
        i = data[0] + 1
    sql_in_cmd = ("INSERT INTO "+diff+marks+" VALUES("+str(i)+",'"+qs+"');")
    cur.execute(sql_in_cmd)
    sql.commit()

def questionselector():
    print("Select Difficulty?(Easy/Medium/Hard)")
    diff = input()
    diff = diff.upper()
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

#recordentry()
questionselector()
sql.close()
