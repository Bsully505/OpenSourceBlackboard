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
        'Cookie': 'JSESSIONID=5920E6AB77AAE6A7F7F8D65F6F941CEA; BbClientCalenderTimeZone=America/New_York; web_client_cache_guid=0fd5b16b-78bc-45d9-8faa-ccf10d77304f; COOKIE_CONSENT_ACCEPTED=true; JSESSIONID=88B6279BA70A1672BB675D99BF83F60B; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F03C12E3FB3F56CA8A62BEA365FD369A677D7A1DDDCFCE04BDBD33143BAEBB05A1; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED99208A7AE0BA845CCE05C9AA0AF618C176F03C12E3FB3F56CA8A62BEA365FD369A677D7A1DDDCFCE04BDBD33143BAEBB05A1; BbRouter=expires:1634771083,id:2E58239C3B6241A2D1182BABFDA59B31,signature:822fada71b91a874ea8c29ebe4a8683160e198b38cec6174b2592a0fd71b8533,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:2f576c06-234b-4e92-a142-fa8c9b02157b'
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
        #very important function it gets the username to get the userid(the way that blackboard tracks students(student primary key)) and then basically starts the program
        def ValidateLogin(self,Username, Password):
            
            username = Username
            password = Password
            self.userID = self.getUserId(username)
            self.SetCourseIDInfo()
            #self.printoutCourseIDs()
            #self.PrintCourseNamesWithIds()
            self.ChangeFrame("LoggedInAPITester")
            self.printoutAnnouncements('_90503_1')



        def ChangeFrame(self,page):
            try:
                frame = self.frames[page]
                self.title(page)
                frame.tkraise()
            except OSError:
                print("Error")



        #not a function that is being used
        def importHeader(self):
            #example course id is _90767_1 this is for procedural generation
            #this would possibly be where selenium is used to capture the cookie of jsessionid
            print('get session cookie and set to header')
        
                
         #returns the userID of the username        
        def getUserId(self,username):
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+username
            response = requests.request("GET",url,headers= self.header)
            return response.json()['results'][0]['id']

        def SetCourseIDInfo(self):
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


        def PrintCourseNames(self):
            for i in self.courses:
                print(self.printoutCourseNameIndividual(i))

        def PrintCourseNamesWithIds(self):
            for i in self.courses:
                print(self.printoutCourseNameIndividual(i))
                print(i)

        def printoutAnnouncements(self,CourseID):
            url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/announcements'
            response = requests.request("GET", url, headers = self.header)
            #print(response.json()['name'] + " it worked!")
            for res in response.json()['results']:
                #print(res)
                print(res['title'])
                print(res['body'])



if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
