from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import fileinput
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.max_colwidth', -1)
#shortcut to use a window
window=Tk()
window.title("example app")
#window.configure(background="black")
file=pd.read_csv('db.csv',sep='#',engine='python',quoting=3)
#print(file[file['subject']=='CSE',file['number']=='10'])
print(file.query('subject=="CSE" and number=="3"'))
#print(row['description'])

def click():
    entered_sub=textentry.get().upper()
    entered_num=textentrynum.get().upper()
    try:
        #row=file[file['subject']==entered_sub,file['number']==entered_num]
        qstring=('subject=="{}" and number=="{}"')
        row=file.query(qstring.format(entered_sub,entered_num))
        print(row['description'])
        name.configure(text=row['title'].values[0])
        desc.configure(text=row['description'].values[0])
    except:
        name.configure("try to spellcheck")

def close_window():
    window.destroy()
    exit()
   
#@leave window
Button(window,text="EXIT",width=4,command=close_window).pack(side=TOP,anchor=NE)
#creates text object
MyTitle = Label(window,text="My first app",font="Helvetica 16 bold")
#puts text obj in the window
MyTitle.pack()
#creates button that calls the earlier function
#create empty text obj. our random function later makes this text non-null and makes it display
#picture
#PhotoImage object created. Uses PIL image opener inside.
#pic=ImageTk.PhotoImage(Image.open("me.gif").resize(400,400))
#grid: sticky = N,W,E,(S)outh
#puts image in frame
#p=Label(window,image=pic,bg="black").grid(row=1,column=0,sticky=W)

Prompt = Label(window,text="Enter class subject",font="none 12 bold")
Prompt.pack()
Prompt = Label(window,text="Enter class #",font="none 12 bold")
Prompt.pack()

#input 
textentry = Entry(window,width=20,bg="white")
textentry.pack()
textentrynum = Entry(window,width=20,bg="white")
textentrynum.pack()

#output=Text(window,width=30,height=20,wrap=WORD,background="white")
#output.pack()
name = Label(window, font="Helvetica 12 bold",wraplength=300, justify="center")
name.pack()
desc = Label(window, font="Helvetica 12 bold",wraplength=300, justify="center")
desc.pack()

Button(window,text="SUBMIT",width=6,command=click).pack()





window.mainloop()