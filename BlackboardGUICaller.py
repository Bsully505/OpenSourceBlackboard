import tkinter as tk
from tkinter import ttk
import requests
#import LoginPage
from LoginPage import LoginPage
from LoggedInAPITester import LoggedInAPITester
import json


#the question that I(Bryan) have is how to get the courses faster
#the answer is to use a different api call which is in the course meembership folder

#first thing to do to get courses 
#get the username from user 
#do search https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName=bcsullivan
class mainApp(tk.Tk):
        global username
        global password
        global userID
        header = {
        'Cookie': 'JSESSIONID=4A5A37413A9F38C27813A90957B1A078; BbClientCalenderTimeZone=America/New_York; web_client_cache_guid=71337fe4-925c-420e-8169-1a508df27f16; COOKIE_CONSENT_ACCEPTED=true; JSESSIONID=795CC5E2FD4C08B446E4C94298548E90; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A3C12E3FB3F56CA8A62BEA365FD369A677D7A1DDDCFCE04BDBD33143BAEBB05A1; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A3C12E3FB3F56CA8A62BEA365FD369A677D7A1DDDCFCE04BDBD33143BAEBB05A1; BbRouter=expires:1634502482,id:DE92A866002A8580F93D3F6A9CD7CF74,signature:88556a6b9d78321459c5f1b7c9a10d68db003f5fbe941fff8c2c42aee1048bca,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:9f02d456-1c12-4fda-ae4c-34212336c88e',
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
            self.ValidateLogin('bcsullivan', 'FakePassword123')
            #self.GetCoursesTaken();
            self.ChangeFrame("LoginPage")

        def ValidateLogin(self,Username, Password):
            
            username = Username
            username = 'bcsullivan'
            password = Password
            userID= self.getUserId(username)
            self.GetCoursesTaken();
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
            
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/?offset=100&courseId=_90503_1"
            response = requests.request("GET",url,headers = headers)
            jsonText = response.json()
            
            #only one page 
            if('paging' not in jsonText):
                print(jsonText);
                print("First and only")
            else:

                nextUrl =jsonText['paging']['nextPage']

            #loops through all of the api results and stops at last page
            
                while('paging' in jsonText):
                    print(nextUrl.split("=")[1])
                    #print(jsonText)
                    nextUrl =jsonText['paging']['nextPage']
                    url = "https://quinnipiac.blackboard.com"+ nextUrl#"&courseid=_90503_1"
                    response = requests.request("GET",url,headers = headers)
                    jsonText = response.json()
                
                #for loop goes here 
                
        def getUserId(username):
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+username
            response = requests.request("GET",url)
            return response.json()['results']['id']

        def printResponseForCourseInfo(self):
            #example course id is _90767_1 this is for procedural generation
            #input = inputText.get(1.0, "end-1c")
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
            response = requests.request("GET",url)

            print(response.json())



if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
