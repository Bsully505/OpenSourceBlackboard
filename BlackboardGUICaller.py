import tkinter as tk
from tkinter import ttk
import requests
#import LoginPage
from LoginPage import LoginPage
from LoggedInAPITester import LoggedInAPITester
import json



class mainApp(tk.Tk):
        global username
        global password
        header = {
        'Cookie': 'JSESSIONID=93F302898351D258EED37AD3B415DDC8; BbClientCalenderTimeZone=America/New_York; JSESSIONID=48E5B689F468CDE38039E367D03A7C84; web_client_cache_guid=71337fe4-925c-420e-8169-1a508df27f16; COOKIE_CONSENT_ACCEPTED=true; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F06B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F06B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; BbRouter=expires:1634266155,id:77801EE8716510CC45DDE3E67E42D7A1,signature:ff2c32b7290c5a17acc09ae4751d4e83c5c5a835449d08e74b4b89c338666811,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:10d4a307-1620-4144-8d10-b98b8f4c5e02',
        'courseId': '_90767_1'
        }



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

            self.GetCoursesTaken();
            self.ChangeFrame("LoginPage")

        def ValidateLogin(self,Username, Password):
            self.GetCoursesTaken();
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

            headers =self.header

            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+"_90767_1"+"/contents"
            response = requests.request("GET",url,headers = headers)

            print(response.json())


        def GetCoursesTaken(self):
            headers = self.header
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/?offset=21000"
            response = requests.request("GET",url,headers = headers)
            jsonText = response.json()
            nextUrl =jsonText['paging']['nextPage']
            while('paging' in jsonText):
                print(len(jsonText))
                
                
                print(nextUrl.split("=")[1])
                nextUrl =jsonText['paging']['nextPage']
                url = "https://quinnipiac.blackboard.com"+ nextUrl
                response = requests.request("GET",url,headers = headers)
                jsonText = response.json()
                
                #for loop goes here 
                


        def printResponseForCourseInfo(self):
            #example course id is _90767_1 this is for procedural generation
            #input = inputText.get(1.0, "end-1c")
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
            response = requests.request("GET",url)

            print(response.json())



if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
