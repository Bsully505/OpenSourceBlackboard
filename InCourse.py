import tkinter as tk
from tkinter import ttk

#this class
#thinking of turning this into a list of courses that the student is taking 

class InCourse(tk.Frame):
    global CourseID
    def __init__(self, parent, controller,CourseID,userID):
        tk.Frame.__init__(self, parent)
        self.CourseID = CourseID
        controller.geometry('250x450')
        tk.Button(self,text = "Back",command=lambda:controller.ChangeFrame("LoggedInAPITester")).pack()
        labelCourses = ttk.Label(self, text = "Get list of courses")
        buttonCourses = tk.Button(self, text = "Courses", command = lambda:controller.getCourseIdsForThisSemester(userID))
        labelGrades = ttk.Label(self, text = "Get list of grades")
        buttonGrades = tk.Button(self, text = "Grades", command = lambda:controller.printoutGrades(self.CourseID))
        labelAnnouncements = ttk.Label(self, text = "Get list of announcements")
        buttonAnnouncements = tk.Button(self, text = "Announcements", command = lambda:controller.printoutAnnouncements(self.CourseID))
        
        labelCourses.pack()
        buttonCourses.pack()
        labelGrades.pack()
        buttonGrades.pack()
        labelAnnouncements.pack()
        buttonAnnouncements.pack()
        

    
        #ideas is to be able be logged in and call an api using buttons 

        

