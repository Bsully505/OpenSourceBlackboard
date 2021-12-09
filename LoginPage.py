import tkinter as tk
from tkinter import ttk


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Sel = False



        #row is up and down an column is the left or right
        #origin is top left

        labelUser = ttk.Label(self, text = "UserName: ")

        textUser = tk.Text(self,height=1 ,width = 15)

        labelPass = ttk.Label(self, text = "Password: ")

        textPass = tk.Text(self,height = 1,width = 15)
        if(Sel==True):
            Submit = tk.Button(self,text = "Submit", command =   lambda:controller.ValidateLoginWithSel(textUser.get(1.0,"end-1c"),textPass.get(1.0,"end-1c")))
        else:
             Submit = tk.Button(self,text = "Submit", command =   lambda:controller.ValidateLogin(textUser.get(1.0,"end-1c"),textPass.get(1.0,"end-1c")))
        Submit.grid(row = 6, column = 4)

        labelUser.grid(row = 2, column = 2)
        textUser.grid(row = 2,column = 4)
        labelPass.grid(row = 4, column = 2)
        textPass.grid(row = 4, column = 4)



    def toString():
        return "LoginPage";

        #label "Username:"    #text box for user
        #label "Password:"    text box for password

        #Button for submitting login
        #button command tests if the username and password is good and then changes fram to loggedinPage
