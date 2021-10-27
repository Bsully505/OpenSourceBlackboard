import tkinter as tk
from tkinter import ttk

#this class
#thinking of turning this into a list of courses that the student is taking 

class LoggedInAPITester(tk.Frame):
    global UserID
    def __init__(self, parent, controller,UserID):
        tk.Frame.__init__(self, parent)
        self.UserID = UserID
        controller.geometry('250x450')
        courses = controller.getCourseIdsandNamesForThisSemester(self.UserID)
      
        for i in courses:
            print(i)
            ttk.Button(self,text = i.split(",")[1],command= lambda:controller.addCourseFrame(i.split(",")[1],i.split(",")[0])).pack()

    
        #ideas is to be able be logged in and call an api using buttons 
        