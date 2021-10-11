import tkinter as tk
from tkinter import ttk
import requests
#import LoginPage
from LoginPage import LoginPage
from LoggedInAPITester import LoggedInAPITester




class mainApp(tk.Tk):
        global username
        global password
        global header



        def __init__(self, *args, **kwargs):


            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            container.pack(side = "top", fill = "both", expand = True)
            self.geometry('200x150')
            container.grid_rowconfigure(0, weight = 1)
            container.grid_columnconfigure(0, weight = 1)

            self.frames = {}

            for F in (LoginPage,LoggedInAPITester):
                page_name = F.__name__
                print(page_name)
                frame = F(container, self)
                self.frames[page_name] = frame
                frame.grid(row = 0, column = 0, sticky = "nsew")


            self.ChangeFrame("LoginPage")

        def ValidateLogin(self,Username, Password):
            print("Validates Login")
            username = Username
            password = Password
            self.ChangeFrame("LoggedInAPITester")



        def ChangeFrame(self,page):
            try:
                frame = self.frames[page]
                self.title(eval(page))
                frame.tkraise()
            except OSError:
                print("Error")




        def inportHeader(self):
            #example course id is _90767_1 this is for procedural generation
            input = inputText.get(1.0, "end-1c")
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
            response = requests.request("GET",url)

            print(response.json())





        def printResponseForCourseInfo(self):
            #example course id is _90767_1 this is for procedural generation
            input = inputText.get(1.0, "end-1c")
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
            response = requests.request("GET",url)

            print(response.json())



if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
