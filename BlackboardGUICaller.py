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
#do search https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName=bcsullivan or user = username
#print out the courses

#problem that occurs 
#which courses should This app be interested in 

#things that Bryan has found out 
#when getting api calls and from json the way to acess the results is doing 
#for  val in response.json()['results'][0] and this will run a for loop on all outputs
#only the session id users courses can be accessed all others are 404 unauth

class mainApp(tk.Tk):
        global username
        global password
        global userID
        courses = []
        preUrl = 'https://quinnipiac.blackboard.com/'
        header = {
        'Cookie': 'JSESSIONID=B9A00112811A9CD22B1A8F7F05A4A09F; BbClientCalenderTimeZone=America/New_York; web_client_cache_guid=2f5ecba6-3258-4b3d-977a-ecae91e35061; COOKIE_CONSENT_ACCEPTED=true; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F06B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F06B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; JSESSIONID=45DAC7F1DEFC0228588BF6F9F3214201; BbRouter=expires:1634604019,id:B3D688374C3E9EA55D7FD765D4345C40,signature:9bb512f069408b00076d4c915d27ba5bf06c16444f853d613f5c9314c9839ad4,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:3eb7d13a-1c7a-4897-9e5b-b16d4d16b7e1'
        }



        def __init__(self, *args, **kwargs):

            
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            container.pack(side = "top", fill = "both", expand = True)
            self.geometry('200x150')
            container.grid_rowconfigure(0, weight = 1)
            container.grid_columnconfigure(0, weight = 1)

            self.frames = {}
            #create the main panels for the tkinter
            for F in (LoginPage,LoggedInAPITester):
                page_name = F.__name__
                frame = F(container, self)
                self.frames[page_name] = frame
                frame.grid(row = 0, column = 0, sticky = "nsew")

            #self.ValidateLogin('cjflannery', 'FakePassword123') this was to test if when using the token from bcsullivan can i access someone elses account does not work
            self.ValidateLogin('bcsullivan', 'FakePassword123')
            self.ChangeFrame("LoginPage")

        def ValidateLogin(self,Username, Password):
            
            username = Username
            password = Password
            self.userID = self.getUserId(username)
            self.printResponseForCourseInfo()
            self.printoutCourseIDs()
            self.ChangeFrame("LoggedInAPITester")



        def ChangeFrame(self,page):
            try:
                frame = self.frames[page]
                self.title(page)
                frame.tkraise()
            except OSError:
                print("Error")



        #not a function that is being used
        def inportHeader(self):
            #example course id is _90767_1 this is for procedural generation
            #this would possibly be where selenium is used to capture the cookie of jsessionid
            print('get session cookie and set to header')
        
                
         #returns the userID of the username        
        def getUserId(self,username):
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+username
            response = requests.request("GET",url,headers= self.header)
            return response.json()['results'][0]['id']

        def printResponseForCourseInfo(self):
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/users/"+self.userID+"/courses"
            response = requests.request("GET",url, headers = self.header)
            #prints out the courses that the student is enrolled in 
            for res in response.json()['results']:
                self.courses.append(str(res['courseId']))
                #self.printoutCourseNameIndividual(res['courseId'])
                #print()
            
        
        def printoutCourseNameIndividual(self,courseId):
            url = self.preUrl + '/learn/api/public/v3/courses/'+courseId
            response = requests.request("GET",url,headers = self.header)
            print(response.json()['name'])

                
        def printoutCourseIDs(self):
            for i in self.courses:
                print(i)


if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
