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
            butt=ttk.Button(self,text = i.split(",")[1],command= lambda i=i:controller.ChangeFrame(i.split(",")[1]))
            controller.addCourseFrame(i.split(",")[1],i.split(",")[0],self.UserID)
            butt.pack()

        buttonUpcoming = tk.Button(self, text = "Get List of Upcoming Assignments", command = lambda:controller.printoutAssignments())
        buttonUpcoming.pack()
        #ideas is to be able be logged in and call an api using buttons 
        