import tkinter as tk
from tkinter import ttk

#this class
class LoggedInAPITester(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry('250x450')
        labelCourses = ttk.Label(self, text = "Get list of courses")
        buttonCourses = tk.Button(self, text = "Courses", command = lambda:controller.GetCoursesTaken())
        labelGrades = ttk.Label(self, text = "Get list of grades")
        buttonGrades = tk.Button(self, text = "Grades", command = lambda:controller.GetCoursesTaken())
        labelAnnouncements = ttk.Label(self, text = "Get list of announcements")
        buttonAnnouncements = tk.Button(self, text = "Announcements", command = lambda:controller.GetCoursesTaken())
        labelUpcoming = ttk.Label(self, text = "Get list of upcoming assignments")
        buttonUpcoming = tk.Button(self, text = "Upcoming Assignments", command = lambda:controller.GetCoursesTaken())
        labelCourses.pack()
        buttonCourses.pack()
        labelGrades.pack()
        buttonGrades.pack()
        labelAnnouncements.pack()
        buttonAnnouncements.pack()
        labelUpcoming.pack()
        buttonUpcoming.pack()

    
        #ideas is to be able be logged in and call an api using buttons 

        

