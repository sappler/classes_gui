from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import webbrowser


window=None
file=None


def close_window():
    window.destroy()
    exit()    

#class that holds all window elements. this makes it easier to delete/create everything fresh
class Elements:
    #opens webpage for current class
    def goto(self):
        webbrowser.open(self.link,new=1)
        
    #searches for class in database and displays its info when submit button is clicked
    def click(self,event=None):
            #retrieves text box string, splits subject/number
            text=self.textentry.get().split(' ')
            try:
                entered_sub=text[0].upper()
                entered_num=text[1].upper()
                #tries to get class from csv
                qstring=('subject=="{}" and number=="{}"')
                row=file.query(qstring.format(entered_sub,entered_num))
                #inserts info into textboxes, changes link to go to that class's page
                self.name.configure(text=row['title'].values[0])
                self.desc.configure(text=row['description'].values[0])
                self.link='https://courses.soe.ucsc.edu/courses/' + entered_sub + entered_num
                self.urlbutton.pack()
            except:
                self.name.configure(text="That is not a class at UCSC.")
                self.clear()
                return
            
            #gets class quarters, if possible
            try:
                temp=row['quarters'].values[0]
                if temp.notnull():
                    self.quarters.configure(text=temp)
                    self.quarters_label.configure(text='Quarters:')
                else:
                    raise Exception('no quarter data')
            except:
                self.quarters.configure(text='')
                self.quarters_label.configure(text='')
            
            #fetches instructors, if possible
            try: 
                temp=row['instructors'].values[0]
                if temp.notnull():
                    self.instructors.configure(text=temp)
                    self.instructors_label.configure(text='Instructors:')
                else:
                    raise Exception('no instr data')
            except:
                self.instructors.configure(text='')
                self.instructors_label.configure(text='')
    
    #packs all objects
    def showall(self):
        self.exit.pack(side=TOP,anchor=NE)
        self.p.pack()
        self.Title.pack(fill=X)
        self.Prompt.pack(fill=X)
        self.textentry.pack()
        # sets cursor inside first text box
        self.textentry.focus()
        self.submit.pack()
        self.name.pack()
        self.desc.pack()
        self.instructors_label.pack()
        self.instructors.pack()
        self.quarters_label.pack()
        self.quarters.pack()
    
    #destroys all objects except exit button
    def killall(self):
        self.p.pack_forget()
        self.Title.pack_forget()
        self.Prompt.pack_forget()
        self.textentry.pack_forget()
        self.submit.pack_forget()
        self.name.pack_forget()
        self.desc.pack_forget()
        self.instructors_label.pack_forget()
        self.instructors.pack_forget()
        self.quarters_label.pack_forget()
        self.quarters.pack_forget()
    
    #clears the output textboxes
    def clear(self):
        self.urlbutton.pack_forget()
        self.desc.configure(text='')
        self.quarters.configure(text='')
        self.quarters_label.configure(text='')
        self.instructors.configure(text='')
        self.instructors_label.configure(text='')
    
    #sets up all objects
    def __init__(self):
        #makes enter button 'press' the submit button
        window.bind('<Return>',self.click)
        self.link=''
        
        
        #opens image as pillow object
        pic_temp=Image.open("images/smal.png")
        pic_temp=pic_temp.resize((175,175), Image.ANTIALIAS)
        self.pic=ImageTk.PhotoImage(pic_temp)
        #puts image in 'frame' (has to be done to display PIL image
        self.p =Label(window,image=self.pic)
        
        
        #creates text object MyTitle. see options
        self.Title = Label(window,text="UCSC offline class lookup",font="Helvetica 16 bold")
        self.Prompt = Label(window,text="Enter class subject, then a space, followed by class number",font="none 12 bold")
        
        #input box
        self.textentry = Entry(window,width=20)

        #all output text boxes
        self.name = Label(window, font="Helvetica 12 bold",justify='left')
        self.desc = Label(window, font="Helvetica 12",wraplength=600,justify='left')
        self.quarters = Label(window, font="Helvetica 12", anchor='w')
        self.instructors = Label(window, font="Helvetica 12",wraplength=600)
        self.quarters_label = Label(window, font="Helvetica 12 bold")
        self.instructors_label = Label(window,font="Helvetica 12 bold")
        
        #buttons: submit, page, and exit buttons
        self.exit = Button(window,text="EXIT",font="bold",width=4,command=close_window,background="red",foreground="white")
        self.submit =  Button(window,text="SUBMIT",width=6,command=self.click)
        self.urlbutton= Button(window,text="Go to Class page",command=self.goto,background="blue",foreground="white")
    
    
if __name__=="__main__":
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    pd.set_option('display.max_colwidth', None)
    file=pd.read_csv('database/db.csv',sep='#',engine='python',quoting=3)
    window=Tk()
    window.title("UCSC Class Lookup")
    #width/height
    window.geometry("1000x750")
    myE=Elements()
    myE.showall()
    window.mainloop()