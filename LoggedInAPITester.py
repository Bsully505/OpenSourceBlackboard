import tkinter as tk
from tkinter import ttk

#this class
class LoggedInAPITester(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #row is up and down an column is the left or right
        #origin is top left

        labelUser = ttk.Label(self, text = "UserName: ")

        textUser = tk.Text(self,height=1 ,width = 15)

        labelPass = ttk.Label(self, text = "Password: ")

        textPass = tk.Text(self,height = 1,width = 15)

        Submit = tk.Button(self,text = "Submit", command = lambda : controller.ChangeFrame("LoginPage"))
        Submit.grid(row=6, column =4)
        labelUser.grid(row = 2, column = 2)
        textUser.grid(row = 2,column = 4)
        labelPass.grid(row = 4, column = 2)
        textPass.grid(row = 4, column = 4)

        #label "Username:"    #text box for user
        #label "Password:"    text box for password

        #Button for submitting login
        #button command tests if the username and password is good and then changes fram to loggedinPage
    def toString():
        return "LoggedInAPITester"
def printText(self):
    input = textUser
