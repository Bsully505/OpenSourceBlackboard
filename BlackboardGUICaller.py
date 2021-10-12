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
        'Cookie': 'JSESSIONID=1D649AA6BF0918ABB0CEC762AE99907F; BbClientCalenderTimeZone=America/New_York; web_client_cache_guid=293fa897-374c-4184-8348-aaea3369328a; COOKIE_CONSENT_ACCEPTED=true; OptanonConsent=isIABGlobal=false&datestamp=Wed+Oct+06+2021+17:41:07+GMT-0400+(Eastern+Daylight+Time)&version=6.19.0&hosts=&consentId=d95e8315-f74c-4afb-b76b-df93befcae93&interactionCount=1&landingPath=https://www.blackboard.com/&groups=C0001:1,C0003:1,BG1:1,C0002:1,C0005:1,C0004:1; JSESSIONID=C2ED5B2938F1AC008B73AE97954D2DF9; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A6B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A6B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; BbRouter=expires:1634003558,id:B92E7FAEE20055E9F718395E924C8EC0,signature:66c9d74c699da4f1a9466591f7d2f992102a8a7161edc1a4242beab34ee72832,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:afdf8090-3457-4e34-aed0-6c92002803df',
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
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/?offset=1000"
            response = requests.request("GET",url,headers = headers)
            jsonText = response.json()
            #for open in jsonText['results']:
            #    for attr in open:
            #        print(attr)
            #        print(attr.index)

            print(json.dumps(jsonText,indent = 4, sort_keys=True))


        def printResponseForCourseInfo(self):
            #example course id is _90767_1 this is for procedural generation
            #input = inputText.get(1.0, "end-1c")
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
            response = requests.request("GET",url)

            print(response.json())



if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
